import requests

# 替换为你的Webhook URL
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEBHOOK_KEY"

def send_message(text):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    return response.json()

# 发送消息
response = send_message("Hello, 企业微信群!")
print(response)
