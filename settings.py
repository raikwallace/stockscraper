
import logging
import os
LOGGING_LEVEL = logging.INFO
TOKEN = '1735885855:AAFtKFrhq0Svinf7rBXet_Y100hmUAEH7Cw' #os.getenv('TELEGRAM_TOKEN') #TOKEN for Telegram Bot

URLS = { #URLS to scrap
    "3080Ti": "https://shop.nvidia.com/es-es/geforce/store/gpu/?page=1&limit=9&locale=es-es&category=GPU&gpu=RTX%203080Ti",
    "3080": "https://shop.nvidia.com/es-es/geforce/store/gpu/?page=1&limit=9&locale=es-es&category=GPU&gpu=RTX%203080",
    "3070": "https://shop.nvidia.com/es-es/geforce/store/gpu/?page=1&limit=9&locale=es-es&category=GPU&gpu=RTX%203070"
    }

TIME_MIN_BETWEEN_EXECS_MS=10000
TIME_MAX_BETWEEN_EXECS_MS=30000

#Añadir carpeta de proyectos como variable de entorno para acceder más rapido
