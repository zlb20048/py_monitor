import jenkins
import gerrit_config

# 配置 Jenkins URL 和认证信息
jenkins_url = 'http://10.10.96.190:8080/view/HMTC/view/HMTC8295'
user = gerrit_config.get_user_name()
api_token = gerrit_config.get_jenkins_api_token()

# 创建 Jenkins 服务器实例
server = jenkins.Jenkins(jenkins_url, username=user, password=api_token)

# 配置 Job 名称和参数
job_name = 'PRJ_HMTC_APP'
params = {
    'Media_build': 'Y',
    'ANDROID_SYSTEM_HOME': 'PRJ_HMTC_8295'
}


def build_8295_app():
    try:
        server.build_job(job_name, parameters=params)
        print("Jenkins Job Triggered Successfully")
    except jenkins.JenkinsException as e:
        print(f"Failed to Trigger Jenkins Job: {e}")
