from flask import Blueprint, request, current_app
from flask_restful import Resource, Api
from app_spider.models import db, company_info, job_info, company_info_ex, job_info_ex
from app_spider.views.common.view_decorators import permission_check, cls_decorate
from app_spider.views.common.utils import *
from app_spider import mongo_client
from .forms import *
from .forms import rule_dic

import json
import traceback
input_mongodb_api_view = Blueprint("input_mongodb_api_view", __name__)
input_mongodb_api = Api(input_mongodb_api_view)

@cls_decorate(permission_check)
class InputMongodbResource(Resource):
    def post(self, table, uid):
        try:
            # 检查表单
            global rule_dic
            relation, data, rule, status, message = check_form(request.form, table)
            if not status:
                return failed_resp(message, 500)

            # 根据classify字段调用相应的函数
            # 返回 _id, 状态, 信息
            classify = rule["classify"]
            obj_id, status, message = rule_dic[classify](data, rule, table, relation, uid) # 根据classify选择不同的函数进行插入数据操作

            # 如果状态为False, 表示插入失败, message里为失败信息
            if not status:
                return failed_resp(message, 500)

            return succeed_resp(_id=str(obj_id))
        except:
            current_app.logger.error(traceback.format_exc())
            return failed_resp("error", 500)

    def patch(self, table, uid):
        return failed_resp("error", 500)

input_mongodb_api.add_resource(InputMongodbResource,"/api/input_mongodb/<string:table>")
