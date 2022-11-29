import json
import uuid

from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache

from file.models import File, FileDetail
from service.file_upload_storage_service import FileUploadStorageService
from util.JsonResult import JsonResult


# Create your views here.


@require_http_methods(["POST"])
@transaction.atomic()
def file_upload(request):
    """
    保存分块文件
    :param request:
    :return:
    """
    params = request.POST
    filename = params['filename']
    chunk_number = int(params['chunk'])
    md5 = params['md5']
    size = int(params['chunkSize'])
    belong = int(params['belong'])
    task_id = params['taskId']
    start = int(params['start'])
    end = int(params['end'])
    facility_code = params['facilityCode']
    print('基本信息', filename, chunk_number, md5, size, task_id, belong)
    task = File.objects.get(task_id=task_id)
    if task is None:
        # 为空, 说明没有提交任务
        return JsonResult.fail(404, "没有提交任务之前不允许直接上传分片")
    file_data = request.FILES.get('file')
    file_service = FileUploadStorageService()
    file_service.upload_file_chunk(task_id=task.task_id, facility_code=facility_code, chunk_number=chunk_number,
                                   filename=filename, bytes=file_data.read(), start=start, end=end, chunk_size=size)

    file_chunk = FileDetail.objects.filter(task_id=task_id, md5=md5).first()
    file = request.FILES.get('file')
    # 任务成功的数量+1
    cache.incr(cache_key(task_id))
    return JsonResponse({
        'code': 200,
        'msg': '上传成功',
        'success': True,
    })


@require_http_methods(["POST"])
def check_file_by_md5(request):
    """
    检查之前是否传输,没有的话就上传文件
    :param request:
    :return:
    """
    body = json.loads(request.body.decode())
    md5 = body.get('md5')
    # 第一步,检查md5在服务器是否已经存在, 存在的话就直接返回
    file = File.objects.filter(md5=md5).first()
    if not file:
        return JsonResult.success({
            'exist': False
        })
    else:
        # 存在的情况,已经完成的状态
        if file.status == 1:
            return JsonResult.success({
                'exist': True,
                'file': file.to_json(),
                'done': True
            })
        elif file.status == 3:
            return JsonResult.success({
                'exist': True,
                'file': file.to_json(),
                'done': 'UPLOADING',
                'msg': '有客户端正在上传,请务重复提交'
            })
        else:
            file_details = FileDetail.objects.filter(task_id=file.task_id)
            # 特别要注意django的序列化
            return JsonResult.success({
                'file': file.to_json(),
                'details': serializers.serialize("json", file_details),
                'done': False,
                'exist': True
            })


@require_http_methods(["POST"])
@transaction.atomic()
def merge(request):
    """
    合并文件 todo 优化，先判断redis的success, 然后在判断数据库的success
    :param request:
    :return:
    """
    body = json.loads(request.body.decode())
    task_id = body.get('taskId')
    file = File.objects.filter(task_id=task_id).first()
    if file is None:
        return JsonResult.fail(404, '找不到file记录,无法发起合并操作')
    # 如果状态是上传完成, 那么直接返回
    if file.status == 1:
        return JsonResult.success({'done': True, 'file': file})
    # 前置条件, 检查是否所有文件均已经上传,防止攻击
    # 找出所有上传成功的分片
    chunks = FileDetail.objects.filter(task_id=file.task_id, status=1)
    print("缓存中的数量", cache.get(cache_key(task_id=task_id)))
    print("分片数量", len(chunks))
    if len(chunks) != file.total_chunk or cache.get(cache_key(task_id=task_id)) != file.total_chunk:
        # 说明没有上传完成,返回未上传完成状态,同时把已经上传成功的返回回去
        # return JsonResult.success({
        #     'done': False,
        #     'details': chunks
        # })
        return JsonResult.fail(400, "分片未全部上传完成,无法发起合并的操作")
    file_service = FileUploadStorageService()
    file_service.merge_chunk(task_id=task_id)
    cache.delete(cache_key(task_id=task_id))
    return JsonResult.success(True)
    # 第四步: 删除所有的切片, 把chunk文件夹直接删除即可


@require_http_methods(["POST"])
def create_upload_file_task(request):
    """
    创建文件上传任务
    :param request:
    :return:
    """
    body = json.loads(request.body.decode())
    md5 = body.get("md5")
    upload_filename = body.get("filename")
    total = int(body.get("totalChunk"))
    belong = int(body.get('belong'))
    if len(md5) == 0 | len(upload_filename) == 0 | total == 0:
        return JsonResult.fail(404, "MD5值不能为空,filename, total 不能为空")
    file_record = File.objects.filter(md5=md5).first()
    if file_record is not None:
        return JsonResult.success({
            "exist": True,
            "msg": "任务已存在",
            "file": file_record.to_json()
        })
    file = File(upload_filename=upload_filename, task_id=uuid.uuid4().hex, md5=md5,
                status=0, total_chunk=total, success_chunk=0, belong=belong)
    file.save()
    # redis中存储
    cache.set(cache_key(file.task_id), 0)
    # todo 是否需要创建分片规则
    return JsonResult.success({
        "file": file.to_json(),
        "exist": False
    })


@require_http_methods(['GET'])
def test(request):
    """
    测试接口
    :param request:
    :return:
    """
    return JsonResponse({
        'code': 0,
        'success': True
    })


def cache_key(task_id):
    return "task_id:" + task_id
