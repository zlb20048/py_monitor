import requests
from loguru import logger


# Get newleast job path
def get_latest_build_url(url):
    api_url = url + "api/json"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            job_path = data["lastBuild"]["url"]
            return job_path
    except Exception as e:
        logger.error("Get latest build url error: %s" % e)
        return None


# Get jenkins build json data
def get_latest_build_data(job_url):
    # print("get_latest_build_data")
    api_url = job_url + "api/json"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        # print("data json\n      ",data)
        # 以方便查看的方式打印json字符串
        # data_json = json.dumps(data,indent=4)
        # print("data json\n      ",data_json)

        # print('///////////////////////////////////////////////////')
        # print(data)
        # print('///////////////////////////////////////////////////')
        # printer.print_color('building : ', data["building"], "RED",True)
        # printer.print_color('result : ', data["result"], data["building"], "RED",True)
        # logger.debug("building : %s" % data["building"])
        # logger.info("result : %s " % data["result"])
        # print("///////////////////////////////////////////////////")
        return data
    else:
        return None


if __name__ == '__main__':
    get_latest_build_data("http://10.10.96.190:8080/view/HMTC/view/HMTC8295/job/PRJ_HMTC_QNX/212/")