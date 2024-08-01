import json

# 提供的JSON数据
data = '''
{
    "project": "projects/HYUNDAI-APP/packages/apps/LocalRadio",
    "branch": "master",
    "id": "I5b90f7d9e7debde14640fc5979d2df30a29fbb32",
    "number": 4551,
    "subject": "DOING\u003d#HMTC8295-1215 【现代8295】【Local Radio】收藏页面-收藏列表(无收藏展示，更新相关UI)",
    "owner": {
        "name": "贾成成",
        "email": "chengchengjia@pateo.com.cn",
        "username": "chengchengjia"
    },
    "url": "http://10.10.96.213:8081/c/projects/HYUNDAI-APP/packages/apps/LocalRadio/+/4551",
    "hashtags": [

    ],
    "createdOn": 1721642592,
    "lastUpdated": 1721705356,
    "open": false,
    "status": "MERGED",
    "currentPatchSet": {
        "number": 1,
        "revision": "2c1d9447b5f2a6535b105e636d95c9ab59f4cbd7",
        "parents": [
            "0b863afa9108e769a2fef9fb3bc7265182fc0ca9"
        ],
        "ref": "refs/changes/51/4551/1",
        "uploader": {
            "name": "贾成成",
            "email": "chengchengjia@pateo.com.cn",
            "username": "chengchengjia"
        },
        "createdOn": 1721642592,
        "author": {
            "name": "贾成成",
            "email": "chengchengjia@pateo.com.cn",
            "username": "chengchengjia"
        },
        "kind": "REWORK",
        "approvals": [
            {
                "type": "Verified",
                "description": "Verified",
                "value": "1",
                "grantedOn": 1721705354,
                "by": {
                    "name": "严国柱",
                    "email": "guozhuyan@pateo.com.cn",
                    "username": "guozhuyan"
                }
            },
            {
                "type": "Sonar-Scan",
                "description": "Sonar-Scan",
                "value": "1",
                "grantedOn": 1721705354,
                "by": {
                    "name": "严国柱",
                    "email": "guozhuyan@pateo.com.cn",
                    "username": "guozhuyan"
                }
            },
            {
                "type": "Code-Review",
                "description": "Code-Review",
                "value": "2",
                "grantedOn": 1721705354,
                "by": {
                    "name": "严国柱",
                    "email": "guozhuyan@pateo.com.cn",
                    "username": "guozhuyan"
                }
            },
            {
                "type": "SUBM",
                "value": "1",
                "grantedOn": 1721705356,
                "by": {
                    "name": "严国柱",
                    "email": "guozhuyan@pateo.com.cn",
                    "username": "guozhuyan"
                }
            },
            {
                "type": "Verified",
                "description": "Verified",
                "value": "1",
                "grantedOn": 1721642857,
                "by": {
                    "name": "sysadmin",
                    "email": "sysadmin@pateo.com.cn",
                    "username": "sysadmin"
                }
            }
        ],
        "sizeInsertions": 140,
        "sizeDeletions": 18
    }
}
'''

# 解析JSON数据
data_dict = json.loads(data)

# 提取Verfiy是sysadmin的内容
verified_by_sysadmin = [
    approval for approval in data_dict['currentPatchSet']['approvals']
    if approval['type'] == 'Verified' and approval['by']['username'] == 'sysadmin'
]

print(len(verified_by_sysadmin))
sysadmin = verified_by_sysadmin[0]
sysadmin_value = sysadmin["value"]
print(f"value --> {sysadmin_value}")

verified_by_sysadmin = [
    approval for approval in data_dict['currentPatchSet']['approvals']
    if approval['type'] == 'Verified' and approval['by']['username'] == 'sysadmin'
]


# 定义测试函数
def do_break_return_test():
    for item in verified_by_sysadmin:
        sysadmin_value = int(item['value'])  # 确保sysadmin_value定义
        print(f"sysadmin_value --> {sysadmin_value}")
        if sysadmin_value == 1:
            break
        print("do_break_return_test")


# 打印结果
if verified_by_sysadmin:
    do_break_return_test()
else:
    print("No 'Verified' approval by 'sysadmin' found.")
