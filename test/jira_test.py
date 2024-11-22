import requests
from requests.auth import HTTPBasicAuth
from jira import JIRA
import gerrit_config

url = 'http://10.10.2.208:8080/secure/Dashboard.jspa?selectPageId=15422'


def login(user_id, user_password):
    auth = HTTPBasicAuth(user_id, user_password)
    try:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, auth=auth, verify=False)
        print(response.status_code)
        print(response.content)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        print("Response content:", e.response.content if e.response is not None else None)




# 设置JIRA的URL和凭证
jira_url = "http://10.10.2.208:8080/"
username = gerrit_config.get_user_name()
api_token = gerrit_config.get_jenkins_token()

# 连接到JIRA
jira = JIRA(jira_url, basic_auth=(username, api_token))
print(f"jira_url --> {jira.server_url}")
# 使用JQL查询
jql_query = 'project = M116 AND assignee in (zixiangliu)'
issues = jira.search_issues(jql_query)

# 打印问题信息
for issue in issues:
    print(f"{issue.key}: {issue.fields.summary}")
