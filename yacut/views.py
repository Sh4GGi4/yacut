import aiohttp
from flask import flash, redirect, render_template

from . import app
from .forms import FilesForm, URLMapForm
from .models import URLMap, URLMapError
from .yandex_disk import async_upload_files_to_yandex_disk

UPLOAD_FAILED_MESSAGE = 'Не удалось загрузить файлы на Яндекс Диск'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(form.original_link.data, form.custom_id.data)
    except URLMapError as error:
        flash(str(error))
        return render_template('index.html', form=form)
    return render_template(
        'index.html', form=form, short_url=url_map.get_short_url()
    )


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FilesForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    try:
        urls = await async_upload_files_to_yandex_disk(form.files.data)
    except aiohttp.ClientError:
        flash(UPLOAD_FAILED_MESSAGE)
        return render_template('files.html', form=form)
    return render_template(
        'files.html',
        form=form,
        files=[
            (file.filename, URLMap.create(url).get_short_url())
            for file, url in zip(form.files.data, urls)
        ],
    )


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
