from peewee import Model, SqliteDatabase, CharField, IntegerField, fn
from datetime import datetime, timedelta

db = SqliteDatabase('monitor.db')


class Gerrit(Model):
    url = CharField(primary_key=True)
    name = CharField()
    time = CharField()
    count = IntegerField()

    class Meta:
        database = db


class JenkinsData(Model):
    DoesNotExist = None
    name = CharField(primary_key=True)
    url = CharField()

    class Meta:
        database = db


class JenkinsBuild(Model):
    DoesNotExist = None
    update_id = CharField(primary_key=True)
    message = CharField()

    class Meta:
        database = db


# 连接到数据库
db.connect()

# 创建表
db.create_tables([Gerrit, JenkinsData, JenkinsBuild])


def save_jenkins_build_update_id(update_id, message):
    with db.atomic():
        jenkins_build, created = JenkinsBuild.get_or_create(update_id=update_id, defaults={'message': message})
        if not created:
            jenkins_build.message = message
            jenkins_build.save()
        return jenkins_build


def get_jenkins_build_update_id():
    try:
        # 查询需要更新的对象
        jenkins_build_data = JenkinsBuild.select(JenkinsBuild.update_id).order_by(JenkinsBuild.update_id.desc()).first()
        return jenkins_build_data
    except JenkinsBuild.DoesNotExist:
        return None


def save_gerrit_data(name, url, time, count):
    with db.atomic():
        gerrit, created = Gerrit.get_or_create(url=url, defaults={'name': name, 'time': time, 'count': count})
        if not created:
            gerrit.count += count
            gerrit.save()
        return gerrit


def get_jenkins_data(name):
    try:
        # 查询需要更新的对象
        jenkins_data = JenkinsData.get(JenkinsData.name == name)

        # 修改属性
        return jenkins_data
    except JenkinsData.DoesNotExist:
        print(f"Jenkins with name '{name}' not found.")
        return None


def save_jenkins_data(name, url):
    with db.atomic():
        jenkins_create, created = JenkinsData.get_or_create(name=name, defaults={'name': name, 'url': url})
        if not created:
            jenkins_create.url = url
            jenkins_create.save()
            return jenkins_create


def analyze_user_commit():
    # 获取当前时间
    current_time = datetime.now()

    # 获取最近一周的开始时间
    start_of_week = current_time - timedelta(days=current_time.weekday(), hours=current_time.hour,
                                             minutes=current_time.minute, seconds=current_time.second)

    # 查询最近一周的数据，并按照每个名称下的数据数量（条数）排序
    user_commit_counts = (
        Gerrit
        .select(Gerrit.name, fn.Count(Gerrit.name).alias('count'))
        .where(Gerrit.time >= start_of_week)
        .group_by(Gerrit.name)
        .order_by(Gerrit.time.asc())
    )

    for user_count in user_commit_counts:
        print("姓名: {}, 提交数: {}".format(user_count.name, user_count.count))

        # 获取该名称下的所有数据，并按时间排序
        user_commit_data = (
            Gerrit
            .select()
            .where((Gerrit.name == user_count.name) & (Gerrit.time >= start_of_week))
            .order_by(Gerrit.time.desc())
        )

        for record in user_commit_data:
            print("  URL: {}, Time: {}".format(record.url, record.time))
        print()  # 每个分组之间添加空行


if __name__ == '__main__':
    save_gerrit_data(name="zixiangliu", url="https://112.112.4", time="2024-01-15 17:52:01", count=1)
    save_gerrit_data(name="zixiangliu", url="https://112.112.3", time="2024-01-15 17:52:01", count=1)
    save_gerrit_data(name="zixiangl", url="https://112.112.1", time="2024-01-17 17:52:01", count=1)
    save_gerrit_data(name="zixiangl", url="https://112.112.11", time="2024-01-14 17:52:01", count=1)
    save_jenkins_build_update_id("12334455", "hello")
    save_jenkins_build_update_id("12334456", "中文")
    jenkins = save_jenkins_data(name="jenkins_app4", url="https://112.112.24")
    jenkins_build = get_jenkins_build_update_id()
    print(f"jenkins_build --> {jenkins_build.update_id}")
    # print(f"name -> {jenkins.name}, url -> {jenkins.url}")
    # data = get_jenkins_data("jenkins_app")
    # print(f"name -> {data.name}, url -> {data.url}")
    # update_jenkins_data(name="jenkins_app3", new_url="https://112.112.10")
    # analyze_user_commit()
