from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command

from keyboards.default import invitation_button
from loader import dp, db
from states import RegisterStatesGroup
from utils.db_api.telegraph_send import photo_link


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext) -> None:
    lid = await db.get_lid(message.from_user.id)
    if lid:
        await message.answer("Siz ro'yxatdan o'tib bo'lgansiz!", reply_markup=invitation_button)
    else:
        if await state.get_state():
            await message.answer("Iltimos, ismingiz va familiyangizni kiriting:",
                                 reply_markup=types.ReplyKeyboardRemove())
            await RegisterStatesGroup.fullname.set()
            return
        await welcome_and_fullname(message)


async def welcome_and_fullname(message: types.Message) -> None:
    welcome_text_1 = ("😃 Fan va texnologiyalar universiteti faoliyati bilan yanada yaqinroq tanishish, "
                      "ta’lim muhitini his qilish va bir kunga o‘zingizni talaba sifatida his qilish imkoniyatini "
                      "qo‘ldan boy bermang! 1-apreldan boshlab har kuni universitetda maktablarning bitiruvchi sinf "
                      "o‘quvchilari uchun “Ochiq eshiklar kuni” tashkil etiladi. \n\n"
                      "🤗Tadbir davomida o’quvchilar uchun universitet bo’ylab ekskursiya o’tkaziladi, eng yangi "
                      "texnika bilan jihozlangan o’quv xonalari, elektron kutubxona va “coworking” markazlari bilan "
                      "tanishtiriladi. O’quvchilar universitet to‘g‘risida barcha savollariga javob olishlari mumkin "
                      "bo’ladi.")
    welcome_text_2 = ("🎭 Shuningdek, tadbirning badiiy qismida universalization QVZ jamoasi barcha o’quvchilar "
                      "uchun maxsus sovg’a sifatida sahna ko’rinishlarini taqdim etishadi.\n\n"
                      "🎁 Tadbir oxirida o'quvchilar orasida qimmatbaho sovg'alar va pullik vaucherlar "
                      "o'ynaladi.\n\n"
                      "Biz “Ochiq eshiklar kuni”da o‘quvchilar, ota-onalar, do‘stlar va oilalarni intiqlik bilan "
                      "kutib qolamiz!\n\n"
                      "📞 Call-markaz: +99878-888-38-88\n📍"
                      " Manzil: Toshkent shahri, Algoritm dahasi, Diydor ko'chasi 71.\n"
                      "📍 Mo'ljal: sobiq Roison binosi\n"
                      "📍 <a href=\"https://yandex.uz/maps/10335/tashkent/?ll=69.163080%2C41.261028&mode=whatshere"
                      "&whatshere%5Bpoint%5D=69.163055%2C41.261021&whatshere%5Bzoom%5D=19.98&z=19\">Lokatsiya</a>\n\n"
                      "📹<a href=\"https://instagram.com/usatuz?igshid=YmMyMTA2M2Y=\">Instagram</a> | "
                      "💬<a href=\"https://t.me/usatuzb\">Telegram</a> | "
                      "📱<a href=\"https://m.facebook.com/usatuz\">Facebook</a> | "
                      "📹<a href=\"https://youtube.com/@Usatuz\">YouTube</a>")

    fullname_text = "Iltimos, ismingiz va familiyangizni kiriting:"
    image_url = await db.get_active_image_url()
    if not image_url:
        image_url = await photo_link('data/images/welcome.jpg')
        await db.add_image_url(image_url)

    try:
        await message.answer_photo(image_url, caption=welcome_text_1)
        await message.answer(welcome_text_2, disable_web_page_preview=True)
    except:
        image_url = await photo_link('data/images/welcome.jpg')
        await message.answer_photo(image_url, caption=welcome_text_1)
        await message.answer(welcome_text_2, disable_web_page_preview=True)

    await message.answer(fullname_text, reply_markup=types.ReplyKeyboardRemove())
    await RegisterStatesGroup.fullname.set()


@dp.message_handler(Command('re_register'))
async def bot_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Iltimos, ismingiz va familiyangizni kiriting:",
                         reply_markup=types.ReplyKeyboardRemove())
    await RegisterStatesGroup.fullname.set()
