import sys
import time
# my part
import jenkins_project
import gerrit_monitor
from loguru import logger
import app_config
import jira_monitor
from apscheduler.schedulers.background import BackgroundScheduler

import work_tips

scheduler = BackgroundScheduler()

# 移除默认的 stderr 处理器
logger.remove(handler_id=None)

# 配置日志输出到控制台，仅输出 INFO 级别的日志
logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    backtrace=False,  # 关闭堆栈跟踪信息，以避免重复输出
    diagnose=True  # 关闭诊断信息，以避免重复输出
)

jenkins_monitors = jenkins_project.build_jenkins_monitor()


def main():
    jira_monitor.do_monitor()
    work_tips.do_monitor()
    logger.info("start gerrit monitor")
    # scheduler.add_job(tel_bot.do_robot_start)
    # scheduler.start()
    # scheduler.add_job(jenkins_project.monitor_jenkins, "interval", seconds=app_config.get_sleep_time())
    while True:
        # schedule.run_pending()
        # logger.info("run pending")
        # 检测Gerrit
        gerrit_monitor.monitor_gerrit()
        # 检测Jenkins编译
        jenkins_project.monitor_jenkins()
        # 增加延迟监听
        time.sleep(app_config.get_sleep_time())


if __name__ == "__main__":
    main()
