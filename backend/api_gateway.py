import requests

api_key = "25caf462649d4081a1db984a688a8b68"
url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}"
params = {
    "number": 5,
    "include-tags": "vegetarian"
}
print(requests.get(url=url, params=params).text)