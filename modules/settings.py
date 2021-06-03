import os
from os.path import join, dirname
from dotenv import load_dotenv
from logging import DEBUG, INFO, WARN, ERROR

def if_env(str):
    if str is None or str.upper() != 'TRUE':
        return False
    else:
        return True

def get_log_level(str):
    if str is None:
        return WARN
    upper_str = str.upper()
    if upper_str == 'DEBUG':
        return DEBUG
    elif upper_str == 'INFO':
        return INFO
    elif upper_str == 'ERROR':
        return ERROR
    else:
        return WARN

def num_env(param):
    if str is None or not str(param).isdecimal():
        return 5
    else:
        return int(param)

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), 'files' + os.sep + '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
LOG_LEVEL = get_log_level(os.environ.get('LOG_LEVEL'))
VIDEO_ID = os.environ.get('VIDEO_ID')
DISCORD_CHANNEL_ID= num_env(os.environ.get('DISCORD_CHANNEL_ID'))
CSV_OUTPUT_FLAG = if_env(os.environ.get('CSV_OUTPUT_FLAG'))