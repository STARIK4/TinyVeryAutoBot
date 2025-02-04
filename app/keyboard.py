from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

connect = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подключить аккаунт➕',callback_data='connected')],
])

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Запустить🚀',callback_data='run')],
    [InlineKeyboardButton(text='Остановить🛑',callback_data='stop')],
    [InlineKeyboardButton(text='Добавить аккаунт✅',callback_data='account')],
    [InlineKeyboardButton(text='Настройки времени(Обязательно)⚙️',callback_data='setting')],
    [InlineKeyboardButton(text='Удалить аккаунт❌',callback_data='del_account')],
    [InlineKeyboardButton(text='Список аккаунтов📋',callback_data='list_account')],
])  

set = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сбора пыли🌪️',callback_data='dust')],
    [InlineKeyboardButton(text='Сбора звезд✨',callback_data='stars')],
])










