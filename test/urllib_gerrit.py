import urllib.request
from urllib.error import HTTPError
import gerrit_config

# URL和认证信息
url = 'http://10.10.96.212:8081/login/%23%2Fq%2Fstatus%3Aopen'
username = gerrit_config.get_user_name()
password = gerrit_config.get_gerrit_pwd()

# 创建一个密码管理器
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

# 添加凭据
password_mgr.add_password(None, url, username, password)

# 创建一个处理器，用于管理身份验证
auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

# 创建一个opener
opener = urllib.request.build_opener(auth_handler)

try:
    # 使用opener发送请求
    response = opener.open(url)

    # 读取响应内容
    data = response.read()

    # 打印响应内容
    print(data.decode('utf-8'))  # 假设使用UTF-8编码

    # 关闭连接
    response.close()

except HTTPError as e:
    print("Error: ", e)
