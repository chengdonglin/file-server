from django.db import DatabaseError
from django.utils.deprecation import MiddlewareMixin

from base.enums import StatusCodeEnum
from base.exceptions import BusinessException
from util.JsonResult import JsonResult


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        """
        print(exception)
        if isinstance(exception, BusinessException):
            # 业务异常处理
            return JsonResult.fail(exception.enum_cls.code,
                                   exception.enum_cls.errmsg)

        elif isinstance(exception, DatabaseError):
            return JsonResult.fail(StatusCodeEnum.DB_ERROR.code,
                                   StatusCodeEnum.DB_ERROR.errmsg)

        else:
            return JsonResult.fail(StatusCodeEnum.SERVER_ERR.code,
                                   StatusCodeEnum.SERVER_ERR.errmsg)
