from models import Meal, MealPlan, User
import json
import pygad
import time

def get_data():
    inFile = open("meals/bfast.json",'r')
    breakfasts = json.load(inFile)
    inFile = open("meals/main_course.json",'r')
    mains = json.load(inFile)

    breakfasts = [Meal(meal) for meal in breakfasts]
    mains = [Meal(meal) for meal in mains]
    meals = breakfasts + mains

    breakfasts = [meal.id for meal in breakfasts]
    mains = [meal.id for meal in mains]
    meal_dict = {meal.id: meal for meal in meals}

    return breakfasts, mains, meal_dict

final = False
breakfasts, mains, meal_dict = get_data()

def fitness_func(ga_instance, solution, solution_idx):
    global final, meal_dict

    mealplan = MealPlan([meal_dict[meal] for meal in solution])
    cost = -mealplan.total_cost(User._preferences, User._ingredients, User.dv, final)

    if final:
        print(cost)

    return cost

def run_ga(debug=False):
    daily_meals = [breakfasts, mains, mains]
    gene_space = [daily_meals[i] for i in range(len(daily_meals)) if User._meal_types[i]] * 7

    ga_instance = pygad.GA(
        num_generations=250,                          # Number of generations
        num_parents_mating=4,                         # Number of parents selected for mating
        fitness_func=fitness_func,                    # Fitness function
        sol_per_pop=min(len(breakfasts), len(mains)), # Number of solutions in the population
        num_genes=len(gene_space),                    # Number of genes (variables) in the solution
        gene_type=int,
        gene_space=gene_space,
        parent_selection_type="tournament",           # Parent selection method
        crossover_type="uniform",                     # Crossover method
        mutation_type="random",                       # Mutation method
        mutation_percent_genes=15,                    # Percentage of genes to mutate
        suppress_warnings=True,
    )

    start = time.time()
    ga_instance.run()
    if debug:
        print('finished in', time.time() - start)

    solution, solution_fitness, _ = ga_instance.best_solution()
    if debug:
        print("solution, fitness:", solution, solution_fitness)
        final = True
        fitness_func(None, solution, None)
        ga_instance.plot_fitness()
