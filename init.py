import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utilities import get_available_slot
from datetime import datetime, timedelta


def element_to_be_located(locator):
    """ An expectation for checking if the given element is clicked in the
    specified place after the page has been refreshed.
    """
    def _predicate(driver_main):
        try:
            driver_main.find_element(*locator).click()
            return True
        except StaleElementReferenceException:
            return False

    return _predicate

def initial_setup():
    global driver, predefined_range, contact_name, phone_number, email_address

    debug = True
    load_dotenv()
    os.environ['WDM_LOCAL'] = '1'
    options = EdgeOptions()
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get("https://ems.colorado.edu/Default.aspx")
    sign_in_button = driver.find_element(By.XPATH, '//*[@id="pc_HomeHelp"]/b')
    sign_in_button.click()
    username = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
    if debug:
        username.send_keys(os.environ['USERNAME'])
        password.send_keys(os.environ['PASSWORD'])
        predefined_range = [os.environ['START_PREFERENCE'], os.environ['END_PREFERENCE']]
        contact_name = os.environ['CONTACT_NAME']
        phone_number = os.environ['CONTACT_NUMBER']
        email_address = os.environ['CONTACT_EMAIL']
    # TODO:  Add ArgParse
    else:
        username = input('Please provide your username\n')
        password = input('Please provide your password\n')
    login_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/form/div[3]/button[1]')
    login_button.click()
    WebDriverWait(driver=driver, timeout=2).until(
        lambda d: d.find_element(By.XPATH, '/html/body/form/div[6]/div[1]/ul/li[2]/a'))
    create_reservation_button = driver.find_element(By.XPATH, '/html/body/form/div[6]/div[1]/ul/li[2]/a')
    create_reservation_button.click()
    rec_court_book_now_button = WebDriverWait(driver=driver, timeout=2).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="templates-grid"]/div/div[16]/div[2]/button[1]'))
    # rec_court_book_now_button = driver.find_element(By.XPATH, '//*[@id="templates-grid"]/div/div[16]/div[2]/button[1]')
    rec_court_book_now_button.click()

def get_time_ranges(events):
    reserved_time_ranges = []

    for event in events:
        try:
            driver.execute_script("arguments[0].click();", event)
            close_button: WebElement = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="booking-details-modal"]/div[1]/div/div[1]/button')))

            reserved_time: WebElement = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="detailsContainer"]/table/tbody/tr/td[contains('
                                                          'string(),"Reserved Time")]/following-sibling::td')))
            reserved_time: str = reserved_time.text
            reserved_time: list[str] = reserved_time.split(' - ')
            reserved_time_ranges.append(reserved_time)
            close_button.click()
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="booking-details-modal"]')))
            # TODO: Incorrect Usage
            # time.sleep(2)
        except TimeoutException as exception:
            print(exception.msg)
        except ElementClickInterceptedException as exception:
            print(exception.msg)
        except ElementNotInteractableException as exception:
            print(exception.msg)
    return reserved_time_ranges


def increment_date_and_reset_time():
    date_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="booking-date-input"]')))
    curr_date = date_input.get_property('value')
    curr_date = datetime.strptime(curr_date, '%a %m/%d/%Y')
    next_date = curr_date + timedelta(days=1)
    date_input.clear()
    date_input.send_keys(next_date.strftime('%a %m/%d/%Y'))
    return


def book_room(available_slot_inside, start_time_element_inside, end_time_element_inside, index, phone_number_inside,
              email_address_inside,
              contact_name_inside):
    start_time_element_inside.clear()
    start_time_element_inside.send_keys(available_slot_inside['start_time'])
    end_time_element_inside.clear()
    end_time_element_inside.send_keys(available_slot_inside['end_time'])
    search_button_inside = driver.find_element(By.XPATH, '//*[@id="location-filter-container"]/div[2]/button')
    # driver.execute_script("arguments[0].click();", search_button_inside)
    search_button_inside.click()
    search_button_inside.click()
    WebDriverWait(driver, 5).until(
        element_to_be_located((By.XPATH,
                               f'//*[@id="book-grid-container"]/div[2]/div/div[1]/div/div[contains(string(),'
                               f'"Badminton_Pickleball {index + 1}")][1]/a[1]')))
    # TODO: Check for Popups
    next_step_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="next-step-btn"]')))
    next_step_button.click()

    contact_name_field: WebElement = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="1stContactName"]')))
    contact_name_field.send_keys(contact_name_inside)

    contact_phone_field: WebElement = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="1stContactPhone1"]')))
    contact_phone_field.send_keys(phone_number_inside)

    contact_email_field: WebElement = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="1stContactEmail"]')))
    contact_email_field.send_keys(email_address_inside)

    additional_info_1 = Select(WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '// *[ @ id = "165"]'))))
    additional_info_1.select_by_value('471')
    additional_info_2 = Select(WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="164"]'))))
    additional_info_2.select_by_value('470')

    reserve_button: WebElement = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="details"]/div[3]/div/span[2]/button')))
    reserve_button.click()

    return


def reserve_from_reservation_page():
    search_button = driver.find_element(By.XPATH, '//*[@id="location-filter-container"]/div[2]/button')
    search_button.click()
    WebDriverWait(driver=driver, timeout=2).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="book-grid-container"]/div[2]/div/div[2]/div[4]'))
    room_2884_element = driver.find_element(By.XPATH, '//*[@id="book-grid-container"]/div[2]/div/div[2]/div[4]')
    room_2875_element = driver.find_element(By.XPATH, '//*[@id="book-grid-container"]/div[2]/div/div[2]/div[5]')
    room_2884_events = room_2884_element.find_elements(By.CLASS_NAME, 'event-container')
    room_2875_events = room_2875_element.find_elements(By.CLASS_NAME, 'event-container')
    room_2884_reserved_time_ranges = get_time_ranges(room_2884_events)
    room_2875_reserved_time_ranges = get_time_ranges(room_2875_events)
    rooms = [room_2884_reserved_time_ranges, room_2875_reserved_time_ranges]
    start_time_element = driver.find_element(By.XPATH, '//*[@id="booking-start"]/input')
    end_time_element = driver.find_element(By.XPATH, '//*[@id="booking-end"]/input')
    curr_time = start_time_element.get_property('value')
    for i in range(len(rooms)):
        available_slots = get_available_slot(rooms[i], predefined_range[:], curr_time)
        if len(available_slots) > 0:
            book_room(available_slots[0], start_time_element, end_time_element, i, phone_number, email_address,
                      contact_name)
            return
    else:
        print('No available slots to book')
        return


# TODO:Learn XPath
# TODO:Possible place that code might break
# TODO:Where are the fucking try/catches
# TODO:Time 6:00 AM to 11:30 PM
# TODO:Hard-Coding Max
# TODO:current_date_time = datetime.now(tz=ZoneInfo('America/Denver'))
# TODO:current_date = current_date_time.date()

initial_setup()
reserve_from_reservation_page()
increment_date_and_reset_time()
reserve_from_reservation_page()
driver.quit()
