from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent.parent.absolute()

LOG_DIR = Path.joinpath(ROOT_DIR,'logger')

DEBUG_DIR = Path.joinpath(LOG_DIR,'DEBUG_TINY.log')

