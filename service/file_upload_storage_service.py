from django.conf import settings

from base.enums import StatusCodeEnum
from base.exceptions import BusinessException
from file.models import FileDetail, File
from service.azure_storage_service import AzureStorageService


class FileUploadStorageService(AzureStorageService):
    def __init__(self):
        self.container_name = settings.AZURE_CONFIG.get('container_name')
        super(AzureStorageService).__init__(settings.AZURE_CONFIG.get('connect_string'),
                                            settings.AZURE_CONFIG.get('base_azure_url'))

    def upload_file_chunk(self, task_id, facility_code, chunk_number, upload_filename, bytes, start, end,
                          chunk_size, ext=".part"):
        """
        保存分块分解
        :param task_id: 任务id
        :param facility_code: 机构编码
        :param chunk_number: 第几块
        :param upload_filename: 上传的文件名
        :param bytes:
        :param start:
        :param end:
        :param chunk_size:
        :param ext:
        :return:
        """
        # 文件规则
        blob_name = facility_code + "/" + task_id + ext
        blob_id = task_id + chunk_number + chunk_size + ".part"
        self.put_chunk(container_name=self.container_name,
                       blob_name=blob_name, file_bytes=bytes
                       , block_id=blob_id
                       )
        detail = FileDetail(task_id=task_id, status=1, chunk=chunk_number, upload_filename=upload_filename,
                            filename=blob_id,
                            chunk_size=chunk_size,
                            start=start,
                            end=end
                            )
        detail.save()

    def merge_chunk(self, task_id):
        file = File.objects.filter(task_id=task_id).first()
        if file is None:
            raise BusinessException(StatusCodeEnum.FILE_TASK_NOT_EXIST)
        # 查询出所有的FileDetail
        details = FileDetail.objects.filter(task_id=task_id, status=1)
        ids = []
        for detail in details:
            ids.append(detail.id)
        # details 排序
        ids.sort()
        blocks = []
        for item in ids:
            block = self.get_block(item)
            blocks.append(block)
        self.put_block_list(self.container_name, file.filename, blocks)
        self.merge(self.container_name, file.filename)
        file.status = 1
        file.success_chunk = len(details)
        file.path = self.base_azure_url + "/" + self.container_name + "/" + file.path
        file.save()
