from flask import Blueprint, request, render_template
from app_spider.views.common.view_decorators import session_check
data_view = Blueprint("data_view", __name__)


@data_view.route("/index", methods=["GET"])
def index():
    return render_template("index/index.html")
