from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import threading
import time
import sys
import requests
import os

sys.path.append(str((Path(__file__).parent.parent.absolute()).joinpath('core')))
sys.path.append(str(Path(__file__).parent.absolute()))

from core.config import DEBUG_DIR
from file_manager import write_txt


load_dotenv()

def notification():
    log = Path(DEBUG_DIR).open('r',encoding='utf-8')
    
    token = os.getenv('NOTIFACAL')
    chat_id = os.getenv('CHAT_ID')
    
    payload = {
        'chat_id':chat_id,
    }
    
    url = (f'https://api.telegram.org/bot{token}/sendDocument')
    
    responce = requests.post(url=url,data=payload,files={'document':log}) 
    if responce.status_code == 200:
        write_txt(path=DEBUG_DIR,text='')
    return responce
    
def monitor_log():
    while True:
        if Path(DEBUG_DIR).stat().st_size > 0:
            notification()
            time.sleep(10)


logger.add(
    DEBUG_DIR,
    level='ERROR',
    format="\n{time:YYYY-MM-DD HH:mm:ss}\n\nLOGE: [{level}] | {message}",
)

def start_monitor_log():
    prosses = threading.Thread(target=monitor_log,daemon=True)
    prosses.start()
    






    
    
