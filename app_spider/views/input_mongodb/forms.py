  # -*- coding: utf8 -*-
from app_spider import mongo_client
from flask import current_app
import traceback
import json


def check_company(data, extend_rule, table):
    web_id = data["web_id"]
    from_web = data["from_web"]
    query = mongo_client.db[table].find({"web_id":web_id,"from_web":from_web})
    if query.count() == 0:
        return True
    else:
        current_app.logger.warning("table:{table}, web_id:{web_id}, from_web:{from_web} 数据已存在".format(table=table, web_id=str(web_id), from_web=str(from_web)))
        return False

rule_dic = {
    "company":check_company,
    "job":check_company,
}

def check_form(form, table):
    # 检测table是否存在
    if table not in mongo_client.db.collection_names():
        current_app.logger.warning("table:{table} 不存在".format(table=table))
        return {}, {}, False
    # 检测form结构是否规范
    if "relation" not in form.keys() or "data" not in form.keys() or "rule" not in form.keys():
        current_app.logger.warning("form:{form} 字段错误".format(form=str(form)))
        return {}, {}, False


    try:
        relation = json.loads(form.get("relation"))
        data = json.loads(form.get("data"))
        rule = json.loads(form.get('rule'))
        # 检测relation, data, rule的结构是否正确
        if type(relation) != list or type(data) != dict or type(rule) != dict:
            current_app.logger.warning("form:{form} 结构错误".format(form=str(form)))
            return {}, {}, False

        # 检查数据
        classify = rule["classify"]
        if not rule_dic[classify](data, rule, table):
            return {}, {}, False

        return relation, data, True
    except:
        current_app.logger.warning(traceback.format_exc())
        return {}, {}, False
