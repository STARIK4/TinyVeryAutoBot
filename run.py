import os
import requests
import asyncio
from dotenv import load_dotenv
from aiogram import Bot,Dispatcher
from app.heandler import router,account_list
from fake_useragent import UserAgent
from utils.random_manager import randoms
from utils.logger import logger,start_monitor_log
from utils.logo import logo
import gc 

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

ua = UserAgent()

headers = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Host": "api.tonverse.app",
    "Origin": "https://app.tonverse.app",
    "Referer": "https://app.tonverse.app/",
    "User-Agent": ua.random,
    "X-Application-Version" : "0.8.7",
    "X-Client-Time-Diff": "1737010053-0",
    "X-Requested-With": "XMLHttpRequest"
}
@logger.catch
async def collect(user_id):
    gc.collect()
    from app.heandler import min_c,max_c
    
    TIME_MIN_COLLET = await min_c(user_id)
    TIME_MAX_COLLET = await max_c(user_id)
    sleep_collet = randoms(TIME_MIN_COLLET,TIME_MAX_COLLET)
    
    dict_data = account_list[user_id]

    curent_index = 0
    while True:
        if curent_index >= len(dict_data):
            curent_index = 0
            await asyncio.sleep(sleep_collet)
        
        early_data = dict_data[curent_index]
            
        curent_sessions = early_data["registration_session"]
        curent_proxy = early_data["registration_proxy"]
            
        proxyies = None
        if curent_proxy != 'no':
            proxyies = {
                'http':curent_proxy,
        	        'https':curent_proxy,
            }
                    
        payload = {
            'session':curent_sessions,
        }
                    
        try:
            response = requests.post(
                'https://api.tonverse.app/galaxy/collect',
        	        proxies=proxyies,
        	        headers=headers,
        	        data=payload,
        	        timeout=30
            )
                    
            if response.status_code == 200:
                logger.success(f'Пыль собрана успешно на аккаунте {user_id,[curent_index]}')
            else:
                logger.error(f'Ошибка пыль не собрана на аккаунте {user_id,[curent_index]}')
        except requests.RequestException as e:
             logger.error(f'Ошибка запроса сбора пыли: {e}')
        gc.collect()
        curent_index+=1
        await asyncio.sleep(600,1200)
        
@logger.catch
async def create_stars(user_id):
    gc.collect()
    from app.heandler import min_s,max_s
    
    TIME_MIN_CREATE = await min_s(user_id)
    TIME_MAX_CREATE = await max_s(user_id)
    sleep_creat = randoms(TIME_MIN_CREATE,TIME_MAX_CREATE)
    
    dict_data = account_list[user_id]
    
    curent_index = 0
    while True:
        if curent_index >= len(dict_data):
            curent_index = 0
            await asyncio.sleep(sleep_creat)
                
        early_data = dict_data[curent_index]
            
        curent_sessions = early_data["registration_session"]
        curent_galaxy = early_data["registration_galaxy"]
        curent_proxy = early_data["registration_proxy"]
        
        proxyies = None
        if curent_proxy != 'no':
            proxyies = {
                'http':curent_proxy,
                'https':curent_proxy,
            }
            
        payload = {
            'session': curent_sessions,
            'galaxy_id': curent_galaxy,
            'stars': '100',
        }
        try:
            response = requests.post(
                'https://api.tonverse.app/stars/create',
                proxies=proxyies,
                headers=headers,
                data=payload,
                timeout=30
            )
            if response.status_code == 200:
                logger.success(f'Звезды созданы успешно на аккаунте {user_id,[curent_index]}')
            else:
                logger.error(f'Ошибка: звезды не созданы на аккаунте {user_id,[curent_index]}')
        except requests.RequestException as e:
            logger.error(f'Ошибка запроса создания звезд: {e}')
        gc.collect()
        curent_index +=1
        await asyncio.sleep(600,1200)


    
async def main():
    logo()
    start_monitor_log()
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

    
    
