from io import BytesIO
import aiohttp
from aiogram import types
from loader import bot


async def photo_link(photo: types.photo_size.PhotoSize) -> str:
    with await photo.download(BytesIO()) as file:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=file,
        )
        print('form', form)
        async with bot.session.post('https://telegra.ph/upload', data=form) as response:
            print('response', response)
            print('response_status', response.status)
            img_src = await response.json()

    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link


async def video_link(video: types.video.Video) -> str:
    with await video.download(BytesIO()) as file:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=file,
        )
        async with bot.session.post('https://telegra.ph/upload', data=form) as response:
            video_src = await response.json()

    link = 'http://telegra.ph/' + video_src[0]["src"]
    return link
