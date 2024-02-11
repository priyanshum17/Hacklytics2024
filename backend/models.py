import numpy as np
import util

class Meal:
    def __init__(self, data):
        self.data = data
        self.id = self.data["id"]
        self.title = self.data["title"]
        self.image = self.data["image"]
        self.restrictions = self.data["diets"] # verify
        self.nutrition = self.parse_nutrition(self.data["nutrition"]["nutrients"])
        self.ingredients = self.parse_ingredients(self.data["nutrition"]["ingredients"])
        self.categories = self.data["dishTypes"]
        self.cuisines = self.data["cuisines"]
        self.time = self.data["readyInMinutes"]
        self.servings = self.data["servings"]

    def parse_nutrition(self, nutrients):
        temp = {}
        for i in range(len(nutrients)):
            temp[nutrients[i]["name"].lower()] = nutrients[i]["percentOfDailyNeeds"]
        return [temp.get(util.NUTRIENTS_LIST[i], 0) for i in range(len(util.NUTRIENTS_LIST))]
  	
    def parse_ingredients(self, ingredients):
        return [(ingredient["id"], ingredient["amount"]) for ingredient in ingredients]

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
                aggregate[cuisine] = aggregate.get(cuisine, 0)
        
        cost = 0
        for cuisine in preferences:
            cost -= aggregate[cuisine] * preferences[cuisine]
        return cost

    def ingredient_cost(self, ingredients):
        aggregate = {}
        for meal in self.meals:
            for ingredient in meal.ingredients:
                aggregate[ingredient["id"]] = aggregate.get(ingredient["id"], 0) + ingredient["amount"]

        cost = 0
        for _id in aggregate:
            cost += (aggregate[_id] - ingredients.get(_id, 0)) / aggregate[_id]
        return cost

    def nutrition_cost(self, dv):
        return np.sqrt(np.sum(util.NUTRITION_WEIGHTS * (sum([meal.nutrition for meal in self.meals]) - dv) ** 2))

    def total_cost(self, preferences, ingredients, dv):
        return np.dot(np.array([self.variety_cost(), self.time_cost(), self.preference_cost(preferences), self.ingredient_cost(ingredients), self.nutrition_cost(dv)]), util.COST_WEIGHTS)

class User:
    # demographics: age, gender, height, weight, exercise
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
        User._demographics = demographics
        User._goals = goals
        User._restrictions = restrictions
        User._preferences = preferences
        User._meal_types = meal_types
        User._restaurants = restaurants
        User._ingredients = ingredients

    @classmethod
    def calculate_calories(cls):
        # scraping work
        return

    @classmethod
    def calculate_goal_dv(cls):
        calories = User.calculate_calories() + 200 * User._goals[0] - 200 * User._goals[1]
        User.dv = [1.0] * len(MealPlan.nutrients_list) * calories / 2000
        User.dv[-1] += 0.3 * User._goals[2]
