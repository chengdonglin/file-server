from enum import Enum


class StatusCodeEnum(Enum):
    """状态码枚举类"""
    OK = (0, 'SUCCESS')
    SERVER_ERR = (500, "SYSTEM ERROR")
    USER_NAME_EXIST = (10010, "用户名已存在")
    DB_ERROR = (500,"db error")
    FILE_TASK_NOT_EXIST = (10010,"文件上传任务不存在")
    USER_NAME_OR_PASSWORD_EMPTY = (10020,"username or password can not empty")

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def errmsg(self):
        return self.value[1]
