import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from .constants import (ORIGINAL_MAX_LENGTH, REDIRECT_VIEW, RESERVED_SHORTS,
                        SHORT_AUTO_LENGTH, SHORT_CHARS,
                        SHORT_GENERATION_ATTEMPTS, SHORT_MAX_LENGTH,
                        SHORT_PATTERN)

INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
LONG_ORIGINAL_MESSAGE = (
    f'Ссылка длиннее {ORIGINAL_MAX_LENGTH} символов'
)
SHORT_GENERATION_FAILED_MESSAGE = (
    f'Не удалось подобрать свободную короткую ссылку за '
    f'{SHORT_GENERATION_ATTEMPTS} попыток'
)


class URLMapError(Exception):
    """Запись создать не удалось: данные отклонены или ссылка занята."""


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def is_taken(short):
        return short in RESERVED_SHORTS or URLMap.get(short)

    @staticmethod
    def get_unique_short():
        for _ in range(SHORT_GENERATION_ATTEMPTS):
            short = ''.join(random.choices(SHORT_CHARS, k=SHORT_AUTO_LENGTH))
            if not URLMap.is_taken(short):
                return short
        raise URLMapError(SHORT_GENERATION_FAILED_MESSAGE)

    @staticmethod
    def create(original, short=None, validated=False, commit=True):
        """Создаёт запись. validated=True пропускает проверки формы."""
        if not validated and len(original) > ORIGINAL_MAX_LENGTH:
            raise URLMapError(LONG_ORIGINAL_MESSAGE)
        if not short:
            short = URLMap.get_unique_short()
        else:
            if not validated and (
                len(short) > SHORT_MAX_LENGTH
                or not re.fullmatch(SHORT_PATTERN, short)
            ):
                raise URLMapError(INVALID_SHORT_MESSAGE)
            if URLMap.is_taken(short):
                raise URLMapError(DUPLICATE_SHORT_MESSAGE)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    @staticmethod
    def create_all(originals):
        """Создаёт записи пакетом: коммит один на весь пакет."""
        url_maps = [
            URLMap.create(original, commit=False) for original in originals
        ]
        db.session.commit()
        return url_maps

    def get_short_url(self):
        return url_for(REDIRECT_VIEW, short=self.short, _external=True)
