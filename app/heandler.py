import asyncio
import random
import app.keyboard as kb
from aiogram import Router,F
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

router = Router()
account_list = {}
running_task = {}
set_collect = {}
set_stars = {}

class Reg(StatesGroup):
    run_account = State()
    stop_account = State()
    set_time_collet_min = State()
    set_time_collet_max = State()
    set_time_stars_min = State()
    set_time_stars_max = State()
    registration_session = State()
    registration_galaxy = State()
    registration_proxy = State()
    delet_account = State()
    
async def start_task(user_id):
        from run import collect,create_stars
        task1 = asyncio.create_task(collect(user_id))
        await asyncio.sleep(random.randint(10,30))
        task2 = asyncio.create_task(create_stars(user_id))
        return task1,task2
        

async def min_c(user_id):
    TIME_MIN_COLLET = set_collect[user_id][0]["set_time_collet_min"]
    return TIME_MIN_COLLET
    
async def max_c(user_id):
    TIME_MAX_COLLET = set_collect[user_id][0]["set_time_collet_max"]
    return TIME_MAX_COLLET

async def min_s(user_id):
    TIME_MIN_CREATE = set_stars[user_id][0]["set_time_stars_min"]
    return TIME_MIN_CREATE
    
async def max_s(user_id):
    TIME_MAX_CREATE = set_stars[user_id][0]["set_time_stars_max"]
    return TIME_MAX_CREATE

@router.message(CommandStart())
async def start(message:Message):
    user_id = message.from_user.id
    await message.answer_photo(
    photo='AgACAgIAAxkBAAOFZ5T2qeQg51WoZiDVfaefyK1eMYcAAjzoMRutq6hICC13SNTmCgABAQADAgADeAADNgQ',
    caption=f'''
    <b>Добро пожаловать в TinyFarmBot</b>👋
    
    <b>Софт для автоматизации работы с TinyVery.</b>
    
    ▪️<b>Работа через session и galaxy_id</b>
    ▪️<b>Возможность подключить прокси</b>
    ▪️<b>Ручная настройках времени сбора пыли и создание звезд</b>
    ▪️<b>Автоматический сбор пыли и звезд</b>
    ▪️<b>Никак не касается вашего тг аккаунта</b>
    ''',
    parse_mode='HTML'
    )
    if user_id not in account_list:
        account_list[user_id] = []
    if user_id not in set_collect:
        set_collect[user_id] = []
    if user_id not in set_stars:
        set_stars[user_id] = []
        
#Кнопка "Подключение аккаунтов"
@router.message(Command('menu'))
async def menu(message:Message):
    user_id = message.from_user.id
    await message.answer(text=f'Личный кабинет🖥️\nАкаунтов подключено:{len(account_list[user_id])}',reply_markup=kb.connect)
    
#Переход в "Меню"
@router.callback_query(F.data == 'connected')
async def connectes(callback:CallbackQuery):
    await callback.answer(text='Идет загрузка',)
    await callback.message.edit_text(text='Выберите раздел:',reply_markup=kb.menu)

#Запуск аккаунтов
@router.callback_query(F.data == 'run')
async def start_one(callback:CallbackQuery,state:FSMContext):
    await callback.answer('Последний шаг')
    await state.set_state(Reg.run_account)
    await callback.message.answer('<b>Напишите "run",чтобы запустить!</b>',parse_mode='HTML')

@router.message(Reg.run_account)
async def start_two(message:Message,state:FSMContext):
    await state.update_data(run_account = str(message.text))
    data = await state.get_data()
    user_id = message.from_user.id
    if data["run_account"].lower()== "run":
        if user_id in running_task:
            task = running_task[user_id]
            if not task[0].done() or not task[1].done():
                await message.answer('Tiny уже работает!🤖')    
        elif len(account_list[user_id]) == 0:
            await message.answer('Ты что совсем не видешь,что "Список аккаунтов📋" пуст!')   
        else:
            running_task[user_id] = await start_task(user_id)
            await message.answer('Tiny запущен✅!')
    else:
        await message.answer('Неможет быть такой команды нету!\nЧто бы все заработала ведеите:"run"!')
    await state.clear()
    
#Остановить аккаунт
@router.callback_query(F.data == 'stop')
async def stop_one(callback:CallbackQuery,state:FSMContext):
    await callback.answer('Идет загрузка')
    await state.set_state(Reg.stop_account)
    await callback.message.answer('Введите "stop",если хотите приостановить скрипт')

@router.message(Reg.stop_account)
async def stop_two(message:Message,state:FSMContext):
    await state.update_data(stop_account = message.text)
    data = await state.get_data()
    user_id = message.from_user.id
    if data["stop_account"].lower() == "stop":
        if user_id in running_task:
            tasks = running_task[user_id]

            if not tasks[0].done() or not tasks[1].done():
                tasks[0].cancel()
                tasks[1].cancel()
            try:
                await tasks[0]
                await tasks[1]
            except asyncio.CancelledError:
                pass
            del running_task[user_id]
            await message.answer('Tiny остановлен❌')
        else:
            await message.answer('Да,ну как так,нету активных процессов')
    else:
        await message.answer('Неможет быть такой команды нету!\nЧто бы все заработала ведеите:"stop"!')
    await state.clear()
        
#Кнопка "Добавление аккаунтов"
@router.callback_query(F.data == 'account')
async def add_one_data(callback:CallbackQuery,state: FSMContext):
    await callback.answer(text='Идет загрузка')
    await state.set_state(Reg.registration_session)
    await callback.message.answer(text='<b>Введите свой SESSION:</b>',parse_mode='HTML')
    
