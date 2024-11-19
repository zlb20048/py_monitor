import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def gerrit_merge_time():
    return int(config.get("gerrit", 'time'))


def get_gerrit_ignore():
    return config.get("gerrit", 'ignore_name').split(",")


def get_jenkins_url():
    return config.get("jenkins", "jenkins_url")

def get_user_name():
    return config.get("user_name", "user_name")

def get_jenkins_token():
    return config.get("pwd", "jenkins_token")

def get_jenkins_api_token():
    return config.get("pwd", "jenkins_api_token")
