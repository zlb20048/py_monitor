import requests
import jenkins_trigger
from db import orm_db
from loguru import logger

# app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '7199212814:AAHusMVs824orJGJzaMMVv5JJOMIe_dKT_g'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'
# curl -F "url=" https://api.telegram.org/bot7199212814:AAHusMVs824orJGJzaMMVv5JJOMIe_dKT_g/deleteWebhook
# 定义代理
proxies = {
    'http': 'http://localhost:17890',
    'https': 'http://localhost:17890'
}


def get_updates(offset=None):
    url = f'{TELEGRAM_API_URL}/getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params, proxies=proxies)
    logger.info(f"data --> ${response.json()}")
    return response.json()


def send_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload, proxies=proxies)


def do_robot_start():
    offset = orm_db.get_jenkins_build_update_id()
    logger.info(f"offset --> {offset}")
    try:
        updates = get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']

                # 此处解析Message，然后进行相关的触发动作
                if message_text in "8295编译":
                    # 触发8295 App 编译
                    jenkins_trigger.build_8295_app()

                # 根据消息内容执行操作
                if message_text == '/start':
                    send_message(chat_id, '欢迎使用我们的服务！')
                else:
                    send_message(chat_id, f'你发送了: {message_text}')

                # 更新offset以防止重复获取相同的消息
                orm_db.save_jenkins_build_update_id(update['update_id'] + 1, "")
    except Exception as e:
        logger.error(e)
    finally:
        do_robot_start()


if __name__ == '__main__':
    do_robot_start()
