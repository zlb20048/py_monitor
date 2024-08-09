from common_jenkins_monitor import monitor_build_status
from datetime import datetime
import robot_send_msg
from loguru import logger


def _report_failed_message(data):
    dt_object = datetime.fromtimestamp(data["timestamp"] / 1000.0)
    current_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    report_content = [
        [{"tag": "text", "text": "oh, No, 失败了!!!"}],
        [{"tag": "text", "text": "失败原因: {}".format(data["result"])}],
        [{"tag": "text", "text": "编译时间: {}".format(current_time)}],
        [{"tag": "text", "text": "失败地址: {}".format(data["url"])}],
    ]
    return report_content


class JenkinsMonitor:
    def __init__(self, name, url, actions, feishu_webhook_list):
        self.name = name
        self.url = url
        self.actions = actions
        self.feishu_webhook_list = feishu_webhook_list

    def start_monitor(self):
        # 在这里编写启动监控的逻辑，使用 self.name、self.url、self.success_message、self.failure_message
        # logger.info("start monitor --> {}".format(self.url))
        monitor_build_status(self.url, self.name, self.success_message, self.failure_message)

    def is_need_send(self, data):
        if self.actions is None:
            return True
        for action in data.get('actions', []):
            if action.get('_class') == 'hudson.model.ParametersAction':
                parameters = action.get('parameters', [])
                for parameter in parameters:
                    for condition in self.actions:
                        if condition.get('name') == parameter.get('name'):
                            value = parameter.get('value')
                            logger.debug("version_type_value --> {}".format(value))
                            if value != condition.get('value'):
                                return False
        return True

    def success_message(self, data):
        if self.is_need_send(data):
            build_url = data["url"]
            artifact_url = build_url + "artifact/"
            dt_object = datetime.fromtimestamp(data["timestamp"] / 1000.0)
            current_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            # 增加不同的artifact的判断
            if "PRJ_HMTC_QNX" in self.url:
                artifact_url = f"http://10.10.96.167:8080/PRJ_HMTC_QNX/{data['number']}"

            report_content = [
                [{"tag": "text", "text": "恭喜你，版本编译成功啦"}],
                [{"tag": "text", "text": "编译时间: {}".format(current_time)}],
                [{"tag": "text", "text": "编译链接: {}".format(build_url)}],
                [{"tag": "text", "text": "产物链接: {}".format(artifact_url)}],
            ]
            for feishu_webhook in self.feishu_webhook_list:
                # 判断是否需要发送机器人消息
                logger.info("need_send_message{}, send To: {}".format(feishu_webhook["need_send_message"],
                                                                      feishu_webhook["tag"]))
                if feishu_webhook["need_send_message"]:
                    robot_send_msg.send_robot_notify("版本编译成功", report_content, feishu_webhook['robot_url'],
                                                     feishu_webhook['robot_key'])

    def failure_message(self, data):
        if self.is_need_send(data):
            error_content = _report_failed_message(data)
            for feishu_webhook in self.feishu_webhook_list:
                # 判断是否需要发送机器人消息
                logger.info("need_send_message{}, send To: {}".format(feishu_webhook["need_send_message"],
                                                                      feishu_webhook["tag"]))
                if feishu_webhook["need_send_message"]:
                    robot_send_msg.send_robot_notify("版本编译失败", error_content, feishu_webhook['robot_url'],
                                                     feishu_webhook['robot_key'])
