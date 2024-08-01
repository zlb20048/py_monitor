import requests
import json

# 替换为你的App ID和App Secret
app_id = "cli_a62369ab46f31013"
app_secret = "6zkoNTYmQjfbtfxHcBSwLgtqjJvkfUeW"


# 获取访问令牌
def get_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json().get("app_access_token")


# 监听消息
def listen_messages(access_token):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.get(url, headers=headers)
    return response.json()


# 获取访问令牌
access_token = get_access_token(app_id, app_secret)

# 获取消息
messages = listen_messages(access_token)
print(messages)
