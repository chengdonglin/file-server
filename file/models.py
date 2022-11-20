from django.db import models
import json


# Create your models here.

class File(models.Model):
    upload_filename = models.CharField(max_length=128, verbose_name="请求时候的文件名称")
    task_id = models.CharField(max_length=64, verbose_name="任务编号")
    md5 = models.CharField(max_length=64, verbose_name="文件MD5值")
    status = models.IntegerField(verbose_name="状态,0-上传中,1-上传成功,2-上传失败")
    total_chunk = models.IntegerField(verbose_name="总分片数")
    success_chunk = models.IntegerField(verbose_name="成功分片数量")
    path = models.CharField(max_length=256, verbose_name="文件存储路径")
    filename = models.CharField(max_length=126, verbose_name="在服务器存储的文件名称")
    belong = models.IntegerField(verbose_name="归属")

    class Meta:
        managed = True
        db_table = 'tb_file'
        verbose_name = '文件信息'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        return json.dumps(d)


class FileDetail(models.Model):
    task_id = models.CharField(max_length=64, verbose_name="任务编号")
    md5 = models.CharField(max_length=64, verbose_name="分片文件MD5值")
    status = models.IntegerField(verbose_name="状态,0-上传中,1-上传成功,2-上传失败,3-待开始")
    chunk = models.IntegerField(verbose_name="当前第几分片")
    path = models.CharField(max_length=256, verbose_name="当前分片路径")
    upload_filename = models.CharField(max_length=128, verbose_name="文件名称")
    filename = models.CharField(max_length=256, verbose_name="在服务器存储的文件名称")
    chunk_size = models.IntegerField(verbose_name="分片的大小")
    start = models.IntegerField(verbose_name="分片开始的位置")
    end = models.IntegerField(verbose_name="分片结束的位置")

    class Meta:
        managed = True
        db_table = 'tb_file_detail'
        verbose_name = '分片信息'

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        return json.dumps(d)