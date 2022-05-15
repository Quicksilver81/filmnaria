import string
import random
import re
import os
from os import environ
from dotenv import load_dotenv
import time, requests
from pyrogram import __version__
from platform import python_version

import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger(__name__).setLevel(logging.ERROR)

botStartTime = time.time()

def is_enabled(value:str):
    return bool(str(value).lower() in ["true", "1", "e", "d"])

def get_config_from_url():
    CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL', None)
    try:
        if len(CONFIG_FILE_URL) == 0: raise TypeError
        try:
            res = requests.get(CONFIG_FILE_URL)
            if res.status_code == 200:
                logging.info("Config uzaktan alındı. Status 200.")
                with open('config.env', 'wb+') as f:
                    f.write(res.content)
                    f.close()
            else:
                logging.error(f"Failed to download config.env {res.status_code}")
        except Exception as e:
            logging.error(f"CONFIG_FILE_URL: {e}")
    except TypeError:
        pass

get_config_from_url()
if os.path.exists('config.env'): load_dotenv('config.env')

id_pattern = re.compile(r'^.\d+$')

logging.info("--- CONFIGS STARTS HERE ---")

# Bot information
SESSION = environ.get('SESSION', 'PiracyTeamMaria' + ''.join(random.choices(string.digits, k=1)))
logging.info(f"SESSION: {str(SESSION)}")
BOT_TOKEN: str = environ.get('BOT_TOKEN', None)
API_ID: int = int(environ.get('API_ID', 3279847))
API_HASH: str = environ.get('API_HASH', None)

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', True))
logging.info(f"USE_CAPTION_FILTER: {str(USE_CAPTION_FILTER)}")
BROADCAST_AS_COPY = is_enabled(environ.get("BROADCAST_AS_COPY", True))
logging.info(f"BROADCAST_AS_COPY: {str(BROADCAST_AS_COPY)}")

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) \
    else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) \
    else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) \
    else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) \
    if auth_channel and id_pattern.search(auth_channel) \
    else None
    
auth_grp = environ.get('AUTH_GROUP')

AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
# düzeltilecek. şimdilik çalışmıyor.
DATABASE_URI = environ.get('DATABASE_URI', "")
#START Mesajı fotosu
PICS = (environ.get('PICS', 'https://telegra.ph/file/7e56d907542396289fee4.jpg https://telegra.ph/file/9aa8dd372f4739fe02d85.jpg https://telegra.ph/file/adffc5ce502f5578e2806.jpg https://telegra.ph/file/6937b60bc2617597b92fd.jpg https://telegra.ph/file/09a7abaab340143f9c7e7.jpg https://telegra.ph/file/5a82c4a59bd04d415af1c.jpg https://telegra.ph/file/323986d3bd9c4c1b3cb26.jpg https://telegra.ph/file/b8a82dcb89fb296f92ca0.jpg https://telegra.ph/file/31adab039a85ed88e22b0.jpg https://telegra.ph/file/c0e0f4c3ed53ac8438f34.jpg https://telegra.ph/file/eede835fb3c37e07c9cee.jpg https://telegra.ph/file/e17d2d068f71a9867d554.jpg https://telegra.ph/file/8fb1ae7d995e8735a7c25.jpg https://telegra.ph/file/8fed19586b4aa019ec215.jpg https://telegra.ph/file/8e6c923abd6139083e1de.jpg https://telegra.ph/file/0049d801d29e83d68b001.jpg')).split()
# db url.
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
# db ismi. db oluştururken Cluster0 diye bıraktıysan elleme.
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'dosyalar')
# db koleksiyon ismi. hiç elleme sorun çıkmaz.
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
# kendi kullanıcı idnizi verin geçin.
BUTTON_COUNT = int(environ.get('BUTTON_COUNT', 10))
# buton sayısı. düzgün çalışmıyor 10da bırakın.
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '')
if len(SUPPORT_CHAT) == 0: SUPPORT_CHAT = None
# destek chati. başında @ olmadan girin.
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
if len(CUSTOM_FILE_CAPTION) == 0: CUSTOM_FILE_CAPTION = None
# dosyanın altında ne yazsın ?
SEND_WITH_BUTTONS = is_enabled(environ.get("SEND_WITH_BUTTONS", False))
logging.info(f"SEND_WITH_BUTTONS: {str(SEND_WITH_BUTTONS)}")
# True: dosyayı butonlarla gönderir
FILE_PROTECTED = is_enabled(environ.get("FILE_PROTECTED", False))
logging.info(f"FILE_PROTECTED: {str(FILE_PROTECTED)}")
# True: dosyayı iletilemez yapar
JOIN_CHANNEL_WARNING = is_enabled(environ.get("JOIN_CHANNEL_WARNING", True))
logging.info(f"JOIN_CHANNEL_WARNING: {str(JOIN_CHANNEL_WARNING)}")
# False: kanalda olmayanlara çalışmaz, True: Kanala katıl diye uyarı verir.
HELP_MESSAGES_AFTER_FILE = is_enabled(environ.get("HELP_MESSAGES_AFTER_FILE", True))
logging.info(f"HELP_MESSAGES_AFTER_FILE: {str(HELP_MESSAGES_AFTER_FILE)}")
# dosya göndedikten sonra yardım mesajları gönderir.
WELCOME_NEW_GROUP_MEMBERS = is_enabled(environ.get("WELCOME_NEW_GROUP_MEMBERS", True))
logging.info(f"WELCOME_NEW_GROUP_MEMBERS: {str(WELCOME_NEW_GROUP_MEMBERS)}")
# gruba gelenleri selamlar
WELCOME_SELF_JOINED = is_enabled(environ.get("WELCOME_SELF_JOINED", True))
logging.info(f"WELCOME_SELF_JOINED: {str(WELCOME_SELF_JOINED)}")
# biri botu gruba ekleyince eklediğin için tşk mesajı.
CAPTION_SPLITTER = environ.get("CAPTION_SPLITTER", ' 🔥 ')
logging.info(f"CAPTION_SPLITTER: {str(CAPTION_SPLITTER)}")
# ben bunu kullanıyorum: ' 🔥 ' sebep: daha fazla caption gözüksün. istersen: '\n'
SHARE_BUTTON_TEXT = environ.get('SHARE_BUTTON_TEXT', 'Denemeni öneririm: {username}')
# dosya altındaki paylaş butonu...
REQUEST_LINK = is_enabled(environ.get("REQUEST_LINK", True))
logging.info(f"REQUEST_LINK: {str(REQUEST_LINK)}")
# linki istek katılma isteği olarak oluşturur.
YOU_JOINED = is_enabled(environ.get("YOU_JOINED", True))
logging.info(f"YOU_JOINED: {str(YOU_JOINED)}")
# kanala katıldın beni kullanabilirsin mesajı
NO_SERVICE = is_enabled(environ.get("NO_SERVICE", False))
logging.info(f"NO_SERVICE: {str(NO_SERVICE)}")
# anti service  messages
GEN_CHAT_LINK_DELAY = int(environ.get('GEN_CHAT_LINK_DELAY', 10))
logging.info(f"GEN_CHAT_LINK_DELAY: {str(GEN_CHAT_LINK_DELAY)}")
# çet içinlink oluşturmadan önce beklenecek süre. dakika cinsinden.
WELCOME_TEXT = environ.get('WELCOME_TEXT', 'Esenlikler {}. Hoş Geldin Sefa Geldin.')
# link vb. girilebilir.

defstarttxt = """Merhaba {},
Ben <a href='https://t.me/Anagrupbot'>Ana Grup Bot</a>, İnline Modda (Satır içi) çalışıyorum ve size film sağlamaya çalışıyorum. Eğer senin de bota eklenmesini istediğin film veya dizi önerin varsa <a href='https://t.me/Anagrupp'>İstek Ve Sohbet</a> Grubuna Beklerim.
"""
LINK_FOR_EVERYTHING = environ.get('LINK_FOR_EVERYTHING', '')
# tüm ayrıntılrınızı içeren birlink varsa buraya girin.
START_TXT = environ.get('START_TXT', defstarttxt)
# 3 tane yer tutucu bırakın. örneğin: "selam {} ben {} {}"


LINK_FOR_ABOUT_PIC = environ.get('LINK_FOR_ABOUT_PIC', 'https://telegra.ph/file/375b69b135524990cb7ca.jpg')
# about kısmındaki foto linki.
defabout = f"[🔥]({LINK_FOR_ABOUT_PIC})" + " {}\n\n" + \
    "Anonim kişiler tarafından geliştirildi.\n" + \
    "Takıl işte üzümü ye bağını sorma.\n" + \
    "Telegramı indexleyen bir bot.\n\n" + \
    "Bot Sürümü: v2.0.5 Beta" + \
    f"\nPython Sürümü: {python_version()}" \
    f"\nPyrogram Sürümü: {__version__}\n"
ABOUT_TXT = environ.get('ABOUT_TXT', defabout)
# bir tane yer tutucu bırakın. botun adı gelecek. örneğin: "bu basit bir hakkında metnidir ve bot adı {} dir."

logging.info("--- CONFIGS ENDS HERE ---")
