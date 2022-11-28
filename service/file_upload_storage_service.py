from django.conf import settings

from file.models import FileDetail
from service.azure_storage_service import AzureStorageService


class FileUploadStorageService(AzureStorageService):
    def __init__(self):
        self.container_name = settings.AZURE_CONFIG.get('container_name')
        super(AzureStorageService).__init__(settings.AZURE_CONFIG.get('connect_string'),
                                            settings.AZURE_CONFIG.get('base_azure_url'))

    def upload_file_chunk(self, task_id, facility_code, chunk_number, bytes, chunk_size, ext=".part"):
        """
        上传分片文件
        :param task_id: 任务id
        :param facility_code: 机构
        :param chunk_number : 分块
        :param bytes: 文件字节
        :param chunk_size: 分片大小
        :param ext: 文件后缀
        :return:
        """
        # 文件规则
        blob_name = facility_code + "/" + task_id + ext
        blob_id = task_id + chunk_number + chunk_size + ".part"
        self.put_chunk(container_name=self.container_name,
                       blob_name=blob_name, file_bytes=bytes
                       , block_id=blob_id
                       )
        detail = FileDetail()
        detail.save()

    def put_file_blocks(self, task_id):
        # 查询出所有的FileDetail
        details = FileDetail.objects.filter(task_id=task_id)
        # details 排序

