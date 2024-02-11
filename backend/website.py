import time
import streamlit as st
from models import User, Meal
from ai import run_ga, get_data
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import webbrowser

_demographics = []
_goals = []
_restrictions = []
_preferences = {}
_meal_types = []
_restaurants = []
_ingredients = {}

user = User([], [False, False, False], [], {}, [True, True, True], [], {})

st.set_page_config(layout="wide")



def main():
    st.title("LET 'EM COOK")

    col1, col2, col3 = st.columns(3)
    # Weight input
    with col1:
        age = st.number_input("Age", min_value=14, max_value=100, step=1)
    # Age input
    with col2:
        weight = st.number_input("Weight", min_value=0, max_value=400, step=1)
    
    with col3:
        gender = st.selectbox("Enter Gender", ["Female", "Male"])

    col1, col2 = st.columns(2)
    # Height input
    with col1:
        height_feet = st.slider("Height", 4, 7, step=1)
    # Height input
    with col2:
        eight_inches =  height_feet = st.slider("Height", 0, 11, step=1)

    col1, col2, col3 = st.columns(3)
    with col1:
        options = ["N/A","Increase Weight", "Decrease Weight", "More Muscles"]
        type_option = st.selectbox("Select an option", ["Balanced Diet","Increase Weight", "Decrease Weight", "More Muscles"])
    with col2:
        diet_option = st.selectbox("Select a diet option", ["Non-Vegetarian", "Vegetarian", "Vegan", "Dairy Free", "Gluten Free"])
    with col3:
        cuisines = ["African", "Asian","American","British", "Cajun","Caribbean","Chinese","Eastern European","European","French",
                    "German","Greek","Indian","Irish","Italian","Japanese","Jewish","Korean","Latin American","Mediterranean","Mexican",
                    "Middle Eastern","Nordic","Southern","Spanish","Thai","Vietnamese"]
        cusine_option = st.selectbox("Select Cuisine", cuisines)


    with open("ingredients_2.json", "r") as file:
        ingredients_set = eval(file.read())

# Convert the set to a list
    ingredients_list = list(ingredients_set)  
    fridge_items = st.multiselect("Items in the fridge",  ingredients_list)
    # btn = st.button("Generate Recipe")
    # if btn:
    #     progress_bar = st.progress(0)
    #     with st.empty():
    #         for i in range(101):
    #             time.sleep(0.05)
    #             progress_bar.progress(i)
    #         st.write("**Recipe Details**")
    #         st.write(f"**Name:** {recipe_name}")
    #         st.image(image_src, width=200)
    #         st.write(f"**Duration:** {duration} minutes")
    #         st.write(f"**Calorie Count:** {calorie_count} calories")

    ingredients = {each: 1000000 for each in fridge_items}
    User._ingredients = ingredients
    User._preferences = {cusine_option.lower(): 1.0}
    if type_option != "Balanced Diet":
        User._goals[options.index(type_option) - 1] = True
    if diet_option != "Non-Vegetarian":
        User._restrictions = [diet_option[0].lower() + diet_option.replace(" ", "")[1:]]
    # print(User._restrictions)
    User.calculate_goal_dv()

    if "cond" not in st.session_state:
        st.session_state.cond = False
    
    generate = st.button("Generate Meal Plan")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    if generate:
        st.session_state.cond = True
        get_data(User._meal_types, User._restrictions)
        solution = np.array(run_ga())
        st.session_state.solution = np.reshape(solution, newshape=(7,3))

    
    
    with tab1:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[0][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Sunday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Sunday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[0][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Sunday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Sunday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[0][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Sunday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Sunday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories") 

    with tab2:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[1][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Monday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Monday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[1][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Monday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Monday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[1][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Monday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Monday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
    
    with tab3:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[2][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Tuesday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Tuesday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[2][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Tuesday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Tuesday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[2][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Tuesday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Tuesday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories") 
    

    with tab4:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[3][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Wednesday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Wednesday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[3][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Wednesday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Wednesday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[3][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Wednesday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Wednesday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories") 
    
    with tab5:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[4][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Thursday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Thursday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[4][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Thursday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Thursday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[4][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Thursday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Thursday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories") 
    

    with tab6:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[5][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Friday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Friday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[5][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Friday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Friday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[5][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Friday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Friday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories") 

    with tab7:
        st.write("**Recipe Details**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.cond == True:
                meal = st.session_state.solution[6][0]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_00 = st.button("Saturday Breakfast")
                if button_00:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Saturday Breakfast")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col2:
            if st.session_state.cond == True:
                meal = st.session_state.solution[6][1]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_01 = st.button("Saturday Lunch")
                if button_01:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Saturday Lunch")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories")
        with col3:
            if st.session_state.cond == True:
                meal = st.session_state.solution[6][2]
                st.write(f"**Name:** {meal.title}")
                st.image(meal.image, width=200)
                st.write(f"**Duration:** {meal.time} minutes")
                st.write(f"**Calorie Count:** {round(meal.nutrition[0] / 100 * 2000)} calories")
                button_02 = st.button("Saturday Dinner")
                if button_02:
                    webbrowser.open_new_tab(meal.url)
            else:
                st.write("Saturday Dinner")
                st.write(f"**Name:** -")
                st.write(f"**Duration:** - minutes")
                st.write(f"**Calorie Count:** - calories") 
    

if __name__ == "__main__":
    main()
