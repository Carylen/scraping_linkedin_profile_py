from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def login(driver, url, email, password):
    driver.get(url)
    print('- Finish initializing a driver')

    # Task 1.2: Key in login credentials
    email_field = driver.find_element(by=By.ID, value='username')
    email_field.send_keys(email)
    print('- Finish keying in email')

    password_field = driver.find_element(by=By.ID, value='password')
    password_field.send_keys(password)
    print('- Finish keying in password')
    # Task 1.2: Click the Login button
    password_field.send_keys(Keys.RETURN)
    # print('- Finish Task 1: Login to Linkedin')
    sleep(2)
    
    return '- Finish Task 1: Login to Linkedin'

def getPeople(driver, search_key):
    search_div = driver.find_element(by=By.ID, value='global-nav-search')
    search_button = search_div.find_element(by=By.CLASS_NAME, value='search-global-typeahead__collapsed-search-button')
    search_button.click()
    search_field=  search_div.find_element(by=By.TAG_NAME, value='input')
    sleep(2)

    # Task 2.2: Input the search query to the search bar
    search_field.send_keys(search_key)
    search_field.send_keys(Keys.RETURN)
    sleep(2)

    # Task 2.3: Filter that shows the related peoples only
    filter_selection = driver.find_element(by=By.CLASS_NAME, value='search-reusables__filters-bar-grouping')
    filtered = filter_selection.find_elements(by=By.TAG_NAME, value='li')
    people = filtered[1].click()
    sleep(1)
    print('- Finish Task 2: Search for profiles')

    return people

def getUrl(driver):
    # list_profile = driver.find_element(by=By.CLASS_NAME, value=class_name)
    profiles = driver.find_elements(by=By.CSS_SELECTOR, value='ul > li > div > div > div > div > div > a')
    all_profile_URL = []
    for profile in profiles:
        profile_URL = profile.get_attribute('href')
        if profile_URL not in all_profile_URL and 'https://' in profile_URL and '.com/' in profile_URL and '?miniProfileUrn=' in profile_URL:
            all_profile_URL.append(profile_URL)
            print(f"- Process this link : {profile_URL}")
    return all_profile_URL

def getSkills(driver):
    skills = []
    i = 1
    action_driver = ActionChains(driver)

    # Wait for the <span> element that contains "skills" to be present
    wait = WebDriverWait(driver, 7)
    # skills_span = driver.find_element(By.XPATH, "//h2/span[1][text()='Skills']")
    skills_span = wait.until(EC.presence_of_element_located((By.XPATH, "//h2/span[1][text()='Skills']")))

    # Traverse up to the section (adjust the number of parent steps as needed)
    parent_section = skills_span.find_element(By.XPATH, "./ancestor::section") # This gets the closest parent <section>
    action_driver.scroll_to_element(parent_section).perform()

    skill_button = parent_section.find_element(by=By.CLASS_NAME, value='pvs-list__footer-wrapper')
    skill_button.click()
    sleep(2)
    list_skill = driver.find_elements(by=By.CSS_SELECTOR, value='main > section > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div > ul > li')
    print(f"- len of list_skills = {len(list_skill)} ")
    for skill in list_skill:
        detail = skill.find_element(by=By.TAG_NAME, value='span').text
        if detail not in skills:
            # print(f"- Skills No.{i} : {detail}\n")
            skills.append(detail)
        i += 1
        
    all_skill = str(','.join(skills))
    return all_skill