# -*- coding:utf-8 -*-
from flask import request
from functools import wraps
from app_spider.views.common.utils import failed_resp
from app_spider.models import db, spider_user


def permission_check(func):
    @wraps(func)
    def _decorate(*args, **kwargs):
        token = request.headers.get("token","")
        if not token:   # 如果头部信息里没有token,返回401
            return failed_resp("token missing", 401)
        user_query = spider_user.query.filter_by(token=token, status=1).first()
        if not user_query: # 如果token在数据库里不存在,返回401
            return failed_resp(u"token 错误", 401)
        # 如果token存在,则返回uid
        uid = user_query.uid
        kwargs.update(uid=uid)
        return func(*args, **kwargs)
    return _decorate
