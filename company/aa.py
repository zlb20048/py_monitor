from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver (make sure you have the necessary WebDriver installed)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the login page
driver.get('http://210.22.130.125:8990/seeyon/main.do?method=main')

# Fill in the username and password
driver.find_element(By.ID, "login_username").send_keys('zixiangliu')
driver.find_element(By.ID, "login_password").send_keys('123123123123!')

# Submit the form (adjust the submit method as necessary)
driver.find_element(By.ID, "login_button").click()

# Wait for login to complete and navigate to the report page
driver.get('http://210.22.130.125:8990/seeyon/vreport/vReport.do?method=vReportView&portalId=1&_resourceCode=F08_report_view')

# Extract the page content (if needed)
page_content = driver.page_source

# Close the browser
driver.quit()

# Output the page content
print(page_content)
