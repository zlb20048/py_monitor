from JenkinsMonitor import JenkinsMonitor
import app_config


def build_jenkins_monitor():
    # 读取配置文件，并发起监控
    jenkins_configs = app_config.get_jenkins_configs()
    jenkins_monitors = []
    for jenkins_data in jenkins_configs:
        jenkins_number_name = jenkins_data['name']
        jenkins_url = jenkins_data['url']
        actions = jenkins_data.get("actions")

        feishu_webhook_list = jenkins_data['feishu_robot']
        monitor = JenkinsMonitor(
            name=jenkins_number_name,
            url=jenkins_url,
            actions=actions,
            feishu_webhook_list=feishu_webhook_list,
        )
        jenkins_monitors.append(monitor)
    return jenkins_monitors


monitors = build_jenkins_monitor()


def monitor_jenkins():
    for monitor in monitors:
        monitor.start_monitor()
