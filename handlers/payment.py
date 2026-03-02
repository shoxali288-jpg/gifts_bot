from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import GIFTS, CARD_NUMBER, ADMIN_ID

router = Router()

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery):
    gift_id = int(callback.data.split("_")[1])
    gift = next((g for g in GIFTS if g["id"] == gift_id), None)
    
    if not gift:
        await callback.answer("Подарок не найден.")
        return

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check_pay_{gift_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Отмена", callback_data="catalog"))

    await callback.message.edit_text(
        f"Вы выбрали: *{gift['name']}*\n"
        f"К оплате: `{gift['price']} руб.`\n\n"
        f"💳 Переведите деньги на карту:\n`{CARD_NUMBER}`\n\n"
        "После перевода нажмите кнопку ниже и пришлите скриншот чека.",
        parse_mode="Markdown",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("check_pay_"))
async def check_payment(callback: types.CallbackQuery):
    gift_id = int(callback.data.split("_")[2])
    await callback.message.answer("Пожалуйста, пришлите скриншот чека об оплате одним сообщением.")
    # Here we should use a state machine (FSM) for a real bot, 
    # but for simplicity we'll just wait for the next photo from this user.
    await callback.answer()

@router.message(F.photo)
async def handle_receipt(message: types.Message, bot: Bot):
    # In a real bot, you'd check if the user is in the "waiting for receipt" state
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin_confirm_{message.from_user.id}"))
    builder.row(types.InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{message.from_user.id}"))

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=f"🔔 Новый платеж от @{message.from_user.username} (ID: {message.from_user.id})\n"
                "Проверьте поступление средств и нажмите кнопку ниже.",
        reply_markup=builder.as_markup()
    )
    await message.answer("Спасибо! Ваш чек отправлен администратору на проверку. Ожидайте подтверждения.")

@router.callback_query(F.data.startswith("admin_confirm_"))
async def admin_confirm(callback: types.CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет прав.")
        return
        
    user_id = int(callback.data.split("_")[2])
    await bot.send_message(user_id, "🎉 Оплата подтверждена! Сейчас мы отправим вам подарок (или свяжемся с вами).")
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n✅ ОПЛАЧЕНО")
    await callback.answer("Подтверждено")

@router.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: types.CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет прав.")
        return

    user_id = int(callback.data.split("_")[2])
    await bot.send_message(user_id, "❌ Оплата отклонена. Если возникла ошибка, свяжитесь с поддержкой.")
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n❌ ОТКЛОНЕНО")
    await callback.answer("Отклонено")
