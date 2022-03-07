import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from zoneinfo import ZoneInfo
from datetime import datetime

os.environ['WDM_LOCAL'] = '1'

options = EdgeOptions()
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=options)

driver.get("https://ems.colorado.edu/Default.aspx")

sign_in_button = driver.find_element(By.XPATH, '//*[@id="pc_HomeHelp"]/b')

sign_in_button.click()

username = driver.find_element(By.XPATH,'//*[@id="username"]')
password = driver.find_element(By.XPATH,'//*[@id="password"]')

username.send_keys("huja4688")
password.send_keys("buff@Devi09")

login_button = driver.find_element(By.XPATH,'/html/body/div/div[1]/div/div[1]/form/div[3]/button[1]')
login_button.click()

WebDriverWait(driver=driver,timeout=2).until(lambda d :d.find_element(By.XPATH,'/html/body/form/div[6]/div[1]/ul/li[2]/a'))
create_reservation_button = driver.find_element(By.XPATH,'/html/body/form/div[6]/div[1]/ul/li[2]/a')
create_reservation_button.click()





rec_court_book_now_button = driver.find_element(By.XPATH,'//*[@id="templates-grid"]/div/div[16]/div[2]/button[1]')
rec_court_book_now_button.click()


##TODO: Possible place that code might break
current_date_time = datetime.now(tz=ZoneInfo('America/Denver'))
current_date = current_date_time.date()



date_input = driver.find_element(By.XPATH,'//*[@id="booking-date-input"]')
date_input.clear()
date_input.send_keys(current_date.strftime('%a %m/%d/%Y'))




# driver.quit()