@router.message(Reg.registration_session)
async def add_two_data(message:Message,state:FSMContext):
    await state.update_data(registration_session = message.text)
    await state.set_state(Reg.registration_galaxy)
    await message.answer(text='<b>Введите свой GALAXY</b>',parse_mode='HTML')

@router.message(Reg.registration_galaxy)
async def add_tree_data(message:Message,state: FSMContext):
    await state.update_data(registration_galaxy = message.text)
    await state.set_state(Reg.registration_proxy)
    await message.answer(text='<b>Введите свой PROXY</b>\n<b>В формате</b>\n<i>http://user:pass@ip:port</i>\n<b>Если нету PROXY напиши "No"</b>',parse_mode='HTML')

@router.message(Reg.registration_proxy)
async def add_end_data(message:Message,state:FSMContext):
    await state.update_data(registration_proxy = message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    if data["registration_proxy"].lower() == 'no':
        data["registration_proxy"] = None
        account_list[user_id].append(data)
        await message.answer(text=f'Аккаунт успешно добавлен в список')
        await state.clear()
    else:
        account_list[user_id].append(data)
        await message.answer(text=f'Аккаунт успешно добавлен в список')
        await state.clear()

#Настройки
@router.callback_query(F.data == 'setting')
async def setting_one(callback:CallbackQuery):
    await callback.answer('Загрузка')
    await callback.message.edit_text(text='Настройка диапазона времени авто-сбора осуществляеться в "секундах".\nРекомендуемые настройки:\n"Сбор пыли" около 1 часа.\n"Сбор звезд" ставить на 5 - 15 мин больше,чем сбор пыли.\n',reply_markup=kb.set)
    
#Настройка время сбора пыли
@router.callback_query(F.data == 'dust')
async def dust_one(callback:CallbackQuery,state:FSMContext):
    await callback.answer('О уже почти')
    await state.set_state(Reg.set_time_collet_min)
    await callback.message.answer('Диапазон секунд "От"')

@router.message(Reg.set_time_collet_min)
async def dust_two(message:Message,state:FSMContext):
    await state.update_data(set_time_collet_min=int(message.text))
    await state.set_state(Reg.set_time_collet_max)
    await message.answer('Диапазон секунд "До"')
    
@router.message(Reg.set_time_collet_max)
async def dust_tree(message:Message,state:FSMContext):
    await state.update_data(set_time_collet_max=int(message.text))
    user_id = message.from_user.id
    data = await state.get_data()
    
    if user_id not in set_collect:
        set_collect[user_id] = []
    
    if len(set_collect[user_id]) == 0:
        set_collect[user_id].append(data)
        await message.answer('Настройки добавлены!')
        await min_c(user_id)
        await max_c(user_id)
    else:
        set_collect[user_id][0].update(data)
        await message.answer('Настройки изменены!')
        await min_c(user_id)
        await max_c(user_id)
    await state.clear()

#Настрока времени сбора звезд
@router.callback_query(F.data == 'stars')
async def stars_one(callback:CallbackQuery,state:FSMContext):
    await callback.answer('Уже загружаем')
    await state.set_state(Reg.set_time_stars_min)
    await callback.message.answer('Диапазон секунд "От"')

@router.message(Reg.set_time_stars_min)
async def stars_two(message:Message,state:FSMContext):
    await state.update_data(set_time_stars_min=int(message.text))
    await state.set_state(Reg.set_time_stars_max)
    await message.answer('Диапазон секунд "До"')
    
@router.message(Reg.set_time_stars_max)
async def stars_tree(message:Message,state:FSMContext):
    await state.update_data(set_time_stars_max=int(message.text))
    user_id = message.from_user.id
    data = await state.get_data()
    
    if user_id not in set_stars:
        set_stars[user_id] = []
    
    if len(set_stars[user_id]) == 0:
        set_stars[user_id].append(data)
        await message.answer('Настройки добавлены!')
        await min_s(user_id)
        await max_s(user_id)
    else:
        set_stars[user_id][0].update(data)
        await message.answer('Настройки изменены')
        await min_s(user_id)
        await max_s(user_id)
    await state.clear()
    
    
#Кнопка "Списка аккаунтов"
@router.callback_query(F.data == 'list_account')
async def list(callback:CallbackQuery):
    user_id = callback.from_user.id
    if len(account_list[user_id]) == 0:
        await callback.message.answer('Что?\nУ тебя нету добавленых аккаунтов!\nА ну-ка добавь быстрее')
    else:
        lst = [f'{n})\nSESSION: {i["registration_session"]}\nGALAXY: {i["registration_galaxy"]}\nPROXY: {i["registration_proxy"]}\n' for n,i in enumerate(account_list[user_id])]
        await callback.answer('Опа прогружаем')
        await callback.message.answer(text='\n'.join(lst))

#Кнопка "Удаление аккаунтов"
@router.callback_query(F.data == 'del_account')
async def del_one(callback:CallbackQuery,state:FSMContext):
    await callback.answer(text='Щас')
    await state.set_state(Reg.delet_account)
    await callback.message.answer(text='Ну-ка вводи номер аккаунта,который хочешь удалить:')

@router.message(Reg.delet_account)
async def del_two(message:Message,state:FSMContext):
    await state.update_data(delet_account = int(message.text))
    user_id = message.from_user.id
    data = await state.get_data()
    lst_data = account_list[user_id]
    if len(lst_data) > data["delet_account"]:
        del lst_data[data["delet_account"]]
        await message.answer(text=f'А надо было?\nНо аккаунт {data["delet_account"]} уже удален')
    else:
        await message.answer(text=f'Опа! Нету такого {data["delet_account"]} аккаунта')
    await state.clear()

    
    
    
    
    
    