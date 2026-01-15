import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration settings"""
    TOKEN = os.getenv('DISCORD_TOKEN')
    PREFIX = os.getenv('PREFIX', '!')
    STATUS = os.getenv('STATUS', 'with commands')
    
    # Bot colors for embeds
    COLOR_PRIMARY = 0x36393F  # Blurple
    COLOR_SUCCESS = 0x36393F   # Green
    COLOR_WARNING = 0x36393F   # Yellow
    COLOR_ERROR = 0x36393F     # Red
