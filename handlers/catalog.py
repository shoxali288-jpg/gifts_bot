from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import GIFTS

router = Router()

@router.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    
    for gift in GIFTS:
        builder.row(types.InlineKeyboardButton(
            text=f"{gift['name']} — {gift['price']} руб.", 
            callback_data=f"buy_{gift['id']}"
        ))
    
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="start_menu"))
    
    await callback.message.edit_text(
        "✨ Выберите подарок из списка:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@router.callback_query(F.data == "start_menu")
async def back_to_start(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🎁 Каталог подарков", callback_data="catalog"))
    builder.row(types.InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help"))
    
    await callback.message.edit_text(
        f"Привет, {callback.from_user.full_name}!\n"
        "Я бот для продажи Telegram подарков. Выбери интересующий раздел:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()
