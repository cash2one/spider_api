  # -*- coding: utf8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField
from wtforms.validators import Optional, InputRequired


def check_data(form, table, db_id=None):
    if db_id:
        query = table.query.filter_by(id=db_id).first()
        if query:
            return True
        else:
            return False
    web_id = form.get("web_id", "")
    from_web = form.get("from_web", "")
    query = table.query.filter_by(web_id=web_id, from_web=from_web).first()
    if query:
        return True
    else:
        return False


def split_form(form, table):
    key_list = table.get_key_list()
    company_form = {key:form.get(key,"") for key in key_list}
    ex_key_list = set(form.keys()) - set(key_list)
    company_ex_form = {key:form.get(key,"") for key in ex_key_list}
    return company_form, company_ex_form

def split_form_in_change(form,table):
    key_list = table.get_key_list()
    company_form = {key:form.get(key,"") for key in key_list if form.get(key,"")}
    ex_key_list = set(form.keys()) - set(key_list)
    company_ex_form = {key:form.get(key,"") for key in ex_key_list if form.get(key,"")}
    return company_form, company_ex_form
