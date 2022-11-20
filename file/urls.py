from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'file/upload$', views.file_upload),
    re_path(r'file/test$',views.test),
    re_path(r'file/check$',views.check_file_by_md5),
    re_path(r'file/merge$',views.merge),
    re_path(r'file/create$',views.create_upload_file_task)
]
