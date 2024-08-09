import requests

# jenkins_url = "http://10.10.96.190:8080/view/DongFeng/view/H97c/view/IVY/job/PRJ_H97c_QNX_IVY/150/"
# jenkins_url = "http://10.10.96.190:8080/view/Hozon/view/EP37/view/EP37_Release/job/PRJ_EP37_QNX_Release/179/"
jenkins_url = "http://10.10.96.190:8080/view/HMTC/view/HMTC8295/job/PRJ_HMTC_QNX/211/"

api_url = jenkins_url + "/api/json"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    print("data --> {}".format(data))
    # print('///////////////////////////////////////////////////')
    for action in data.get('actions', []):
        if action.get('_class') == 'hudson.model.ParametersAction':
            parameters = action.get('parameters', [])
            for parameter in parameters:
                if parameter.get('name') == 'VERSION_TYPE':
                    version_type_value = parameter.get('value')
                    print("version_type_value --> {}".format(version_type_value))
                    break

        
    # print('lastBuild: : ', data["lastBuild"])
    # print('lastBuild:number : ', data["lastBuild"]["number"])
    # print('///////////////////////////////////////////////////')
    # job_path = data["lastBuild"]["url"]
    # print('job_path : ',job_path)
    # print('///////////////////////////////////////////////////')

    # for job in data["jobs"]:
    #     if job_path in job["url"]:
    #         job_url = job["url"]
    #         print(job_url)
else:
    print("Failed to get job list.")