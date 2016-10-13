from flask import Blueprint, request
from app_spider.views.common.view_decorators import session_check
data_view = Blueprint("data_view", __name__)
