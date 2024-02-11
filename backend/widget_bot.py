import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open(age, gender, activity, weight, height_ft, height_in):
    driver = Driver(uc=True)

    # Open the URL
    url = "https://www.myplate.gov/widgets/myplate-plan-start"
    driver.get(url)

    # Click "Start"
    start_button = driver.find_element(By.ID, "edit-start")
    start_button.click()

    # Time Delay
    age_dropdown_locator = (By.ID, "edit-age")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(age_dropdown_locator))

    # Select age
    age = f"{age} years old"
    age_dropdown = Select(driver.find_element(*age_dropdown_locator))
    age_dropdown.select_by_visible_text(age)

    # Select Gender [M/F]
    assert(gender == 'm' or gender == 'f')
    sex_dropdown = Select(driver.find_element(By.ID, "edit-sex"))
    sex_dropdown.select_by_value(gender)

    # Activity level
    assert(type(activity) == int and 1 <= activity <= 3)
    activity_dropdown = Select(driver.find_element(By.ID, "edit-physical-activity"))
    activity_dropdown.select_by_value(f"{activity}")

    # Input Weight
    assert(weight % 10 == 0)
    weight_input = driver.find_element(By.ID, "edit-weight")
    weight_input.clear()
    weight_input.send_keys(f"{weight}")

    # Height [Feet Component]
    height_feet_dropdown = Select(driver.find_element(By.ID, "edit-height-feet"))
    height_feet_dropdown.select_by_value(f"{height_ft}")

    # Height [Inches Component]
    height_inches_dropdown = Select(driver.find_element(By.ID, "edit-height-inches"))
    height_inches_dropdown.select_by_value(f"{height_in}")

    # Click Submit
    calculate_button = driver.find_element(By.ID, "edit-submit")
    calculate_button.click()

    # Time Delay
    plan_link_locator = (By.XPATH, "//p[@class='plan-link']/a[@id='standard_pattern']")
    plan_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(plan_link_locator))

    # Plan Hyperlink
    plan_link_href = plan_link.get_attribute("href")

    driver.quit()

    return plan_link_href

def nutrition(url):

    response = requests.get(url)

    list = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")   
        food_groups = soup.find_all("div", class_="mp-plan-food-groups-item__title")
        
        # Extract and print the text under each food group
        for food_group in food_groups:

            # Find the corresponding body containing information about the food group
            body = food_group.find_next_sibling("div", class_="mp-plan-food-groups-item__body")
            
            # Extract and print the text under the body
            if body:
                paragraphs = body.find_all("p")
                for paragraph in paragraphs:
                    list.append(paragraph.get_text(strip=True))
    
    return list

# print(open())
# print(nutrition(open()))