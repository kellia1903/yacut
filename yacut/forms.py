from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import Length, Optional, Regexp, URL

from .constants import VALID_CHARACTERS


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            URL(message='Некоректная ссылка'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(min=0, max=16),
            Optional(strip_whitespace=False),
            Regexp(VALID_CHARACTERS, message='Некорректные символы'),
        ]
    )
    submit = SubmitField('Создать')
