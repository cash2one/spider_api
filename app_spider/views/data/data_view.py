from flask import Blueprint, request, render_template, session
from sqlalchemy import func
import json

from app_spider.views.common.view_decorators import session_check
from app_spider.models import *
from app_spider.views.common.view_decorators import *
data_view = Blueprint("data_view", __name__)


@data_view.route("/index", methods=["GET"], endpoint='index')
@session_check()
def index():
    return render_template("index/index.html")

@data_view.route("/index/total_data", methods=["GET"], endpoint='total_data')
@session_check()
def index_totaldata():
    uid = session["uid"]
    level = session["level"]
    job_count = job_info.query.filter_by(status=1).count()
    company_count = company_info.query.filter_by(status=1).count()

    job_query = job_info.query.\
                with_entities(func.count(job_info.id).label("count"),job_info.from_web).\
                filter_by(status=1).\
                group_by(job_info.from_web).all()

    company_query = company_info.query.\
                    with_entities(func.count(company_info.id).label("count"),company_info.from_web).\
                    filter_by(status=1).\
                    group_by(company_info.from_web).all()
    data = {
        "level":level,
        "job_count":job_count,   # 职位数
        "company_count":company_count, # 公司数
        "job_query":[{"from_web":i.from_web,"count":i.count} for i in job_query], # 每个网站的职位数
        "company_query":[{"from_web":i.from_web,"count":i.count} for i in company_query] # 每个网站的公司数
    }
    if level == "1":
        user_count = spider_user.query.filter_by(status=1).count()
        data["user_count"] = user_count # 爬虫数
    return json.dumps(data)
