import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import VALID_CHARACTERS
from .models import URLMap
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_url = data.get('custom_id')
    if short_url != '' and short_url is not None:
        if (re.fullmatch(VALID_CHARACTERS, short_url) is None or len(short_url) > 16):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    else:
        short_url = get_unique_short_id()
    if URLMap.query.filter_by(short=short_url).first() is not None:
        raise InvalidAPIUsage(f'Имя "{short_url}" уже занято.')
    url = URLMap(
        original=data['url'],
        short=short_url,
    )
    db.session.add(url)
    db.session.commit()
    return jsonify({
        'url': url.original,
        'short_link': request.host_url + url.short,
    }), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
