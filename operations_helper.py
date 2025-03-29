from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
    sleep(1)
    
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
    sleep(4)

    # Task 2.3: Filter that shows the related peoples only
    filter_selection = driver.find_element(by=By.CLASS_NAME, value='search-reusables__filters-bar-grouping')
    filtered = filter_selection.find_elements(by=By.TAG_NAME, value='li')
    people = filtered[2].click()
    sleep(3)
    print('- Finish Task 2: Search for profiles')

    return people

def getUrl(driver):
    # list_profile = driver.find_element(by=By.CLASS_NAME, value=class_name)
    profiles = driver.find_elements(by=By.CSS_SELECTOR, value='ul > li > div > div > div > div > div > a')
    all_profile_URL = []
    for profile in profiles:
        profile_URL = profile.get_attribute('href')
        # profile_URL = "https://www.linkedin.com" + profile_ID
        if profile_URL not in all_profile_URL and 'https://' in profile_URL and '.com/' in profile_URL and '?miniProfileUrn=' in profile_URL:
            all_profile_URL.append(profile_URL)
            print(f"- Process this link : {profile_URL}")
    return all_profile_URL

def getSkills(driver):
    all_skills = []
    main_section = driver.find_element(by=By.TAG_NAME, value='main')
    inner_main_section = main_section.find_elements(by=By.TAG_NAME, value='li')
    skill_section = inner_main_section[6].click()
    sleep(2)
    # main_section_skill = driver.find_element(by=By.TAG_NAME, value='main')
    # list_skill = main_section_skill.find_element(by=By.TAG_NAME, value='ul')
    list_skill = driver.find_elements(by=By.CSS_SELECTOR, value='main > section > div:nth-child(1) > div:nth-child(1) > div > div > div > ul > li')
    for skill in list_skill:
        detail = skill.find_element(by=By.TAG_NAME, value='span').text
        if detail not in all_skills:
            all_skills.append(detail)
        