from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import ORIGINAL_MAX_LENGTH, SHORT_MAX_LENGTH, SHORT_PATTERN
from .models import INVALID_SHORT_MESSAGE

ORIGINAL_LINK_LABEL = 'Длинная ссылка'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
FILES_LABEL = 'Файлы'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
NO_FILES_MESSAGE = 'Выберите хотя бы один файл'
CREATE_BUTTON = 'Создать'
UPLOAD_BUTTON = 'Загрузить'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_MESSAGE),
            Length(max=ORIGINAL_MAX_LENGTH),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Optional(),
            Length(max=SHORT_MAX_LENGTH, message=INVALID_SHORT_MESSAGE),
            Regexp(SHORT_PATTERN, message=INVALID_SHORT_MESSAGE),
        ],
    )
    submit = SubmitField(CREATE_BUTTON)


class FilesForm(FlaskForm):
    files = MultipleFileField(
        FILES_LABEL,
        validators=[FileRequired(message=NO_FILES_MESSAGE)],
    )
    submit = SubmitField(UPLOAD_BUTTON)
