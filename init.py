import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from datetime import datetime

debug = True
load_dotenv()
os.environ['WDM_LOCAL'] = '1'

options = EdgeOptions()
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

driver.get("https://ems.colorado.edu/Default.aspx")

sign_in_button = driver.find_element(By.XPATH, '//*[@id="pc_HomeHelp"]/b')

sign_in_button.click()

##TODO:Add Wait
username = driver.find_element(By.XPATH, '//*[@id="username"]')
password = driver.find_element(By.XPATH, '//*[@id="password"]')

if debug:
    username.send_keys(os.environ('USERNAME'))
    password.send_keys(os.environ('PASSWORD'))

##TODO:Ask username and password
else:
    pass

login_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/form/div[3]/button[1]')
login_button.click()

WebDriverWait(driver=driver, timeout=2).until(
    lambda d: d.find_element(By.XPATH, '/html/body/form/div[6]/div[1]/ul/li[2]/a'))
create_reservation_button = driver.find_element(By.XPATH, '/html/body/form/div[6]/div[1]/ul/li[2]/a')
create_reservation_button.click()

rec_court_book_now_button = driver.find_element(By.XPATH, '//*[@id="templates-grid"]/div/div[16]/div[2]/button[1]')
rec_court_book_now_button.click()

##TODO: Learn XPath
##TODO: Possible place that code might break
##TODO: Where are the funcking try/catches
## Time 6:00 AM to 11:30 PM

# current_date_time = datetime.now(tz=ZoneInfo('America/Denver'))
# current_date = current_date_time.date()


date_input = driver.find_element(By.XPATH, '//*[@id="booking-date-input"]')
# date_input.clear()
# date_input.send_keys(current_date.strftime('%a %m/%d/%Y'))

date_value = date_input.get_property('value')
start_time = driver.find_element(By.XPATH, '//*[@id="booking-start"]/input')
end_time = driver.find_element(By.XPATH, '//*[@id="booking-end"]/input')

search_button = driver.find_element(By.XPATH, '//*[@id="location-filter-container"]/div[2]/button')
search_button.click()

WebDriverWait(driver=driver, timeout=2).until(
    lambda d: d.find_element(By.XPATH, '//*[@id="book-grid-container"]/div[2]/div/div[2]/div[4]'))

room_2884_element = driver.find_element(By.XPATH, '//*[@id="book-grid-container"]/div[2]/div/div[2]/div[4]')
room_2875_element = driver.find_element(By.XPATH, '//*[@id="book-grid-container"]/div[2]/div/div[2]/div[5]')

room_2884_events = room_2884_element.find_elements(By.CLASS_NAME, 'event-container')
room_2875_events = room_2875_element.find_elements(By.CLASS_NAME, 'event-container')


def get_time_ranges(events):
    time_ranges = set()

    for event in events:
        event.click()
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="booking-details-modal"]/div[1]/div/div[1]/button')))
        close_button.click()

    return


room_2884_reserved_time_ranges = get_time_ranges(room_2884_events)

room_2875_reserved_time_ranges = get_time_ranges(room_2875_events)

# badminton_room_elements = {
#     2884 : None,
#     2875: None
# }

# //*[@id="book-grid-container"]/div[2]/div/div[2]/div[5]


# list_button = driver.find_element(By.XPATH,'//*[@id="result-tabs"]/li[1]/a')
# list_button.click()
# driver.quit()

# table = driver.find_element(By.XPATH,'//*[@id="available-list"]')
