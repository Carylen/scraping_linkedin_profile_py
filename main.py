from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
from time import sleep
from operations_helper import login, getUrl, getPeople, getSkills
import csv

print('- Finish importing package')
result = ''
max_width = 720
max_height = 900
try:
    driver = webdriver.Chrome()
    driver.set_window_size(max_width, max_height)
    login_message = login(driver, 'https://www.linkedin.com/login', 'iirham440@gmail.com', 'Hamza612')
    print(login_message)
    people = getPeople(driver, 'Data Analyst')
    input_page = int(input('How many pages you want to scrape: '))
    URLs_all_page = []
    for page in range(input_page):
        # URLs_one_page = GetURL('GvXnnMieLesgSiMjvOXypGYCDABjCBejdLw.')
        URLs_one_page = getUrl(driver)
        sleep(2)
        URLs_all_page = URLs_all_page + URLs_one_page
        if page > 1:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
            sleep(2)
            next_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-pagination__button--next")
            driver.execute_script("arguments[0].click();", next_button)
            sleep(2)

    print('- Finish Task 3: Scrape the URLs')

    # ------------------------------------------------------------------------------

    # Step 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file

    with open('output_clone.csv', 'w',  newline = '') as file_output:
        headers = ['Name', 'Job Title', 'Location', 'URL', 'SkillSet']
        writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
        writer.writeheader()
        for linkedin_URL in URLs_all_page:
            driver.get(linkedin_URL)
            sleep(2)
            print('- Accessing profile: ', linkedin_URL)
            # Get the Main <div> to get the all of informations like name, position, location
            main_container = driver.find_element(by=By.CLASS_NAME, value='mt2.relative')
            # Get the name of person
            name = main_container.find_element(by=By.TAG_NAME, value='h1').text
            # get the second <div>, then get the first <span> tag to get the value of location
            location = main_container.find_element(by=By.CSS_SELECTOR, value='div:nth-child(1) > span').text
            # Get the job title of the person
            title = main_container.find_element(by=By.CLASS_NAME, value='text-body-medium.break-words').text
            # Get the skill of the person
            all_skill = getSkills(driver)
            sleep(2)
            # all_skill = 'getSkills'
            print('--- Profile name is: ', name)
            print('--- Profile location is: ', location)
            print('--- Profile title is: ', title)
            print('--- Profile skill is: ', all_skill)
            writer.writerow({headers[0]:name.strip(), headers[1]:location.strip(), headers[2]:title.strip(), headers[3]:linkedin_URL, headers[4]:all_skill})
            print('\n')

    print('Mission Completed!')
    result = 'Success'
except Exception as e:
    print(e)
    result = e
    