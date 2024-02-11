import numpy as np
import util
import widget_bot as wb

class Meal:
    def __init__(self, data):
        self.data = data
        self.id = self.data["id"]
        self.title = self.data["title"]
        self.image = self.data["image"]
        self.restrictions = self.data["diets"] # verify
        self.nutrition = self.parse_nutrition(self.data["nutrition"]["nutrients"])
        self.ingredients = self.parse_ingredients(self.data["nutrition"]["ingredients"])
        self.categories = [each.lower() for each in self.data["dishTypes"]]
        self.cuisines = [each.lower() for each in self.data["cuisines"]]
        self.time = self.data["readyInMinutes"]
        self.servings = self.data["servings"]
        self.url = self.data["spoonacularSourceUrl"]

    def parse_nutrition(self, nutrients):
        temp = {}
        for i in range(len(nutrients)):
            temp[nutrients[i]["name"].lower()] = nutrients[i]["percentOfDailyNeeds"]
        return [temp.get(util.NUTRIENTS_LIST[i], 0) for i in range(len(util.NUTRIENTS_LIST))]
  	
    def parse_ingredients(self, ingredients):
        return [(ingredient["id"], ingredient["amount"]) for ingredient in ingredients]
    
    def __str__(self):
        output = ''
        output += "title: " + self.title
        output += '\n'
        output += "restrictions: " + str(self.restrictions)
        output += '\n'
        output += "nutrition: " + str(self.nutrition)
        output += '\n'
        output += "ingredients: " + str(self.ingredients)
        output += '\n'
        output += "categories: " + str(self.categories)
        output += '\n'
        output += "cuisines: " + str(self.cuisines)
        output += '\n'
        output += "cook time: " + str(self.time)
        return output

class MealPlan:
    def __init__(self, meals):
        self.meals = meals

    def variety_cost(self):
        counts = {}
        for meal in self.meals:
            if meal.id in counts:
                counts[meal.id] += 1
            else:
                counts[meal.id] = 1

        max_count = 0
        for count in counts.values():
            if count > util.COUNT_THRESHOLD:
                return util.VARIETY_COST
            if count > max_count:
                max_count = count

        return 0
  
    def time_cost(self):
        ids = set()
        time = 0

        # TODO: store bought meals don't have saved time cost
        for meal in self.meals:
            if meal.id not in ids:
                time += meal.time
                ids.add(meal)

        return time

    def preference_cost(self, preferences):
        aggregate = {}
        for meal in self.meals:
            for cuisine in meal.cuisines:
                aggregate[cuisine] = aggregate.get(cuisine, 0) + 1
        
        cost = 0
        for cuisine in preferences:
            cost -= aggregate.get(cuisine, 0) * preferences[cuisine]
        return cost

    def ingredient_cost(self, ingredients):
        aggregate = {}
        for meal in self.meals:
            for ingredient in meal.ingredients:
                aggregate[ingredient[0]] = aggregate.get(ingredient[0], 0) + ingredient[1]

        cost = 0
        for _id in aggregate:
            cost += max(0, aggregate[_id] - ingredients.get(_id, 0)) / aggregate[_id]
        return cost

    def nutrition_cost(self, dv, debug=False):
        error = sum([np.array(meal.nutrition) for meal in self.meals]) / 7 - np.array(dv)
        if debug:
            print(error)
        return np.sqrt(np.sum(util.NUTRITION_WEIGHTS * error ** 2))

    def total_cost(self, preferences, ingredients, dv, debug=False):
        costs = util.COST_WEIGHTS * np.array([self.variety_cost(), self.time_cost(), self.preference_cost(preferences), self.ingredient_cost(ingredients), self.nutrition_cost(dv, debug)])
        if debug:
            print(costs)
        return np.sum(costs)

class User:
    # demographics: age, gender, activity, weight, height_ft, height_in
    # goals: gain weight, lose weight, gain muscle
    # restrictions: restrictions
    # preferences: cuisines
    # meal types: breakfast, lunch, dinner
    # restaurants: location, radius, outside meals per week
    # ingredients: home ingredients

    _demographics = []
    _goals = []
    _restrictions = []
    _preferences = {}
    _meal_types = []
    _restaurants = []
    _ingredients = {}
    dv = []

    def __init__(self, demographics, goals, restrictions, preferences, meal_types, restaurants, ingredients):
        User._demographics = demographics # age, gender, activity, weight, height_ft, height_in
        User._goals = goals
        User._restrictions = restrictions
        User._preferences = preferences
        User._meal_types = meal_types
        User._restaurants = restaurants
        User._ingredients = ingredients
        User.calculate_goal_dv()

    @classmethod
    def calculate_calories(cls):
        # TODO: revert after testing
        # link = wb.open(*User._demographics)
        # return int(link.split('/')[-1].split('-')[0])
        return 2000

    @classmethod
    def calculate_goal_dv(cls):
        calories = User.calculate_calories() + 200 * User._goals[0] - 200 * User._goals[1]
        User.dv = np.array([100.0] * len(util.NUTRIENTS_LIST)) * (calories / 2000)
        User.dv[-1] += 30.0 * User._goals[2]
    
