from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🎁 Каталог подарков", callback_data="catalog"))
    builder.row(types.InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help"))
    
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n"
        "Я бот для продажи Telegram подарков. Выбери интересующий раздел:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(lambda c: c.data == "help")
async def process_help(callback: types.CallbackQuery):
    await callback.message.answer(
        "Как купить подарок:\n"
        "1. Выберите подарок в каталоге.\n"
        "2. Переведите деньги на карту.\n"
        "3. Пришлите чек об оплате.\n"
        "4. После проверки мы отправим вам подарок!"
    )
    await callback.answer()
