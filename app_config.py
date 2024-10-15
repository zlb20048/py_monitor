import json
import os


def read_config():
    with open('config.json', 'r') as f:
        data = json.load(f)
        return data


config = read_config()


def get_sleep_time():
    return config['app']['sleep_time']


def get_jenkins_configs():
    return config['jenkins']


def get_jira_configs():
    return config['jira']


def get_work_configs():
    return config['work']

def get_gerrit_check_count():
    return config['gerrit_config']['check_count']


def get_gerrit_ignore():
    print("ignore list --> {}".format(config['gerrit_config']['project']))
    return config['gerrit_config']['project']


def get_gerrit_control_project():
    return config['gerrit_config']['manager_project']


if __name__ == '__main__':
    # ignore_list = get_gerrit_ignore()
    # for ignore_name in ignore_list:
    #     print("ignore name --> {}".format(ignore_name['name']))
    manager_projects = get_gerrit_control_project()
    for project in manager_projects:
        print("project name --> {}".format(project["project_name"]))
        app_configs = project["project_config"]
        for app_config in app_configs:
            print("app config --> {}".format(app_config))
