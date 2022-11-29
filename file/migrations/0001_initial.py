# Generated by Django 4.1.3 on 2022-11-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_filename', models.CharField(max_length=128, verbose_name='请求时候的文件名称')),
                ('task_id', models.CharField(max_length=64, verbose_name='任务编号')),
                ('md5', models.CharField(max_length=64, verbose_name='文件MD5值')),
                ('status', models.IntegerField(verbose_name='状态,0-上传中,1-上传成功,2-上传失败')),
                ('total_chunk', models.IntegerField(verbose_name='总分片数')),
                ('success_chunk', models.IntegerField(verbose_name='成功分片数量')),
                ('path', models.CharField(max_length=256, verbose_name='文件存储路径')),
                ('filename', models.CharField(max_length=126, verbose_name='在服务器存储的文件名称')),
                ('belong', models.IntegerField(verbose_name='归属')),
                ('facility_code',models.CharField(max_length=64,verbose_name="机构编码")),
            ],
            options={
                'verbose_name': '文件信息',
                'db_table': 'tb_file',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FileDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=64, verbose_name='任务编号')),
                ('md5', models.CharField(max_length=64, verbose_name='分片文件MD5值')),
                ('status', models.IntegerField(verbose_name='状态,0-上传中,1-上传成功,2-上传失败')),
                ('chunk', models.IntegerField(verbose_name='当前第几分片')),
                ('path', models.CharField(max_length=256, verbose_name='当前分片路径')),
                ('upload_filename', models.CharField(max_length=128, verbose_name='文件名称')),
                ('filename', models.CharField(max_length=256, verbose_name='在服务器存储的文件名称')),
                ('chunk_size', models.IntegerField(verbose_name='分片大小')),
                ('start', models.IntegerField(verbose_name='分片开始的位置')),
                ('end', models.IntegerField(verbose_name='分片结束的位置')),
            ],
            options={
                'verbose_name': '分片信息',
                'db_table': 'tb_file_detail',
                'managed': True,
            },
        ),
    ]
