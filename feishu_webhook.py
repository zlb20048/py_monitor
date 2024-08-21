import json
from loguru import logger
import time

import requests
import urllib3
import yaml
from jenkins_artifact_data import JenkinsArtifactData

urllib3.disable_warnings()

import hashlib
import base64
import hmac

# important!
feishu_webhook = (
    "https://open.feishu.cn/open-apis/bot/v2/hook/069ea72c-0154-4240-9bd9-e42e702a5e05"
)


def load_yaml(config_file):
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
            return config
    except Exception as e:
        print(str(e))

    return None


try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


def gen_sign(timestamp, key):
    # 拼接timestamp和secret
    # secret = "l8romj5jtqr9PAE0hmQiGe"
    string_to_sign = "{}\n{}".format(timestamp, key)
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


class FeiShuBot(object):
    def __init__(self):
        """
        机器人初始化
        :param webhook: 飞书群自定义机器人webhook地址
        :param secret: 机器人安全设置页面勾选“加签”时需要传入的密钥
        :param pc_slide: 消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
        :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理
        """
        super(FeiShuBot, self).__init__()
        self._headers = {"Content-Type": "application/json; charset=utf-8"}

    def _post(self, webhook, data):
        self._web_hook = webhook
        if self._web_hook is None:
            logger.warning("no valid web_hook or chat_group is selected")
            return

        try:
            post_data = json.dumps(data)
            logger.info("post_data --> " + post_data)
            response = requests.post(
                self._web_hook, headers=self._headers, data=post_data, verify=False
            )
            logger.info("response --> " + response.text)
        except requests.exceptions.HTTPError as exc:
            logger.error(
                "消息发送失败， HTTP error: %d, reason: %s"
                % (exc.response.status_code, exc.response.reason)
            )
            raise
        except requests.exceptions.ConnectionError:
            logger.error("消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            logger.error("消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            logger.error("消息发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except JSONDecodeError:
                logger.error(
                    "服务器响应异常，状态码：%s，响应内容：%s" % (response.status_code, response.text)
                )
                return {"errcode": 500, "errmsg": "服务器响应异常"}
            else:
                # logger.debug("发送结果：%s" % result)
                return result

    # -----------------public function-----------------
    # l8romj5jtqr9PAE0hmQiGe

    def send_notification(self, title, report_content, webhook, webhook_key):
        logger.info("send_notification title " + title + " report_content {}".format(report_content))

        # get sign
        timestamp = int(time.time())
        sign = gen_sign(timestamp, webhook_key)

        self._post(
            webhook,
            {
                "timestamp": timestamp,  # 时间戳。
                "sign": sign,  # 得到的签名字符串。
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": report_content,
                        }
                    }
                },
            },
        )

    def send_jenkins_card_message(self, jenkins_artifact: JenkinsArtifactData, webhook, webhook_key):
        logger.info("send_jenkins_card_message " + jenkins_artifact.name)
        # get sign
        timestamp = int(time.time())
        sign = gen_sign(timestamp, webhook_key)
        self._post(
            webhook,
            {
                "timestamp": timestamp,  # 时间戳。
                "sign": sign,  # 得到的签名字符串。
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "content": jenkins_artifact.name,
                            "tag": "lark_md"
                        }
                    },
                    "elements": [{
                        "tag": "div",
                        "text": {
                            "content": jenkins_artifact.build_content,
                            "tag": "lark_md"
                        }
                    },
                        {
                        "tag": "div",
                        "text": {
                            "content": jenkins_artifact.build_time,
                            "tag": "lark_md"
                        }
                    },
                        {
                        "actions": [{
                            "tag": "button",
                            "text": {
                                "content": "编译链接",
                                "tag": "lark_md"
                            },
                            "url": jenkins_artifact.build_url,
                            "type": "default",
                            "value": {}
                        }, {
                            "tag": "button",
                            "text": {
                                "content": "产物下载链接",
                                "tag": "lark_md"
                            },
                            "url": jenkins_artifact.artifact_url,
                            "type": "default",
                            "value": {}
                        }],
                        "tag": "action"
                    },
                    ],
                },
            },
        )

# def job():
#     print("I'm working...")
#     logging.debug("logging say : I'm working...")
#     fsb = FeiShuBot()
#     fsb.send_notification()

# if __name__ == "__main__":

#     schedule.every(5).seconds.do(job)
#     # schedule.every(10).seconds.do(job)
#     # schedule.every(0.25).minutes.do(job)
#     # schedule.every().hour.do(job)
#     # schedule.every().day.at("21:00").do(job)
#     # schedule.every().monday.do(job)
#     # schedule.every().wednesday.at("13:15").do(job)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)
