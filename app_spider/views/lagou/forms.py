  # -*- coding: utf8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField
from wtforms.validators import Optional, InputRequired


class InfoForm(Form):
    web_id = StringField(validators = [InputRequired()])
    from_web = StringField(validators = [InputRequired()])
    status = IntegerField(validators = [InputRequired()], default=0)


class CompanyInfoForm(InfoForm):
    name = StringField(validators = [InputRequired()])
    web_url = StringField(validators = [InputRequired()])
    boss = StringField()
    category = StringField()
    level = StringField()
    people_number = StringField()
    location = StringField()
    description = StringField()
    company_url = StringField()
    rate = StringField()

class JobInfoForm(InfoForm):
    name = StringField(validators = [InputRequired()])
    web_url = StringField(validators = [InputRequired()])
    company_id = IntegerField(validators = [InputRequired()])
    salary = StringField()
    job_year = StringField()
    education = StringField()
    employee_type = StringField()

class Change_CompanyInfoForm(InfoForm):
    db_id = IntegerField()
    data_json = StringField(validators = [InputRequired()])

class Change_JobInfoForm(InfoForm):
    db_id = IntegerField()
    data_json = StringField(validators = [InputRequired()])
