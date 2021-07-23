
import os
import shutil


def create_folder(folder_path):
    try:
        shutil.rmtree(folder_path)  # 결과 폴더 삭제
    except:
        pass
    finally:
        os.mkdir(folder_path)  # 결과 폴더 생성


def create_folder_not_remove(folder_path):
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)


def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
