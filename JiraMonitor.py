from jira import JIRA
from loguru import logger
import robot_send_msg

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# 设置JIRA的URL和凭证
jira_url = "http://10.10.2.208:8080/"
username = "zixiangliu"
api_token = "Lzx19880328pa"


class JiraMonitor:
    def __init__(self, name, project, condition, feishu_webhook_list):
        self.name = name
        self.condition = condition
        self.project = project
        self.feishu_webhook_list = feishu_webhook_list

    def success_message(self, report_content):
        for feishu_webhook in self.feishu_webhook_list:
            # 判断是否需要发送机器人消息
            logger.info("need_send_message: {}, send To: {}".format(feishu_webhook["need_send_message"],
                                                                    feishu_webhook["tag"]))
            if feishu_webhook["need_send_message"]:
                logger.info("send message to robot")
                # 确保 robot_send_msg 已定义
                robot_send_msg.send_robot_notify("超时任务检测机器人", report_content, feishu_webhook['robot_url'],
                                                 feishu_webhook['robot_key'])

    def monitor(self):
        # 连接到JIRA
        jira = JIRA(jira_url, basic_auth=(username, api_token))

        # 使用JQL查询
        jql_query = self.condition
        fields = 'summary, status, assignee'
        issues = jira.search_issues(jql_query, maxResults=100000, fields=fields)
        jira_browser_url = jira.server_url + "/browse"
        logger.info("jira_browser_url --> {}", jira_browser_url)
        logger.info("issues count --> {}".format(len(issues)))
        # 打印超时任务信息
        if len(issues) != 0:
            report_content = [
                [{"tag": "text", "text": "请大家及时更新下列的超时任务"}],
                [{"tag": "at", "user_id": "all", "user_name": "所有人"}],
                [{"tag": "text", "text": ""}],
            ]
        else:
            report_content = [
                [{"tag": "text", "text": "恭喜大家，本次没有任何超时任务"}],
                [{"tag": "at", "user_id": "all", "user_name": "所有人"}],
                [{"tag": "text", "text": ""}],
            ]
        for issue in issues:
            assignee = issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
            print(f"{issue.key}: {issue.fields.summary}, {assignee}")
            message = [{"tag": "text", "text": f"{issue.fields.summary}, {assignee}"}]
            report_content.append([{"tag": "text", "text": ""}])
            report_content.append(message)
            message = [{"tag": "text", "text": f"{jira_browser_url}/{issue.key}"}]
            report_content.append(message)
        self.success_message(report_content)

    def do_scheduler_job(self):
        scheduler.add_job(self.monitor, 'cron', hour=17, minute=00, day_of_week='mon-sat')
        scheduler.add_job(self.monitor, 'cron', hour=18, minute=00, day_of_week='mon-sat')

        # scheduler.add_job(self.monitor, 'interval', seconds=10)
        logger.info("Scheduler job added")
        scheduler.start()

    def start_monitor(self):
        self.do_scheduler_job()
