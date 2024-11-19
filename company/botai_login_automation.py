# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check if selenium is installed, if not, install it
try:
    import selenium
except ImportError:
    print("Selenium not found. Installing...")
    install("selenium")
    import selenium

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Firefox driver
driver = webdriver.Chrome()

# Open Botai website
driver.get("http://210.22.130.125:8990/seeyon/main.do")

# Wait for username input field to load
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login_username"))
)

# Input username
username_input.send_keys("zixiangliu")

# Find password input field and enter password
password_input = driver.find_element(By.ID, "login_password")
password_input.send_keys("123123123!")

# Find login button and click
login_button = driver.find_element(By.ID, "login_button")
login_button.click()

# Wait for page to load (assuming login redirects to a page with a specific element)
# Note: Replace 'some_element_id_on_logged_in_page' with an actual element ID on the logged-in page
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "some_element_id_on_logged_in_page"))
)

print("Login successful!")

# Wait for the report center element to be clickable
report_center = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'报表中心')]"))
)

# Create ActionChains object to handle mouse hover
actions = ActionChains(driver)

# Move the mouse to the "report center" element (hover)
actions.move_to_element(report_center).perform()

# Wait for the report analysis element to be clickable
report_analysis = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'报表分析')]"))
)

# Wait for the submenu to become visible after hovering
submenu_item = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "报表分析"))  # Adjust selector based on actual HTML structure
)

# Click on the report analysis
submenu_item.click()

print("Navigated to Report Analysis!")

# Add more operations here if needed

# Close the browser when done (uncomment the line below to enable)
# driver.quit()
