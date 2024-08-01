from gerrit_onwer_data import GerritData
import app_config


def do_data_test():
    owner_data_list = [
        "{\"url\": \"http://10.10.96.212:8081/407365\", \"count\": 1, \"time\": \"2024-01-09 15:11:16\"}"]
    convert_data_list = []
    if isinstance(owner_data_list, list):
        print("owner_data_list is list")
        convert_data_list = owner_data_list
    else:
        convert_data_list.append(owner_data_list)

    gerrit_data_list = [GerritData(**data) for data in convert_data_list]
    print("gerrit_data_list ---> {}".format(gerrit_data_list))


def test_include():
    project = "projects/HYUNDAI-APP/packages/apps/LocalRadio"
    projects = "projects/HYUNDAI-APP/packages/apps"
    if projects in project:
        print("in projects")
    else:
        print("Not in projects")


def load_app_config_data():
    manager_project = app_config.get_jenkins_configs()["manager_project"]
    print(f"manager project --> {manager_project}")


if __name__ == '__main__':
    # do_data_test()
    # test_include()
    load_app_config_data()
