from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamingizni yuboring", request_contact=True)],
    ],
    resize_keyboard=True
)


id_card_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Hali ID-karta olmaganman")],
    ],
    resize_keyboard=True
)


invitation_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📥 Taklifnomani yuklab olish")],
    ],
    resize_keyboard=True
)
