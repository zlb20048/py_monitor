import requests
from requests.auth import HTTPBasicAuth

url = 'http://10.10.96.213:8081/a/changes/?q=owner:self%20status:open'


def login(user_id, user_password):
    auth = HTTPBasicAuth(user_id, user_password)
    try:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'GerritAccount=aUceprtIZiOqoLTWAiE0dn1dUGYlsEsaUa',
            'X-Gerrit-Auth': "aUceprtyacx1ebefvZX2QJ1y4HyrO7J0TW",
            "KexAlgorithms": "+diffie-hellman-group1-sha1",
            "sec-ch-ua-platform": "Linux",
            "Remote Address": "10.10.96.212:8081",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, auth=auth, verify=False)
        print(response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        print("Response content:", e.response.content if e.response is not None else None)


if __name__ == '__main__':
    login("zixiangliu", "1234556")
