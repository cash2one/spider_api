from flask import Blueprint, request, current_app
from flask_restful import Resource, Api
from app_spider.models import db, company_info, job_info, company_info_ex, job_info_ex
from app_spider.views.common.view_decorators import permission_check, cls_decorate
from app_spider.views.common.utils import *
from app_spider import mongo_client
from .forms import *

import json
import traceback
import time
input_mongodb_api_view = Blueprint("input_mongodb_api_view", __name__)
input_mongodb_api = Api(input_mongodb_api_view)

@cls_decorate(permission_check)
class InputMongodbResource(Resource):
    def post(self, table, uid):
        try:
            # 检查表单

            relation, data, status = check_form(request.form, table)
            if not status:
                return failed_resp("error", 500)

            # 查找关联数据, 并且获取_id
            one_relation = {}
            for i in relation:
                if "table" not in i.keys():
                    continue
                relation_table = i.pop("table")
                relation_query = mongo_client.db[relation_table].find(i)
                if relation_query.count() == 0:
                    continue
                one_relation[relation_table] = [i["_id"] for i in relation_query]

            # 插入数据
            data["create_time"] = int(time.time())
            data["update_time"] = int(time.time())
            data['relation'] = one_relation if one_relation else None
            obj_id = mongo_client.db[table].insert_one(data).inserted_id

            # 在关联数据中, 插入当前数据_id

            for table_name, value in one_relation.items():
                query_count = mongo_client.db[table_name].update({"_id":{"$in":value}}, {"$push":{"relation.{table}".format(table=table):obj_id}}, multi=True)
            return succeed_resp(_id=str(obj_id))
        except:
            current_app.logger.error(traceback.format_exc())
            return failed_resp("error", 500)

    def patch(self, table, uid):
        return failed_resp("error", 500)

input_mongodb_api.add_resource(InputMongodbResource,"/api/input_mongodb/<string:table>")
