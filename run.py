import asyncio
import logging
import random
import time
import aiogram
import requests
from aiogram import Bot, Dispatcher
from fake_useragent import UserAgent
from app.heandler import router, account_list
from utils.random_range import random_range
from config import TOKEN

# Инициализация основных компонентов
bot = Bot(token=TOKEN)
dp = Dispatcher()
ua = UserAgent()

# Заголовки для всех API запросов к TonVerse
headers = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Host": "api.tonverse.app",
    "Origin": "https://app.tonverse.app",
    "Referer": "https://app.tonverse.app/",
    "User-Agent": ua.random,
    "X-Application-Version": "0.8.7", #Если происходит так что написано пыль успешно собрана а заходите в бота и видите что не собрадось,это потому что поменялась версия приложения ее нужно будет изменить
    "X-Client-Time-Diff": "1737010053-0",
    "X-Requested-With": "XMLHttpRequest"
}


async def collect(user_id):
    """
    Автоматический сбор пыли для всех аккаунтов пользователя.
    Работает циклически с случайными задержками между действиями.
    """
    from app.heandler import min_c, max_c
    
    # Получаем настройки времени для сбора
    TIME_MIN_COLLET = await min_c(user_id)
    TIME_MAX_COLLET = await max_c(user_id)
    sleep_collet = random_range(TIME_MIN_COLLET, TIME_MAX_COLLET)
    
    dict_data = account_list[user_id]
    current_index = 0
    
    while True:
        if current_index >= len(dict_data):
            current_index = 0
            await asyncio.sleep(sleep_collet)
        
        early_data = dict_data[current_index]
        current_session = early_data["registration_session"]
        current_proxy = early_data["registration_proxy"]
        
        # Настройка прокси если указан
        proxies = None
        if current_proxy != 'no':
            proxies = {
                'http': current_proxy,
                'https': current_proxy,
            }
                    
        payload = {
            'session': current_session,
        }
                    
        try:
            response = requests.post(
                'https://api.tonverse.app/galaxy/collect',
                proxies=proxies,
                headers=headers,
                data=payload,
                timeout=30
            )
                    
            if response.status_code == 200:
                print(f'[{time.strftime("%H:%M:%S")}] Пыль успешно собрана для аккаунта {user_id},[{current_index}]')
            else:
                print(f'[{time.strftime("%H:%M:%S")}] Ошибка: Пыль не собрана для аккаунта {user_id},[{current_index}]')
        except requests.RequestException as e:
            print(f'[{time.strftime("%H:%M:%S")}] Ошибка запроса при сборе пыли: {e}')
            
        current_index += 1
        await asyncio.sleep(random.randint(10, 60))


async def create_stars(user_id):
    """
    Автоматическое создание звезд для всех аккаунтов пользователя.
    Работает циклически с случайными задержками между действиями.
    """
    from app.heandler import min_s, max_s
    
    # Получаем настройки времени для создания звезд
    TIME_MIN_CREATE = await min_s(user_id)
    TIME_MAX_CREATE = await max_s(user_id)
    sleep_create = random_range(TIME_MIN_CREATE, TIME_MAX_CREATE)
    
    dict_data = account_list[user_id]
    current_index = 0
    
    while True:
        if current_index >= len(dict_data):
            current_index = 0
            await asyncio.sleep(sleep_create)
                
        early_data = dict_data[current_index]
        current_session = early_data["registration_session"]
        current_galaxy = early_data["registration_galaxy"]
        current_proxy = early_data["registration_proxy"]
        
        proxies = None
        if current_proxy != 'no':
            proxies = {
                'http': current_proxy,
                'https': current_proxy,
            }
            
        payload = {
            'session': current_session,
            'galaxy_id': current_galaxy,
            'stars': '100',
        }
        
        try:
            response = requests.post(
                'https://api.tonverse.app/stars/create',
                proxies=proxies,
                headers=headers,
                data=payload,
                timeout=30
            )
            if response.status_code == 200:
                print(f'[{time.strftime("%H:%M:%S")}] Звезды успешно созданы для аккаунта {user_id},[{current_index}]')
            else:
                print(f'[{time.strftime("%H:%M:%S")}] Ошибка: Звезды не созданы для аккаунта {user_id},[{current_index}]')
        except requests.RequestException as e:
            print(f'[{time.strftime("%H:%M:%S")}] Ошибка запроса при создании звезд: {e}')
            
        current_index += 1
        await asyncio.sleep(random.randint(10, 60))


async def main():
    """Запуск бота и всех обработчиков."""
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())

    
    
