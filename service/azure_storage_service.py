from azure.storage.blob import BlockBlobService
from azure.storage.blob.models import BlobBlock


class AzureStorageService:
    """azure存储服务类"""

    def __init__(self, connect_string,base_azure_url):
        self.base_azure_url = base_azure_url
        self.block_blob_service = BlockBlobService(connect_string)

    def put_chunk(self, container_name, blob_name, file_bytes, block_id):
        """
        上传分块
        :param container_name: 容器名称
        :param blob_name: 整块文件名称
        :param file_bytes: 字节数据
        :param block_id: 分块名称
        :return:
        """
        self.block_blob_service.put_block(container_name, blob_name, file_bytes, block_id)
        return block_id

    def get_blobk(self, block_id):
        """
        返回 Block
        :param block_id:
        :return:
        """
        return BlobBlock(id=block_id)

    def put_block_list(self, container_name, blob_name, blocks):
        """合并文件"""
        self.block_blob_service.put_block_list(container_name=container_name, blob_name=blob_name, block_list=blocks)

    def merge(self, container_name, blob_name):
        block_list = self.block_blob_service.get_block_list(container_name=container_name, blob_name=blob_name,
                                                            snapshot=None,
                                                            block_list_type="all")
        block_list.committed_blocks
        # return {
        #     'url': self.base_azure_url + "/" + container_name + "/" + blob_name # todo 带确认
        # }
