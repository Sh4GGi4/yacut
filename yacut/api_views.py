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
        url_map = URLMap.create(data['url'], data.get('custom_id'))
    except URLMapError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(
        url=url_map.original, short_link=url_map.get_short_url()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(ID_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify(url=url_map.original), HTTPStatus.OK
