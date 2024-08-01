import os
import shutil
import glob
import requests
import zipfile
import find_package_path
from tqdm import tqdm
import time
from alive_progress import alive_bar

# global_save_path = "/home/zhengfang/software/Jenkins-python-monitor/download/"
global_save_path = "D:/IVY-SOP/"


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100)

    with open(save_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    print("文件下载成功！")


def check_and_delete_folders(path, max_folders):
    folders = glob.glob(os.path.join(path, "*"))  # 获取指定路径下的所有文件夹
    folders = [folder for folder in folders if os.path.isdir(folder) and not
    os.path.islink(folder) and not is_system_folder(folder)]  # 排除隐藏和系统文件夹

    print("当前文件夹数量:  ", len(folders), "    ", folders)
    if len(folders) > max_folders:
        folders.sort(key=lambda x: os.path.getmtime(x))  # 按修改时间排序
        folders_to_delete = folders[:len(folders) - max_folders]  # 获取要删除的文件夹列表

        print("要删除的文件夹列表:\n", folders_to_delete)
        for folder in folders_to_delete:
            shutil.rmtree(folder)  # 删除文件夹及其内容
            print(f"已删除文件夹: {folder}")
    else:
        print("文件夹数量未超过限制，无需删除。")


def is_system_folder(folder):
    folder = os.path.realpath(folder)  # 获取链接文件夹的真实路径
    system_folders = ['$RECYCLE.BIN', 'System Volume Information']  # 系统文件夹列表
    return os.path.basename(folder) in system_folders


def extract_zip(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        # progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100)
        progress_bar = tqdm(total=len(file_list), unit="file", ncols=100)

        for file in file_list:
            zip_ref.extract(file, extract_path)
            progress_bar.update(1)

        progress_bar.close()

    print("压缩包解压缩完成！")


def download_wrapper(package_url, num, need_unzip=False):
    download_folder_path = global_save_path + num + "/"

    package_name = find_package_path.get_package_name_from_url(package_url)
    save_file_path = download_folder_path + package_name

    max_folders_to_keep = 5
    extract_folder_path = download_folder_path + package_name + "dir/"

    check_and_delete_folders(global_save_path, max_folders_to_keep)

    folder = os.path.exists(download_folder_path)
    if not folder:
        os.makedirs(download_folder_path)

    print("save_file_path           ", save_file_path)
    print("download_folder_path     ", download_folder_path)
    print("extract_folder_path      ", extract_folder_path)

    download_file(package_url, save_file_path)

    if need_unzip == True:
        folder = os.path.exists(extract_folder_path)
        if not folder:
            os.makedirs(extract_folder_path)
        # check_and_delete_folders(download_folder_path, max_folders_to_keep)
        extract_zip(save_file_path, extract_folder_path)

# 使用示例
# jenkins_url = "http://example.com/path/to/your/zipfile.zip"
# save_file_path = "/path/to/save/your/zipfile.zip"
# download_folder_path = "/path/to/download/folder"
# max_folders_to_keep = 10
# extract_folder_path = "/path/to/extract/folder"

# download_file(jenkins_url, save_file_path)
# check_and_delete_folders(download_folder_path, max_folders_to_keep)
# extract_zip(save_file_path, extract_folder_path)
