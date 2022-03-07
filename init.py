import os
from this import d
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

os.environ['WDM_LOCAL'] = '1'

options = EdgeOptions()
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=options)

driver.quit()

