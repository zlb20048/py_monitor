import requests
from requests.auth import HTTPBasicAuth

# URLs
url_login = "http://210.22.130.125:8990/seeyon/main.do?method=main"
url_report = "http://210.22.130.125:8990/seeyon/vreport/vReport.do?method=vReportView&portalId=1&_resourceCode=F08_report_view"

# Replace with your actual credentials
username = 'zixiangliu'
password = '1231243141'

# Create a session to persist cookies
session = requests.Session()

# Log in using Basic Authentication
response = session.get(url_login, auth=HTTPBasicAuth(username, password))

# Check if login was successful and extract any tokens or session information if necessary
if response.status_code == 200:
    print("Login Success")

    # Check if CSRF token or any other form field is required
    # You might need to parse the HTML to get the token if it's embedded
    # For example, if you find a hidden CSRF token:
    # csrf_token = extract_token_from_html(response.text) # Example function

    # Make sure to include any required headers, such as CSRF tokens or custom headers
    headers = {
        'Authorization': f'Bearer {username}',  # Example, modify as needed
        # 'X-CSRF-Token': csrf_token  # Add this if you find a CSRF token
    }

    # Now make the second request using the same session (which carries the cookies)
    response = session.get(url_report, headers=headers)

    # Check if the request for the report was successful
    if response.status_code == 200:
        print("Report Success:", response.text)
    else:
        print(f"Failed to retrieve report with status code {response.status_code}")
else:
    print(f"Login failed with status code {response.status_code}")
