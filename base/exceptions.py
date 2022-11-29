class CommonException(Exception):
    """
    公共异常类
    """

    def __init__(self, enum_cls):
        self.code = enum_cls.code
        self.errmsg = enum_cls.errmsg
        self.enum_cls = enum_cls  # 状态枚举码
        super(Exception).__init__()


class BusinessException(CommonException):
    """业务异常类"""

    def __init__(self, enum_cls):
        super(BusinessException, self).__init__(enum_cls=enum_cls)
