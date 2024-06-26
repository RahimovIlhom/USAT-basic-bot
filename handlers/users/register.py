import asyncio
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove

from keyboards.default import phone_button, id_card_button, invitation_button
from loader import dp, db
from states import RegisterStatesGroup
from utils.db_api import create_certificate
from utils.db_api.telegraph_send import photo_link


@dp.message_handler(state=RegisterStatesGroup.fullname)
async def fullname_input(msg: types.Message, state: FSMContext) -> None:
    await state.set_data({'fullname': msg.text})
    await msg.answer("Endi pastdagi tugmani bosib, telefon raqamingizni yuboring",
                     reply_markup=phone_button)
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.phone, content_types=ContentType.CONTACT)
async def contact_input(msg: types.Message, state: FSMContext) -> None:
    await state.update_data({'phone': msg.contact.phone_number})
    await msg.answer("Maktabingiz raqamini kiriting", reply_markup=ReplyKeyboardRemove())
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.phone)
async def err_contact_input(msg: types.Message) -> None:
    await msg.answer("Iltimos, pastdagi tugmani bosib, telefon raqamingizni yuboring",
                     reply_markup=phone_button)


@dp.message_handler(state=RegisterStatesGroup.school)
async def contact_input(msg: types.Message, state: FSMContext) -> None:
    await state.update_data({'school': msg.text})
    image_id_card_url = await db.get_active_image_url('id_card')
    if not image_id_card_url:
        image_id_card_url = await photo_link('data/images/id_card.jpg')
        await db.add_image_url(image_id_card_url, name='id_card')
    info = ("ID-kartangizdagi Shaxsiy raqamingizni kiriting. ID-karta olmagan bo’lsangiz pastda “Hali ID-karta "
            "olmaganman” tugmasini bosing.")
    await msg.answer_photo(image_id_card_url, caption=info, reply_markup=id_card_button)
    await RegisterStatesGroup.next()


@dp.message_handler(state=RegisterStatesGroup.pinfl)
async def contact_input(msg: types.Message, state: FSMContext) -> None:
    try:
        await state.update_data({'pinfl': msg.text})
        data = await state.get_data()
        await state.reset_data()
        await state.finish()
        info = ("Tabriklaymiz, siz ro'yxatdan muvaffaqiyatli o'tdingiz! Universitetga borganda taklifnomani "
                "ko'rsatishingiz kifoya.\n\n"
                "Taklifnomani quyidagi tugma orqali yuklab olishingiz mumkin! 👇")
        await msg.answer(info, reply_markup=invitation_button)
        invitation_image_path = await create_certificate(msg.from_user.id, data.get('fullname'), data.get('school'))
        invitation_image_url = await photo_link(invitation_image_path)
        data.update({'invitation': invitation_image_url, 'tg_id': msg.from_user.id})
        await db.add_or_update_lid(**data)
    except Exception as e:
        await msg.answer(f"An error occurred: {e}")
    finally:
        try:
            os.remove(invitation_image_path)
        except Exception as e:
            print(f"Failed to delete image file: {e}")


@dp.message_handler(text="📥 Taklifnomani yuklab olish")
async def contact_input(msg: types.Message, state: FSMContext) -> None:
    invitation_image_fullname = await db.get_lid_invitation_image(msg.from_user.id)
    info = ("⚡️ Hurmatli {}! Bizni sizga yana bitta taklifimiz bor.\n\nUniversitetda grant asosida "
            "bepul ta’lim olishni yoki 15 million so’mgacha vaucher yutib olishni xohlaysizmi? O’zingizni test "
            "sinovlarida sinab ko’rmoqchimisiz? Unda “Fan javohirlari” olimpiadasi aynan siz uchun! "
            "\n\n@FanJavohirlaribot telegram-botida ro’yxatdan o’ting, imtihonda ishtirok eting va grant, "
            "vaucher hamda boshqa qimmatbaho sovg’alarni yutib olish imkoniyatini qo’lga kiriting!\n\n✅ Olimpiadaga "
            "ro’yxatdan o’tish 👉 @FanJavohirlaribot\n\n✅ “Fan javohirlari” kanali 👉 @FanJavohirlari")
    if invitation_image_fullname:
        await msg.answer_photo(invitation_image_fullname[0], caption="Sizning taklifnomangiz")
        await asyncio.sleep(3)
        await msg.answer(info.format(invitation_image_fullname[1]))
    else:
        await msg.answer("Taklifnoma topilmadi! Qayta urinib ko'ring.")
