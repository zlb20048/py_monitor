import configparser

config = configparser.ConfigParser()
config.read('pwd.ini')

def get_user_name():
    return config.get("user_name", "user_name")

def get_jenkins_token():
    return config.get("pwd", "jenkins_token")

def get_jenkins_api_token():
    return config.get("pwd", "jenkins_api_token")

def get_gerrit_pwd():
    return config.get("pwd", "gerrit_pwd")
