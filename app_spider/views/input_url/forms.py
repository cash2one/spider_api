  # -*- coding: utf8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField
from wtforms.validators import Optional, InputRequired


class url_tableForm(Form):
    url = StringField(validators = [InputRequired()])
    from_web = StringField(validators = [InputRequired()])
    classify = StringField(default="0")

class url_tablechangeForm(url_tableForm):
    db_id = IntegerField(validator = [InputRequired()])
    status = IntegerField(validators=[InputRequired()], default=1)
    
