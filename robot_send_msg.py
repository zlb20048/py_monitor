from feishu_webhook import FeiShuBot
from jenkins_artifact_data import JenkinsArtifactData

# 飞书机器人
fsb = FeiShuBot()


# 自动发送消息的机器人


# 机器人统一发送
def send_self_message(title, message):
    # 发送给到自己的机器人
    pub_feishu_webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/069ea72c-0154-4240-9bd9-e42e702a5e05"
    pub_key = "5kC2Sl3pFoi9bDwolplp1c"
    send_robot_notify(title, message, pub_feishu_webhook, pub_key)


def send_card_message_to_self(jenkins_artifact):
    # 发送给到自己的机器人
    pub_feishu_webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/069ea72c-0154-4240-9bd9-e42e702a5e05"
    pub_key = "5kC2Sl3pFoi9bDwolplp1c"
    fsb.send_jenkins_card_message(jenkins_artifact, pub_feishu_webhook, pub_key)


def send_card_message(jenkins_artifact, pub_feishu_webhook, pub_key):
    # 发送给到自己的机器人
    fsb.send_jenkins_card_message(jenkins_artifact, pub_feishu_webhook, pub_key)


# 真实发送数据
def send_robot_notify(title, message, pub_feishu_webhook, pub_key):
    fsb.send_notification(title, message, pub_feishu_webhook, pub_key)


if __name__ == '__main__':
    jenkins_artifact_data = JenkinsArtifactData("11", "22", "33", "44", "恭喜恭喜")
    send_card_message_to_self(jenkins_artifact_data)
