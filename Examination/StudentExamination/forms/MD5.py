from django.conf import settings
import hashlib


def md5(date_string):
    """md5加密"""
    # 选择加密的字段为django自带的
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    # 将要加密的数据放进去
    obj.update(str(date_string).encode("utf-8"))
    # 返回加密过的数据
    return obj.hexdigest()
