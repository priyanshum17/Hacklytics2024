from ai import run_ga
from models import User

user = User([], [False, False, False], [], {'indian': 1.0, 'american': 0.1, 'chinese': 0.6}, [True, True, True], [], {})
run_ga(True)
