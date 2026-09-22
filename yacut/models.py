import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from .constants import (DUPLICATE_SHORT_MESSAGE, INVALID_SHORT_MESSAGE,
                        LONG_ORIGINAL_MESSAGE, ORIGINAL_MAX_LENGTH,
                        RESERVED_SHORTS, SHORT_AUTO_LENGTH, SHORT_CHARS,
                        SHORT_GENERATION_ATTEMPTS,
                        SHORT_GENERATION_FAILED_MESSAGE, SHORT_MAX_LENGTH,
                        SHORT_PATTERN)


class URLMapError(Exception):
    """Ошибка создания короткой ссылки."""


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
    def is_taken(short):
        return short in RESERVED_SHORTS or URLMap.get(short) is not None

    @staticmethod
    def get_unique_short():
        for _ in range(SHORT_GENERATION_ATTEMPTS):
            short = ''.join(random.choices(SHORT_CHARS, k=SHORT_AUTO_LENGTH))
            if not URLMap.is_taken(short):
                return short
        raise URLMapError(SHORT_GENERATION_FAILED_MESSAGE)

    @staticmethod
    def create(original, short=None):
        if len(original) > ORIGINAL_MAX_LENGTH:
            raise URLMapError(LONG_ORIGINAL_MESSAGE)
        if not short:
            short = URLMap.get_unique_short()
        elif (
            len(short) > SHORT_MAX_LENGTH
            or not re.fullmatch(SHORT_PATTERN, short)
        ):
            raise URLMapError(INVALID_SHORT_MESSAGE)
        elif URLMap.is_taken(short):
            raise URLMapError(DUPLICATE_SHORT_MESSAGE)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def get_short_url(self):
        return url_for('redirect_view', short=self.short, _external=True)
