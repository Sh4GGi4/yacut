from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (INVALID_SHORT_MESSAGE, ORIGINAL_MAX_LENGTH,
                        SHORT_MAX_LENGTH, SHORT_PATTERN)


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=ORIGINAL_MAX_LENGTH),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=SHORT_MAX_LENGTH, message=INVALID_SHORT_MESSAGE),
            Regexp(SHORT_PATTERN, message=INVALID_SHORT_MESSAGE),
        ],
    )
    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[FileRequired(message='Выберите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')
