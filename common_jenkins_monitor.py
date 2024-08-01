# common_jenkins_monitor.py

import datetime
import jenkins_api

from datetime import datetime
from loguru import logger
from db import orm_db


def monitor_build_status(
        job_url, jenkins_number_name, success_message, failure_message
):
    # for debug url
    # logger.info("job_url: {}", job_url)
    latest_build_url = jenkins_api.get_latest_build_url(job_url)
    # logger.info("latest_build_url: {}", latest_build_url)
    if latest_build_url is None:
        return
    jenkins_data = orm_db.get_jenkins_data(jenkins_number_name)
    # logger.info("jenkins_data: {}", jenkins_data)
    if jenkins_data is None:
        present_url = ""
    else:
        present_url = jenkins_data.url
    # logger.info("present_url: {}", present_url)
    # logger.info("latest_build_url: {}", latest_build_url)

    if present_url == latest_build_url:
        return

    data = jenkins_api.get_latest_build_data(latest_build_url)
    if data is None:
        logger.error("Failed to get build status.")
    else:
        if not data["building"]:
            orm_db.save_jenkins_data(jenkins_number_name, latest_build_url)
            if data["result"] == "SUCCESS":
                logger.info("Job is build success ... send feishu notify")
                success_message(data)
            else:
                logger.error("build failed")
                failure_message(data)



