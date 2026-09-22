import asyncio
from urllib.parse import unquote

import aiohttp

from . import app

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}


async def upload_file_and_get_url(session, file):
    """Загружает файл на Яндекс Диск и возвращает ссылку на скачивание."""
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params={'path': f'app:/{file.filename}', 'overwrite': 'True'},
    ) as response:
        upload_url = (await response.json())['href']
    async with session.put(upload_url, data=file.read()) as response:
        location = unquote(response.headers['Location'])
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': location.removeprefix('/disk')},
    ) as response:
        return (await response.json())['href']


async def async_upload_files_to_yandex_disk(files):
    """Загружает файлы на Яндекс Диск одновременно."""
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        return await asyncio.gather(
            *(upload_file_and_get_url(session, file) for file in files)
        )
