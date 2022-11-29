from django.http import JsonResponse


class JsonResult:
    @staticmethod
    def success(data):
        result = {'code': 0, 'msg': '请求成功', 'success': True, 'data': data}
        return JsonResponse(result)

    @staticmethod
    def fail(code, msg):
        result = {'code': code, 'msg': msg, 'success': False, 'data': {}}
        return JsonResponse(result)

    @staticmethod
    def failed(enum_cls):
        result = {
            'code': enum_cls.code,
            'msg': enum_cls.errmsg,
            'data': None
        }
