from flask import Blueprint, request
from flask_restful import Resource, Api
from app_spider.models import db, company_info, job_info
from app_spider.views.common.view_decorators import permission_check
from app_spider.views.common.utils import *
lagou_api_view = Blueprint("lagou_api_view", __name__)
lagou_api = Api(lagou_api_view)

class lagouResource(Resource):
    @permission_check
    def post(self, table):
        if table == "company_info":
            one = {
                "web_id":request.form.get("web_id"),
                "name":request.form.get("name"),
                "boss":request.form.get("boss"),
                "category":request.form.get("category"),
                "level":request.form.get("level"),
                "people_number":request.form.get("people_number"),
                "location":request.form.get("location"),
                "description":request.form.get("description"),
                "web_url":request.form.get("web_url"),
                "company_url":request.form.get("company_url"),
                "rate":request.form.get("rate"),
                "from_web":request.form.get("from_web"),
                "status":request.form.get("status",0)
            }
            one = company_info(one)
            db.session.add(one)
            db.session.commit()
            return succeed_resp()
        elif table == "job_info":
            one = {
                "web_id":request.form.get("web_id"),
                "company_id":request.form.get("company_id"),
                "name":request.form.get("name"),
                "salary":request.form.get("salary"),
                "job_year":request.form.get("job_year"),
                "education":request.form.get("education"),
                "employee_type":request.form.get("employee_type"),
                "web_url":request.form.get("web_url"),
                "status":request.form.get("status",0),
                "from_web":request.form.get("from_web"),
            }
            one = job_info(one)
            db.session.add(one)
            db.session.commit()
            return succeed_resp()
        else:
            return failed_resp("wrong url", 401)


lagou_api.add_resource(lagouResource,"/api/lagou/<string:table>")
