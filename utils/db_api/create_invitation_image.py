import os
import asyncio
import datetime

from PIL import Image, ImageDraw, ImageFont

from utils.db_api.transliterate import to_latin


async def create_certificate(user_id, fullname: str, school, created_date=datetime.datetime.now().date()):
    img = Image.open(f'data/images/invitation.jpg')

    draw = ImageDraw.Draw(img)

    font_path1 = 'data/fonts/KaushanScript-Regular.otf'
    font_path2 = 'data/fonts/Montserrat-Regular.otf'
    font1 = ImageFont.truetype(font_path1, 200)
    font2 = ImageFont.truetype(font_path2, 100)

    text_color = (255, 255, 255)
    if not fullname.isascii():
        fullname = to_latin(fullname)

    text_bbox = draw.textbbox((1150, 2300), fullname, font=font1)
    text_width = text_bbox[2] - text_bbox[0]
    text_position = (1150 - text_width / 2, 2300)
    draw.text(text_position, fullname, font=font1, fill=text_color)  # fullname
    draw.text((1590, 3770), str(school), font=font2, fill=text_color)  # school num
    draw.text((1590, 3935), str(created_date), font=font2, fill=text_color)  # date

    os.makedirs("data/certificates/", exist_ok=True)

    save_image_name = f"data/certificates/{user_id}.jpg"
    img.save(save_image_name)
    return save_image_name
