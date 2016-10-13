from flask import Blueprint, request, render_template, session, redirect, url_for
from app_spider.models import db, spider_user
from app_spider.views.common.utils import *

login_view = Blueprint("login_view", __name__)

@login_view.route("/", methods=["GET", "POST"])
@login_view.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("level",""):
            return redirect(url_for("data_view.index"))
        return render_template("login/login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        query = spider_user.query.filter_by(name=username, password=password, status=1).first()
        if not query:
            return succeed_resp(result=0)
        else:
            session["uid"] = query.uid
            session["username"] = username
            session["level"] = query.level
            return succeed_resp(result=1)

@login_view.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("login/login.html")
