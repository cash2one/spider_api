from flask import Blueprint, request
from flask_restful import Resource, Api
from app_spider.models import db, company_info, job_info, company_info_ex, job_info_ex
from app_spider.views.common.view_decorators import permission_check
from app_spider.views.common.utils import *
from .forms import *
import json
import traceback

input_data_api_view = Blueprint("input_data_api_view", __name__)
input_data_api = Api(input_data_api_view)


class InputDataResource(Resource):
    @permission_check
    def post(self, table, uid):
        if table == "company_info":
            if check_data(request.form, company_info):
                return failed_resp("data exists", 401)

            company_form, company_ex_form = split_form(request.form, company_info)
            company_form["uid"]=uid
            one = company_info(company_form)
            db.session.add(one)
            db.session.flush()
            db_id = one.id
            for key,value in company_ex_form.items():
                inr = company_info_ex(db_id, key, str(value))
                db.session.add(inr)
            db.session.commit()
            return succeed_resp(db_id=db_id)

        elif table == "job_info":
            if check_data(request.form, job_info):
                return failed_resp("data exists", 401)
            if not check_data(request.form, job_info, db_id=request.form.get("company_id","-1")):
                return failed_resp("job_id is not exists", 401)

            job_info_form, job_info_ex_form = split_form(request.form, job_info)
            job_info_form["uid"]=uid
            one = job_info(job_info_form)
            db.session.add(one)
            db.session.flush()
            db_id = one.id
            for key,value in job_info_ex_form.items():
                inr = job_info_ex(db_id, key, str(value))
                db.session.add(inr)
            db.session.commit()
            return succeed_resp(db_id=db_id)

        else:
            return failed_resp("wrong url", 401)

    @permission_check
    def patch(self, table, uid):
        try:
            if table == "company_info":
                # 修改数据的某一些字段
                if check_data(request.form, company_info, request.form.get("db_id")):
                    data = json.loads(request.form.get("data_json"))
                    company_info_form, company_info_ex_form = split_form_in_change(data, company_info)
                    if request.form.get("db_id"):
                        query = company_info.query.filter_by(id=request.form.get("db_id")).first()
                    else:
                        query = company_info.query.filter_by(web_id=request.form.get("web_id"), from_web=request.form.get("from_web")).first()
                    for key, value in company_info_form.items():
                        print (key, value)
                        setattr(query, key, value)
                    db_id = query.id
                    db.session.commit()
                    for key, value in company_info_ex_form.items():
                        query_ex = company_info_ex.query.filter_by(company_info_id=db_id, meta_key=key).update({"meta_value":value})
                    db.session.commit()
                    return succeed_resp()
                else:
                    return failed_resp("company is not exists", 401)

            elif table == "job_info":
                if check_data(request.form, job_info, request.form.get("db_id")):
                    data = json.loads(request.form.get("data_json"))
                    job_info_form, job_info_ex_form = split_form_in_change(data, job_info)
                    if request.form.get("db_id"):
                        query = job_info.query.filter_by(id=request.form.get("db_id")).first()
                    else:
                        query = job_info.query.filter_by(web_id=request.form.get("web_id"), from_web=request.form.get("from_web")).first()
                    for key, value in job_info_form.items():
                        print (key, value)
                        setattr(query, key, value)
                    db_id = query.id
                    db.session.commit()
                    for key, value in job_info_ex_form.items():
                        query_ex = job_info_ex.query.filter_by(job_info_id=db_id, meta_key=key).update({"meta_value":value})
                    db.session.commit()
                    return succeed_resp()
                else:
                    return failed_resp("job is not exists", 401)
            else:
                return failed_resp("wrong url", 401)
        except:
            traceback.print_exc()
            return failed_resp("error", 500)

input_data_api.add_resource(InputDataResource,"/api/input_data/<string:table>")
