from flask import flash, redirect, render_template

from . import app
from .constants import REDIRECT_VIEW
from .forms import FilesForm, URLMapForm
from .models import URLMap, URLMapError
from .yandex_disk import async_upload_files_to_yandex_disk

INDEX_TEMPLATE = 'index.html'
FILES_TEMPLATE = 'files.html'
UPLOAD_FAILED_MESSAGE = 'Не удалось загрузить файлы на Яндекс Диск: {error}'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_TEMPLATE, form=form)
    try:
        return render_template(
            INDEX_TEMPLATE,
            form=form,
            short_url=URLMap.create(
                form.original_link.data,
                form.custom_id.data,
                validated=True,
            ).get_short_url(),
        )
    except URLMapError as error:
        flash(str(error))
        return render_template(INDEX_TEMPLATE, form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FilesForm()
    if not form.validate_on_submit():
        return render_template(FILES_TEMPLATE, form=form)
    try:
        urls = await async_upload_files_to_yandex_disk(form.files.data)
    except Exception as error:
        flash(UPLOAD_FAILED_MESSAGE.format(error=error))
        return render_template(FILES_TEMPLATE, form=form)
    try:
        url_maps = [
            URLMap.create(url, commit=(number == len(urls)))
            for number, url in enumerate(urls, start=1)
        ]
    except URLMapError as error:
        flash(str(error))
        return render_template(FILES_TEMPLATE, form=form)
    return render_template(
        FILES_TEMPLATE,
        form=form,
        files=[
            (file.filename, url_map.get_short_url())
            for file, url_map in zip(form.files.data, url_maps)
        ],
    )


@app.route('/<string:short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    return redirect(URLMap.get(short, or_404=True).original)
