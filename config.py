import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('DISCORD_TOKEN')
    PREFIX = os.getenv('PREFIX', '!')
    STATUS = os.getenv('STATUS', 'with commands')
    
    COLOR_DEFAULT = 0x36393F
    COLOR_SUCCESS = 0x57F287
    COLOR_ERROR = 0xED4245
    COLOR_WARNING = 0xFEE75C
