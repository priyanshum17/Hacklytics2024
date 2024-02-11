import time
import streamlit as st

st.set_page_config(layout="wide")

def main():
    st.title("LET 'EM COOK")

    col1, col2 = st.columns(2)
    # Weight input
    with col1:
        age = st.number_input("Age", min_value=14, max_value=100, step=1)
    # Age input
    with col2:
        weight = st.number_input("Weight", min_value=0, max_value=400, step=1)

    col1, col2 = st.columns(2)
    # Height input
    with col1:
        height_feet = st.slider("Height", 4, 7, step=1)
    # Height input
    with col2:
        eight_inches =  height_feet = st.slider("Height", 0, 11, step=1)

    col1, col2, col3 = st.columns(3)
    with col1:
        type_option = st.selectbox("Select an option", ["N/A","Increase Weight", "Decrease Weight", "More Muscles"])
    with col2:
        diet_option = st.selectbox("Select a diet option", ["Non-Vegetarian", "Vegetarian", "Vegan", "Dairy Free", "Gluten Free"])
    with col3:
        cuisines = ["African", "Asian","American","British", "Cajun","Caribbean","Chinese","Eastern European","European","French",
                    "German","Greek","Indian","Irish","Italian","Japanese","Jewish","Korean","Latin American","Mediterranean","Mexican",
                    "Middle Eastern","Nordic","Southern","Spanish","Thai","Vietnamese"]
        cusine_option = st.selectbox("Select Cusine", cuisines)


    with open("backend/ingredients.txt", "r") as file:
        ingredients_set = eval(file.read())

# Convert the set to a list
    ingredients_list = list(ingredients_set)  
    fridge_items = st.multiselect("Items in the fridge",  ingredients_list)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

    with tab1:
        col1, col2, col3 = st.columns(3)

        with col1:
            recipe_name = "Name"
            image_src = "https://static.streamlit.io/examples/cat.jpg"
            duration = 100
            calorie_count = 2000
            st.write("**Recipe Details**")
            st.write(f"**Name:** {recipe_name}")
            st.write(f"**Duration:** {duration} minutes")
            st.write(f"**Calorie Count:** {calorie_count} calories")
            btn1 = st.button("Generate Recipe")

            if btn1:
                progress_bar = st.progress(0)
                with st.empty():
                    for i in range(101):
                        time.sleep(0.05)
                        progress_bar.progress(i)
                    st.write("**Recipe Details**")
                    st.write(f"**Name:** {recipe_name}")
                    st.image(image_src, width=200)
                    st.write(f"**Duration:** {duration} minutes")
                    st.write(f"**Calorie Count:** {calorie_count} calories")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            btn2 = st.button("Sunday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            btn3 = st.button("Sunday Dinner")
    

    with tab2:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Monday Breakfast")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Monday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Monday Dinner")
    
    with tab3:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Tuesday Breakfast")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Tuesday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Tuesday Dinner")
    

    with tab4:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Wednesday Breakfast")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Wednesday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Wednesday Dinner")
    
    with tab5:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Thursday Breakfast")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Thursday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Thursday Dinner")
    

    with tab6:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Friday Breakfast")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Friday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Friday Dinner")

    with tab7:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Saturday Breakfast")
        
        with col2:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Saturday Lunch")
        
        with col3:
            st.write("Receipe Name")
            st.write("duration")
            st.write("Calorie Count")
            button = st.button("Saturday Dinner")
    

if __name__ == "__main__":
    main()
