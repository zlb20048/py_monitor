import app_config
from JiraMonitor import JiraMonitor


def build_jira_monitors():
    # 读取配置文件，并发起监控
    jira_config = app_config.get_jira_configs()
    monitors = []
    for jira_data in jira_config:
        jira_project_name = jira_data['name']
        jira_project = jira_data['project']
        jira_condition = jira_data['condition']
        feishu_webhook_list = jira_data['feishu_robot']
        monitor = JiraMonitor(
            name=jira_project_name,
            condition=jira_condition,
            project=jira_project,
            feishu_webhook_list=feishu_webhook_list,
        )
        monitors.append(monitor)
    return monitors


jira_monitors = build_jira_monitors()


def do_monitor():
    for jira_monitor in jira_monitors:
        jira_monitor.start_monitor()


# if __name__ == '__main__':
#     do_monitor()
