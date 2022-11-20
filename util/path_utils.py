import os
import time
from django.conf import settings


def make_target_path(target_dir, base_path):
    return os.path.join(base_path, target_dir)


# 创建目录或者文件
def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path=path)


def get_time_str():
    return time.strftime("%Y-%m")


def get_chunk_info(md5, belong):
    info = {}
    # 存放的跟路径
    make_dir(settings.FILE_ROOT)
    # 归属于某一家扫描仪
    belong_path = os.path.join(settings.FILE_ROOT, belong)
    make_dir(belong_path)
    # 具体某一月份
    month_path = os.path.join(belong_path, get_time_str())
    make_dir(month_path)
    # 具体某一个文件的路径
    md5_path = make_target_path(md5, month_path)
    make_dir(md5_path)
    # 合并完整的存放路径
    file_path = os.path.join(md5_path, "files")
    make_dir(file_path)
    # 分片文件存放路径
    chunk_path = os.path.join(md5_path, "chunk")
    make_dir(chunk_path)
    info['file_path'] = file_path
    info['chunk_path'] = chunk_path
    return info


def merge_files(file_details, file_name, file_path):
    """
    合并文件
  :param file_details: 分片列表
  :param file_name: 合并之后的文件名
  :param file_path: 合并之后文件存放的位置
  :return:
  """
    part_files = sorted(file_details, key=lambda item: item.chunk)
    with open(os.path.join(file_path, file_name), 'wb') as fp:
        for part in part_files:
            with open(part.path, "rb") as sf:
                fp.write(sf.read())
                sf.close()
        fp.close()
    return os.path.join(file_path, file_name)
