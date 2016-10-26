from flask import Blueprint, request
from flask_restful import Resource, Api
from app_spider.models import db, url_table
from app_spider.views.common.view_decorators import permission_check
from app_spider.views.common.utils import *
from .forms import *
import json

input_api_view = Blueprint("input_api_view", __name__)
input_api = Api(input_api_view)

def check_input(form, table):
    web_id = form.web_id
    from_web = form.form_web
    query = table.query.filter_by(web_id=web_id, from_web=from_web).first()
    if query:
        return False
    else:
        return True

class inputResource(Resource):
    @permission_check
    def get(self, uid):
        query = url_table.query.filter_by(uid=uid).with_lockmode("update").first()
        data = {
            "url":query.url,
            "from_web":query.from_web,
            "classify":query.classify,
            "db_id":query.id
        }
        query.status = 2
        db.session.commit()
        return succeed_resp(url=data['url'],from_web=data['from_web'],classify=data['classify'],db_id=data["db_id"])

    @permission_check
    def post(self, uid):
        form = url_tableForm(request.form)
        if form.validate():
            one = {
                "url":form.url.data,
                "from_web":form.from_web.data,
                "classify":form.classify.data,
                "uid":uid
            }
            one = url_table(one)
            db.session.add(one)
            db.session.flush()
            db_id = one.id
            return succeed_resp(db_id=db_id)
        else:
            for error_filed, error_message in form.errors.items():
                if isinstance(error_message, list) and error_message:
                    error_message = error_message[0]
                return failed_resp("%s: %s" % (error_filed, error_message), 400)

    @permission_check
    def patch(self, uid):
        try:
            form = url_tablechangeForm(request.form)
            if form.validate():
                query = url_table.query.filter_by(id=form.db_id.data).update(status=form.status.data)
                db.session.commit()
                return succeed_resp()
            else:
                for error_filed, error_message in form.errors.items():
                    if isinstance(error_message, list) and error_message:
                        error_message = error_message[0]
                    return failed_resp("%s: %s" % (error_filed, error_message), 400)
        except:
            return failed_resp("error", 500)


input_api.add_resource(inputResource,"/api/input")
