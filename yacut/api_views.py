from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap, URLMapError

EMPTY_BODY_MESSAGE = 'Отсутствует тело запроса'
URL_REQUIRED_MESSAGE = '"url" является обязательным полем!'
ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_BODY_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_MESSAGE)
    try:
        return jsonify(
            url=data['url'],
            short_link=URLMap.create(
                data['url'], data.get('custom_id')
            ).get_short_url(),
        ), HTTPStatus.CREATED
    except URLMapError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    if (url_map := URLMap.get(short)) is None:
        raise InvalidAPIUsage(ID_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify(url=url_map.original), HTTPStatus.OK
