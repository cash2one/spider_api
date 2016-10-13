from flask import Blueprint, request
from flask_restful import Resource, Api
from app_spider.models import db, company_info, job_info
from app_spider.views.common.view_decorators import permission_check
from app_spider.views.common.utils import *
from .forms import *
import json

lagou_api_view = Blueprint("lagou_api_view", __name__)
lagou_api = Api(lagou_api_view)

def check_input(form, table):
    web_id = form.web_id
    from_web = form.form_web
    query = table.query.filter_by(web_id=web_id, from_web=from_web).first()
    if query:
        return False
    else:
        return True

class lagouResource(Resource):
    @permission_check
    def post(self, table, uid):
        if table == "company_info":
            form = CompanyInfoForm(request.form)
            if form.validate():
                if check_input(form, company_info):
                    return failed_resp("data exists", 401)
                one = {
                    "web_id":form.web_id.data,
                    "name":form.name.data,
                    "boss":form.boss.data,
                    "category":form.category.data,
                    "level":form.level.data,
                    "people_number":form.people_number.data,
                    "location":form.location.data,
                    "description":form.description.data,
                    "web_url":form.web_url.data,
                    "company_url":form.company_url.data,
                    "rate":form.rate.data,
                    "from_web":form.from_web.data,
                    "status":form.status.data,
                    "uid":uid,
                }
                one = company_info(one)
                db.session.add(one)
                db.session.flush()
                db_id = one.id
                return succeed_resp(db_id=db_id)
            else:
                for error_filed, error_message in form.errors.items():
                    if isinstance(error_message, list) and error_message:
                        error_message = error_message[0]
                    return failed_resp("%s: %s" % (error_filed, error_message), 400)

        elif table == "job_info":
            form = JobInfoForm(request.form)
            if form.validate():
                if check_input(form, job_info):
                    return failed_resp("data exists", 401)
                one = {
                    "web_id":form.web_id.data,
                    "company_id":form.company_id.data,
                    "name":form.name.data,
                    "salary":form.salary.data,
                    "job_year":form.job_year.data,
                    "education":form.education.data,
                    "employee_type":form.employee_type.data,
                    "web_url":form.web_url.data,
                    "status":form.status,
                    "from_web":form.from_web.data,
                    "uid":uid,
                }
                one = job_info(one)
                db.session.add(one)
                db.session.flush()
                db_id = one.id
                return succeed_resp(db_id=db_id)
            else:
                for error_filed, error_message in form.errors.items():
                    if isinstance(error_message, list) and error_message:
                        error_message = error_message[0]
                    return failed_resp("%s: %s" % (error_filed, error_message), 400)
        else:
            return failed_resp("wrong url", 401)

    @permission_check
    def patch(self, table, uid):
        try:
            if table == "company_info":
                # 修改数据的某一些字段
                form = Change_CompanyInfoForm(request.form)
                if form.validate():
                    data = json.loads(form.data_json.data)
                    one = {key:value for key,value in data.items()}
                    if form.db_id:
                        query = company_info.query.filter_by(id=form.db_id).update(one)
                    else:
                        query = company_info.query.filter_by(web_id=form.web_id, from_web=form.from_web).update(one)
                    db.session.commit()
                    return succeed_resp()
                else:
                    for error_filed, error_message in form.errors.items():
                        if isinstance(error_message, list) and error_message:
                            error_message = error_message[0]
                        return failed_resp("%s: %s" % (error_filed, error_message), 400)
            elif table == "job_info":
                form = Change_JobInfoForm(request.form)
                if form.validate():
                    data = json.loads(form.data_json.data)
                    one = {key:value for key,value in data.items()}
                    if form.db_id:
                        query = job_info.query.filter_by(id=form.db_id).update(one)
                    else:
                        query = job_info.query.filter_by(web_id=form.web_id, from_web=form.from_web).update(one)
                    db.session.commit()
                    return succeed_resp()
                else:
                    for error_filed, error_message in form.errors.items():
                        if isinstance(error_message, list) and error_message:
                            error_message = error_message[0]
                        return failed_resp("%s: %s" % (error_filed, error_message), 400)
            else:
                return failed_resp("wrong url", 401)
        except:
            return failed_resp("error", 500)


lagou_api.add_resource(lagouResource,"/api/lagou/<string:table>")
