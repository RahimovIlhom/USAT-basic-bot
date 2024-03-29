import aiohttp


async def photo_link(photo: str) -> str:
    async with aiohttp.ClientSession() as session:
        with open(photo, 'rb') as file:
            form = aiohttp.FormData()
            form.add_field('file', file)

            async with session.post('https://telegra.ph/upload', data=form) as response:
                img_src = await response.json()

    link = 'http://telegra.ph' + img_src[0]["src"]
    return link
