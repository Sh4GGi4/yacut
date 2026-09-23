import asyncio
from http import HTTPStatus
from urllib.parse import unquote

import aiohttp

from settings import Config

AUTH_HEADERS = {'Authorization': f'OAuth {Config.DISK_TOKEN}'}
RESOURCES_URL = f'{Config.DISK_API_URL}disk/resources'
REQUEST_UPLOAD_URL = f'{RESOURCES_URL}/upload'
DOWNLOAD_LINK_URL = f'{RESOURCES_URL}/download'
FOLDER_EXISTS_STATUSES = (HTTPStatus.CREATED, HTTPStatus.CONFLICT)


class UploadFolderNotFoundError(Exception):
    """На Диске ещё нет папки, в которую сервис складывает файлы."""


async def request_upload_link(session, path):
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params={'path': path, 'overwrite': 'True'},
    ) as response:
        if response.status == HTTPStatus.CONFLICT:
            raise UploadFolderNotFoundError(path)
        return (await response.json())['href']


async def create_upload_folder(session):
    async with session.put(
        RESOURCES_URL,
        headers=AUTH_HEADERS,
        params={'path': f'app:/{Config.DISK_UPLOAD_FOLDER}'},
    ) as response:
        if response.status not in FOLDER_EXISTS_STATUSES:
            response.raise_for_status()


async def upload_file_and_get_url(session, file):
    """Загружает файл на Яндекс Диск и возвращает ссылку на скачивание."""
    path = f'app:/{Config.DISK_UPLOAD_FOLDER}/{file.filename}'
    try:
        upload_url = await request_upload_link(session, path)
    except UploadFolderNotFoundError:
        await create_upload_folder(session)
        upload_url = await request_upload_link(session, path)
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
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(upload_file_and_get_url(session, file) for file in files)
        )
