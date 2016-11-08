  # -*- coding: utf8 -*-
from app_spider import mongo_client
from flask import current_app
import traceback
import json
import time


def insert_company(data, extend_rule, table, relation, uid):
    '''
        1. 校验data, 是否已存在重复的数据
        2. 根据relation里的条件, 找到 关联的 数据, 保存到one_relation变量中
        3. 插入数据, 顺便将one_relation加入relation字段中
        4. 将当前数据的_id, 插入到 关联的 数据中的relation字段中
        5. return obj_id, 状态(True/False), 信息
    '''
    # 检验data, 通过web_id, from_web查看数据是否有重复
    web_id = data["web_id"]
    from_web = data["from_web"]
    query = mongo_client.db[table].find({"web_id":web_id,"from_web":from_web})
    if query.count() != 0:
        current_app.logger.warning("table:{table}, web_id:{web_id}, from_web:{from_web} 数据已存在".format(table=table, web_id=str(web_id), from_web=str(from_web)))
        return None, False,  "table:{table}, web_id:{web_id}, from_web:{from_web} 数据已存在".format(table=table, web_id=str(web_id), from_web=str(from_web))
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
    data['relation'] = one_relation
    data['uid'] = uid
    obj_id = mongo_client.db[table].insert_one(data).inserted_id

    # 在关联数据中, 插入当前数据_id

    for table_name, value in one_relation.items():
        query_count = mongo_client.db[table_name].update({"_id":{"$in":value}}, {"$push":{"relation.{table}".format(table=table):obj_id}}, multi=True)

    return obj_id, True, 'OK'

rule_dic = {
    "company":insert_company,
    "job":insert_company,
}

def check_form(form, table):
    '''
        校验form: 返回值 relation, data, rule, status, message
    '''
    # 检测table是否存在
    if table not in mongo_client.db.collection_names():
        current_app.logger.warning("table:{table} 不存在".format(table=table))
        return {}, {}, {}, False, "table:{table} 不存在".format(table=table)

    # 检测form结构是否规范
    if "relation" not in form.keys() or "data" not in form.keys() or "rule" not in form.keys():
        current_app.logger.warning("form:{form} 字段错误".format(form=str(form)))
        return {}, {}, {}, False, "form:{form} 字段错误".format(form=str(form))


    try:
        relation = json.loads(form.get("relation"))
        data = json.loads(form.get("data"))
        rule = json.loads(form.get('rule'))
        # 检测relation, data, rule的结构是否正确
        if type(relation) != list or type(data) != dict or type(rule) != dict:
            current_app.logger.warning("form:{form} 结构错误".format(form=str(form)))
            return {}, {}, {}, False, "form:{form} 结构错误".format(form=str(form))

        if "classify" not in rule or rule["classify"] not in rule_dic.keys():
            current_app.logger.warning("rule:{rule} 有误".format(rule=str(rule)))
            return {}, {}, {}, False, "rule:{rule} 有误".format(rule=str(rule))

        return relation, data, rule, True, "OK"
    except:
        current_app.logger.warning(traceback.format_exc())
        return {}, {}, {}, False, traceback.format_exc()
