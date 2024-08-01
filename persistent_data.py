from collections import namedtuple
from CustomProperty import PersistentClass

# 定义一个具名元组，包含 add_value、update_value 和 get_data 方法
PersistentMethods = namedtuple(
    "PersistentMethods", ["add_value", "update_value", "get_value"]
)


def create_persistent_instance(file_name):
    persistent_instance = PersistentClass(file_name)

    # 返回一个具名元组对象，包含相关方法
    return PersistentMethods(
        add_value=persistent_instance.add_value,
        update_value=persistent_instance.update_value,
        get_value=persistent_instance.data.get,
    )
