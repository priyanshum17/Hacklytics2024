import streamlit as st

def main():
    st.title("LET'EM COOK")

    col1, col2 = st.columns(2)
    # Height input
    with col1:
        height_feet = st.slider("Height", 4, 8, step=1)
    # Height input
    with col2:
        eight_inches =  height_feet = st.slider("Height", 0, 11, step=1)
    
    col1, col2 = st.columns(2)
    # Weight input
    with col1:
        age = st.number_input("Age", min_value=14, max_value=100, step=1)
    # Age input
    with col2:
        weight = st.number_input("Weight", min_value=0, max_value=400, step=1)

    col1, col2 = st.columns(2)
    with col1:
        type_option = st.selectbox("Select an option", ["N/A","Increase Weight", "Decrease Weight", "More Muscles"])
    with col2:
        diet_option = st.selectbox("Select a diet option", ["Non-Vegetarian", "Vegetarian", "Vegan", "Dairy Free", "Gluten Free"]) 


    with open("backend/ingredients.txt", "r") as file:
        ingredients_set = eval(file.read())

# Convert the set to a list
    ingredients_list = list(ingredients_set)  
    fridge_items = st.multiselect("Items in the fridge",  ingredients_list)

     
if __name__ == "__main__":
    main()
