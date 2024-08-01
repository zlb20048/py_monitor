import json
import os


def _get_info_from_gerrit(cmd_str):
    output_lines = _do_process(cmd_str)
    jsn_data_list = []
    for line in output_lines:
        jsn_data = json.loads(line)
        jsn_data_list.append(jsn_data)
    return jsn_data_list


def get_review_info(gerrit_home):
    cmd_str = (
            "ssh -p 29418 %s gerrit query --format=JSON --current-patch-set reviewer:self status:open"
            % gerrit_home
    )
    jsn_data_list = _get_info_from_gerrit(cmd_str=cmd_str)
    return jsn_data_list


def get_self_unmerge(gerrit_home):
    cmd_str = (
            "ssh -p 29418 %s gerrit query --format=JSON --current-patch-set owner:self status:open"
            % gerrit_home
    )
    jsn_data_list = _get_info_from_gerrit(cmd_str=cmd_str)
    return jsn_data_list


def get_all_un_merge(gerrit_url):
    gerrit_review_info = get_review_info(gerrit_url)
    gerrit_self_unmerge_info = get_self_unmerge(gerrit_url)
    gerrit_info = gerrit_review_info + gerrit_self_unmerge_info
    return gerrit_info


def _do_process(cmd_str):
    process = os.popen(cmd_str)
    output_lines = process.readlines()
    process.close()
    return output_lines


def verify_code(gerrit_home, patch_id):
    cmd_str = (
            "ssh -p 29418 %s gerrit review --verified +1 --code-review +2 --sonar-scan +1 %s"
            % (gerrit_home, patch_id)
    )
    _do_process(cmd_str)


def submit_code(gerrit_home, patch_id):
    cmd_str = "ssh -p 29418 %s gerrit review --submit %s" % (gerrit_home, patch_id)
    _do_process(cmd_str)
