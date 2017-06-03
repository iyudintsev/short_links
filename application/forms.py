from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import URL


class GenerateShortUrlForm(FlaskForm):
    url = StringField('Please, input url', validators=[URL(require_tld=False)],
                      filters=[lambda x: x.strip() if x else None])
