import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def gerrit_merge_time():
    return int(config.get("gerrit", 'time'))


def get_gerrit_ignore():
    return config.get("gerrit", 'ignore_name').split(",")


def get_jenkins_url():
    return config.get("jenkins", "jenkins_url")
