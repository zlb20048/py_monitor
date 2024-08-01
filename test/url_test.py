from urllib.parse import urlparse
from loguru import logger

url = "http://10.10.96.212:8081/425231"

if __name__ == '__main__':
    parsed_url = urlparse(url)
    gerrit_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    ssh_gerrit_url = f"zixiangliu@{parsed_url.hostname}"
    logger.info(f"message --> {parsed_url.hostname}")
    logger.info(f"current gerrit url --> {gerrit_url}, ssh_gerrit_url --> {ssh_gerrit_url}")
