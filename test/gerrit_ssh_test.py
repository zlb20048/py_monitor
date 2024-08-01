import os, json

def get_patch_info(GERRIT_HOME, status):
    cmd_str='ssh -p 29418 %s gerrit query --format=JSON reviewer:self status:%s'%(GERRIT_HOME, status)
    process = os.popen(cmd_str)
    output = process.readlines()[0] # 参见说明
    process.close()
    jsn_data = json.loads(output) # 返回的是dict
    print("format {}".format(jsn_data))
    return jsn_data

def get_review_info(GERRIT_HOME):
    cmd_str='ssh -p 29418 %s gerrit query --format=JSON reviewer:self status:open'%(GERRIT_HOME)
    print(cmd_str)
    process = os.popen(cmd_str)
    output_lines = process.readlines()
    process.close()

    jsn_data_list = []
    for line in output_lines:
        jsn_data = json.loads(line)
        jsn_data_list.append(jsn_data)
    
    return jsn_data_list
    