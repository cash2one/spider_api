# -*- coding:utf-8 -*-
from flask import request
from functools import wraps
from app_spider.views.common.utils import failed_resp
from app_spider.config import TOKEN

def permission_check(func):
    @wraps(func)
    def _decorate(*args, **kwargs):
        token = request.headers.get("token","")
        if not token:
            return failed_resp("token missing", 401)
        if token != TOKEN:
            return failed_resp(u"token 错误", 401)
        return func(*args, **kwargs)
    return _decorate
