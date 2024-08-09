# 监听当前的服务器信息
import json

import gerrit_option
import robot_send_msg
import persistent_data as pd
from gerrit_onwer_data import GerritData
from datetime import datetime
from loguru import logger
import app_config
from db import orm_db
from urllib.parse import urlparse

# Gerrit服务器地址
gerrit_url_212 = "zixiangliu@10.10.96.212"
gerrit_url_213 = "zixiangliu@10.10.96.213"

persistent_data = pd.create_persistent_instance("gerrit_data")


def get_owner_data(name):
    owner_data = persistent_data.get_value(name)
    if owner_data is None:
        return None
    return json.loads(owner_data)


def save_owner_data(name, data_list):
    json_string = json.dumps([data.__dict__ for data in data_list], default=lambda o: o.__dict__)
    persistent_data.add_value(name, json_string)


def update_owner_data(name, gerrit_data_list):
    json_string = json.dumps([data.__dict__ for data in gerrit_data_list], default=lambda o: o.__dict__)
    persistent_data.update_value(name, json_string)


def process_gerrit_data(unmerge_info, owner_data_list):
    url = unmerge_info["url"]
    convert_data_list = []
    if isinstance(owner_data_list, list):
        convert_data_list = owner_data_list
    else:
        convert_data_list.append(owner_data_list)

    gerrit_data_list = [GerritData(**data) for data in convert_data_list]

    # 判断列表中是否有这条数据
    found = False
    for data in gerrit_data_list:
        if data.url == url:
            data.count += 1
            found = True

    if not found:
        # 如果列表中没有相应的数据，则添加新数据
        new_data = GerritData(url=url, count=1, time=datetime.fromtimestamp(unmerge_info['createdOn']).strftime(
            "%Y-%m-%d %H:%M:%S"))
        gerrit_data_list.append(new_data)

    return gerrit_data_list


def load_app_config(project_name, branch):
    manager_projects = app_config.get_gerrit_control_project()
    for project in manager_projects:
        if project["project_name"] in project_name:
            app_configs = project["project_config"]
            for app in app_configs:
                if app["ignore_branch"] == branch:
                    return app
    return None


def check_project_in_control(project, branch):
    for project_config in app_config.get_gerrit_ignore():
        if project_config["project_name"] in project:
            if project_config["ignore_branch"] == branch:
                return project_config
    return None


def monitor_gerrit():
    # logger.info("monitor start")
    # 查询已经提交但未被合并的变更
    unmerge_infos_212 = gerrit_option.get_all_un_merge(gerrit_url=gerrit_url_212)
    # logger.info("get 212 unmerge info end")
    unmerge_infos_213 = gerrit_option.get_all_un_merge(gerrit_url=gerrit_url_213)
    # logger.info("get 213 unmerge info end")
    combined_unmerge_infos = unmerge_infos_212 + unmerge_infos_213
    # logger.info("merge info --> {}".format(combined_unmerge_infos))
    for unmerge_info in combined_unmerge_infos:
        if "subject" in unmerge_info:
            subject = unmerge_info["subject"]
            if "commitMessage" in unmerge_info:
                content = unmerge_info["commitMessage"]
            else:
                content = subject
            project = unmerge_info["project"]
            url = unmerge_info["url"]
            time = datetime.fromtimestamp(unmerge_info['createdOn']).strftime(
                "%Y-%m-%d %H:%M:%S")
            branch = unmerge_info['branch']
            name = unmerge_info["owner"]["name"]
            report_content = [
                [{"tag": "text", "text": "提交人:   {}".format(name)}],
                [{"tag": "text", "text": "分支:  {}".format(branch)}],
                [{"tag": "text", "text": "代码地址:  {}".format(url)}],
                [{"tag": "text", "text": "修改内容:  {}".format(content)}],
            ]
            patch_id = unmerge_info["currentPatchSet"]["revision"]
            # 提取Verify是sysadmin的内容
            if 'currentPatchSet' in unmerge_info and 'approvals' in unmerge_info['currentPatchSet']:
                verified_by_sysadmin = [
                    approval for approval in unmerge_info['currentPatchSet']['approvals']
                    if approval['type'] == 'Verified' and approval['by']['username'] == 'sysadmin'
                ]
            else:
                verified_by_sysadmin = []

            parsed_url = urlparse(url)
            gerrit_url = f"zixiangliu@{parsed_url.hostname}"
            logger.info(f"current gerrit url --> {gerrit_url}")

            # 增加数据库存储，然后方便从数据库里面获取更多的数据
            # 新查询数据
            query_result = orm_db.save_gerrit_data(name=name, url=url, time=time, count=1)
            # 记录当前的count数据
            saved_count = query_result.count
            # 如果saved_count --> 1 机器人提示 + verify_code
            logger.info(f"url --> {url}\n\t\t\t\t name --> {name}，count --> {saved_count}")
            logger.info(f"project --> {project}")
            if saved_count == 1:
                # 给出提示信息
                orm_db.analyze_user_commit()
                verify(gerrit_url, patch_id=patch_id)
                robot_send_msg.send_self_message(subject, report_content)
                # 最后打印信息
            else:
                # 存在数据,则需要更新count
                if saved_count < app_config.get_gerrit_check_count():
                    continue
                app = load_app_config(project, branch)
                if app is not None:
                    if app["is_need_jenkins_verify"]:
                        # 判断是否验证编译过了
                        logger.info("project needs verify")
                        if verified_by_sysadmin:
                            sysadmin_value = int(verified_by_sysadmin[0]["value"])
                            logger.info(f"jenkins verify value --> {sysadmin_value}")
                            if sysadmin_value != 1:
                                logger.info("sysadmin is not verify")
                                continue
                        else:
                            logger.info("verified_by_sysadmin is null")
                            continue

                    logger.info("check is need merge")
                    if app["is_need_merge"]:
                        if app["ignore_branch"] == branch:
                            verify_and_merge(gerrit_url, patch_id=patch_id)
                        else:
                            logger.error(f"项目当前{branch}不能merge")
                    else:
                        if app["ignore_branch"] == branch:
                            logger.info(
                                f"项目分支不在管理列表,当前{branch}不做merge动作")
                        else:
                            logger.info("不需要Merge")
                else:
                    logger.info(f"merge --> project --> {project}")
                    verify_and_merge(gerrit_url, patch_id=patch_id)


def verify_and_merge(url, patch_id):
    verify(url, patch_id)
    merge(url, patch_id)


def verify(url, patch_id):
    gerrit_option.verify_code(url, patch_id=patch_id)


def merge(url, patch_id):
    gerrit_option.submit_code(url, patch_id=patch_id)
