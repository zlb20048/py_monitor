import re
from loguru import logger


def get_qfil_package_url(data):
    jenkins_url = data['url']
    qfil_package_url = ""
    for artifact in data["artifacts"]:
        if artifact["displayPath"].startswith("QFIL"):
            qfil_package_url = jenkins_url + "artifact/" + artifact["relativePath"]
            break
    logger.debug("qfil_package_url\n      {}", qfil_package_url)
    return qfil_package_url


def get_udisk_package_url(data):
    jenkins_url = data['url']
    udisk_package_url = ""
    for artifact in data["artifacts"]:
        if artifact["displayPath"].startswith("update-factory-xbl"):
            udisk_package_url = jenkins_url + "artifact/" + artifact["relativePath"]
            break
    logger.debug("udisk_package_url\n      {}", udisk_package_url)
    return udisk_package_url


def get_mcu_package_url(data):
    jenkins_url = data['url']
    mcu_package_url = ""
    for artifact in data["artifacts"]:
        if artifact["displayPath"].startswith("update-mcu"):
            mcu_package_url = jenkins_url + "artifact/" + artifact["relativePath"]
            break
    logger.debug("mcu_package_url\n      {}", mcu_package_url)
    return mcu_package_url


def get_package_name_from_url(package_url):
    package_name = re.search(r"\/([^\/]+\.zip)$", package_url).group(1)
    logger.debug("package_name             {}", package_name)
    return package_name

