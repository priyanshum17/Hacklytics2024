import numpy as np

NUTRIENTS_LIST = ['calories', 'fat', 'saturated fat', 'carbohydrates', 'net carbohydrates', 'sugar', 'cholesterol', 'sodium', 'protein']
NUTRITION_WEIGHTS = np.array([1 / len(NUTRIENTS_LIST)] * len(NUTRIENTS_LIST)) # tuned later
COUNT_THRESHOLD = 3
VARIETY_COST = 500
COST_WEIGHTS = np.array([1, 1, 1, 1, 1])
