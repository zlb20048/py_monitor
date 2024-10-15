from PIL.TiffTags import lookup
from loguru import logger
import robot_send_msg
import app_config

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def _build_work_monitors():
    # 读取配置文件，并发起监控
    work_configs = app_config.get_work_configs()
    monitors = []
    for work_data in work_configs:
        feishu_webhook_list = work_data['feishu_robot']
        monitor = WorkMonitor(
            feishu_webhook_list=feishu_webhook_list,
        )
        monitors.append(monitor)
    return monitors

def do_monitor():
    work_monitors = _build_work_monitors()
    for work_monitor in work_monitors:
        work_monitor.start_monitor()


class WorkMonitor:
    def __init__(self, feishu_webhook_list):
        self.feishu_webhook_list = feishu_webhook_list

    def success_message(self, report_content):
        for feishu_webhook in self.feishu_webhook_list:
            # 判断是否需要发送机器人消息
            logger.info("need_send_message: {}, send To: {}".format(feishu_webhook["need_send_message"],
                                                                    feishu_webhook["tag"]))
            if feishu_webhook["need_send_message"]:
                logger.info("send message to robot")
                # 确保 robot_send_msg 已定义
                robot_send_msg.send_robot_notify("工时提醒机器人", report_content, feishu_webhook['robot_url'],
                                                 feishu_webhook['robot_key'])

    def monitor(self):
        report_content = [
            [{"tag": "text", "text": "请大家不要忘记填写工时，已填请忽略"}],
            [{"tag": "at", "user_id": "all", "user_name": "所有人"}],
            [{"tag": "text", "text": ""}],
        ]
        self.success_message(report_content)

    def do_scheduler_job(self):
        scheduler.add_job(self.monitor, 'cron', hour=18, minute=30, day_of_week='mon-sat')
        scheduler.add_job(self.monitor, 'cron', hour=19, minute=30, day_of_week='mon-sat')
        scheduler.add_job(self.monitor, 'cron', hour=20, minute=30, day_of_week='mon-sat')

        # scheduler.add_job(self.monitor, 'interval', seconds=10)
        logger.info("Scheduler job added")
        scheduler.start()


    def start_monitor(self):
        self.do_scheduler_job()