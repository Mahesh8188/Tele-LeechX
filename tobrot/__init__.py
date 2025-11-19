#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved 


import asyncio
import logging
import os
import time
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from sys import exit
import urllib.request
import dotenv

# Keep original alias used in project
import telegram.ext as tg

# Import pyrogram
from pyrogram import Client

# Optional import for Bot object
try:
    from telegram import Bot as TgBot  # python-telegram-bot
except Exception:
    TgBot = None

# Clear old logs if present
if os.path.exists("FuZionXLogs.txt"):
    with open("FuZionXLogs.txt", "r+") as f_d:
        f_d.truncate(0)

# the logging things >>>>>>>>>>>
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "FuZionXLogs.txt", maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

user_specific_config = dict()
dotenv.load_dotenv("config.env")

# The Telegram API things >>>>>>>>>>>
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7857092417:AAHqALkEC4YwpdFPTV0g3yQsdQkPI8hPpv0")
APP_ID = os.environ.get("APP_ID", "26741021")
API_HASH = os.environ.get("API_HASH", "7c5af0b88c33d2f5cce8df5d82eb2a94")
OWNER_ID = int(os.environ.get("OWNER_ID", "6859451629"))

# Authorised Chat Functions >>>>>>>>>>>
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "-1002084819782").split()]
# SUDO_USERS parsing - safe fallback if empty
_sudo_env = os.environ.get("SUDO_USERS", "").strip()
if _sudo_env:
    SUDO_USERS = [int(sudos) for sudos in _sudo_env.split()]
else:
    SUDO_USERS = []
AUTH_CHANNEL.append(OWNER_ID)
AUTH_CHANNEL += SUDO_USERS

# Download Directory >>>>>>>>>>>
DOWNLOAD_LOCATION = "./DOWNLOADS"

# Telegram maximum file upload size
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
TG_PRM_FILE_SIZE = 4194304000
FREE_USER_MAX_FILE_SIZE = 50000000

# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "128"))
# default thumbnail to be used in the videos
DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://telegra.ph/file/3a7f09b89943b51cdba38.jpg")
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096
# set timeout for subprocess
PROCESS_MAX_TIMEOUT = 3600
# Internal Requirements >>>>>>>>>>>
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", "10"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 600))
MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", "1072864000"))

# add config vars for the display progress
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "■")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "□")

# add offensive API
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")

#Bot Command [Leech]  >>>>>>>>>>>
LEECH_COMMAND = os.environ.get("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = os.environ.get("LEECH_UNZIP_COMMAND", "extract")
LEECH_ZIP_COMMAND = os.environ.get("LEECH_ZIP_COMMAND", "archive")
GLEECH_COMMAND = os.environ.get("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = os.environ.get("GLEECH_UNZIP_COMMAND", "gleechunzip")
GLEECH_ZIP_COMMAND = os.environ.get("GLEECH_ZIP_COMMAND", "gleechzip")

#Bot Command [ytdl] >>>>>>>>>>>
YTDL_COMMAND = os.environ.get("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = os.environ.get("GYTDL_COMMAND", "gytdl")

#Bot Command [RClone]  >>>>>>>>>>>
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "FuZionXBot")
INDEX_LINK = os.environ.get("INDEX_LINK", "https://covid.demonn.workers.dev/0:/FuZionXBot https://infyplexultra.mysterydemon.workers.dev/0:/FuZionXBot")
TELEGRAM_LEECH_COMMAND = os.environ.get("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = os.environ.get("TELEGRAM_LEECH_UNZIP_COMMAND", "tleechunzip")
CANCEL_COMMAND_G = os.environ.get("CANCEL_COMMAND_G", "cancel")
GET_SIZE_G = os.environ.get("GET_SIZE_G", "getsize")
STATUS_COMMAND = os.environ.get("STATUS_COMMAND", "status")
SAVE_THUMBNAIL = os.environ.get("SAVE_THUMBNAIL", "savethumb")
CLEAR_THUMBNAIL = os.environ.get("CLEAR_THUMBNAIL", "clearthumb")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")
PYTDL_COMMAND = os.environ.get("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = os.environ.get("GPYTDL_COMMAND", "gpytdl")
LOG_COMMAND = os.environ.get("LOG_COMMAND", "log")
CLONE_COMMAND_G = os.environ.get("CLONE_COMMAND_G", "gclone")
UPLOAD_COMMAND = os.environ.get("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = os.environ.get("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = os.environ.get("RENAME_COMMAND", "rename")
TOGGLE_VID = os.environ.get("TOGGLE_VID", "togglevid")
TOGGLE_DOC = os.environ.get("TOGGLE_DOC", "toggledoc")
RCLONE_COMMAND = os.environ.get("RCLONE_COMMAND", "rclone")

#Bot Command [Utils]  >>>>>>>>>>>
HELP_COMMAND = os.environ.get("HELP_COMMAND", "help")
SPEEDTEST = os.environ.get("SPEEDTEST", "speedtest")
TSEARCH_COMMAND = os.environ.get("TSEARCH_COMMAND", "tshelp")
MEDIAINFO_CMD = os.environ.get("MEDIAINFO_CMD", "mediainfo")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "@FuZionX")
CAP_STYLE = os.environ.get("CAP_STYLE", "code")
BOT_NO = os.environ.get("BOT_NO", "")

#Bot Command [Token Utils]  >>>>>>>>>>>
UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", "")
EMAIL = os.environ.get("EMAIL", "mysterysd.sd@gmail.com")
PWSSD = os.environ.get("PWSSD", "S#D#97531")
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "0AN3LeVWuYvwEUk9PVA")
CRYPT = os.environ.get("CRYPT", "S3htTzl3aDdHUWdJWDhLZVV2MlpSVGlkZ0RVYU0xc29oQlNKSENGakRaOD0%3D")
HUB_CRYPT = os.environ.get("HUB_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
DRIVEFIRE_CRYPT = os.environ.get("DRIVEFIRE_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
KATDRIVE_CRYPT = os.environ.get("KATDRIVE_CRYPT", "")
KOLOP_CRYPT = os.environ.get("KOLOP_CRYPT", "")
DRIVEBUZZ_CRYPT = os.environ.get("DRIVEBUZZ_CRYPT", "")
GADRIVE_CRYPT = os.environ.get("GADRIVE_CRYPT", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")

#Bot Command [IMDB]  >>>>>>>>>>>
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")
MAX_LIST_ELM = os.environ.get("MAX_LIST_ELM", None)
DEF_IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", """<i><b>⚡𝐓𝐢𝐭𝐥𝐞: </b> {title}
<b>⚡𝐈𝐌𝐃𝐁 𝐑𝐚𝐭𝐢𝐧g :</b> <code>{rating} </code>
<b>⚡𝐐𝐮𝐚𝐥𝐢𝐭𝐲:  </b>
<b>⚡𝐑𝐞𝐥𝐞𝐚𝐬𝐞 𝐃𝐚𝐭𝐞: </b> {release_date}
<b>⚡𝐆𝐞𝐧𝐫𝐞: </b>{genres}
<b>⚡️𝐈𝐌𝐃𝐁: </b>{url}
<b>⚡𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞:  </b>{languages}
<b>⚡𝐂𝐨𝐮𝐧𝐭𝐫𝐲: </b> {countries}
<b>⚡𝐒𝐮𝐛𝐭𝐢𝐭𝐥𝐞𝐬: </b>

<b>⚡𝐒𝐭𝐨𝐫𝐲 𝐋𝐢𝐧𝐞: </b><code>{plot}</code>

⚡️𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 :  @FuZionX </i>

⚡️✅ 𝑪𝒍𝒊𝒄𝒌 𝑫𝒐𝒘𝒏 𝒂𝒏𝒅 𝑺𝒕𝒂𝒓𝒕 𝒕𝒉𝒆 𝑩𝒐𝒕 𝒕𝒐 𝑮𝒆𝒕 𝒕𝒉𝒆 𝑭𝒊𝒍𝒆 ✅ !! ⬇️ ⬇️""")

#Bot Command [Bot PM & Log Channel]  >>>>>>>>>>>
LEECH_LOG = os.environ.get("LEECH_LOG", "-1002084819782")
EX_LEECH_LOG = os.environ.get("EX_LEECH_LOG", "")
EXCEP_CHATS = os.environ.get("EXCEP_CHATS", "")
BOT_PM = os.environ.get("BOT_PM", "True")
SERVER_HOST = os.environ.get("SERVER_HOST", "Heroku")

# 4 GB Upload Utils >>>>>>>>>>>
PRM_USERS = os.environ.get("PRM_USERS", "6859451629")
PRM_LOG = os.environ.get("PRM_LOG", "-1002084819782")

BOT_START_TIME = time.time()
# dict to control uploading and downloading
gDict = defaultdict(lambda: [])
# user settings dict #ToDo
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])
_lock = asyncio.Lock()

# Rclone Config Via any raw url
###########################################################################
try:
    RCLONE_CONF_URL = os.environ.get('RCLONE_CONF_URL', "")
    if len(RCLONE_CONF_URL) == 0:
        RCLONE_CONF_URL = None
    else:
        urllib.request.urlretrieve(RCLONE_CONF_URL, '/app/rclone.conf')
except KeyError:
    RCLONE_CONF_URL = None
###########################################################################

def multi_rclone_init():
    if RCLONE_CONFIG:
        LOGGER.warning("Don't use this var now, put your rclone.conf in root directory")
    if not os.path.exists("rclone.conf"):
        LOGGER.warning("Sed, No rclone.conf found in root directory")
        return
    if not os.path.exists("rclone_bak.conf"):  # backup rclone.conf file
        with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
            with open("rclone.conf", "r") as f:
                fole.write(f.read())
        LOGGER.info("rclone.conf backuped to rclone_bak.conf!")

multi_rclone_init()

# --------------- AUTO UPDATE guard ---------------
# Default OFF to avoid git pull errors in read-only envs (Koyeb etc.)
AUTO_UPDATE = os.environ.get("AUTO_UPDATE", "False").lower() in ("1", "true", "yes")
if AUTO_UPDATE:
    LOGGER.info("AUTO_UPDATE enabled. Will attempt git updates if container allows.")
else:
    LOGGER.info("AUTO_UPDATE disabled. Skipping git pull to avoid permission errors.")

# Pyrogram Client Initialization >>>>>>>>>>>
# Keep names used elsewhere: app (Pyrogram bot client) and userBot (optional user client)
try:
    # Try to ensure types are correct for Pyrogram init
    _api_id = int(APP_ID) if isinstance(APP_ID, str) and APP_ID.isdigit() else APP_ID
    app = Client("LeechBot", bot_token=TG_BOT_TOKEN, api_id=int(_api_id), api_hash=API_HASH, workers=343)
    LOGGER.info("Pyrogram bot client (app) created.")
except Exception as e:
    LOGGER.exception("Failed to create Pyrogram bot client: %s", e)
    app = None

if STRING_SESSION:
    try:
        userBot = Client("Tele-UserBot", api_id=int(_api_id), api_hash=API_HASH, session_string=STRING_SESSION)
        LOGGER.info("[PRM] Initiated USERBOT")
    except Exception as e:
        LOGGER.exception("Failed to create userBot: %s", e)
        userBot = None
else:
    userBot = None

# ------------------ python-telegram-bot (PTB) Updater & dispatcher ------------------
updater = None
dispatcher = None
bot = None  # exported name expected by __main__.py

try:
    # Initialize PTB Updater (v13.x style). Wrap in try to avoid import-time crash.
    LOGGER.debug("Attempting to initialize python-telegram-bot Updater...")
    updater = tg.Updater(token=TG_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # create a Bot object for compatibility imports (some code expects 'bot')
    if TgBot is not None:
        bot = TgBot(token=TG_BOT_TOKEN)
    else:
        # fallback: try to access from updater
        try:
            bot = updater.bot
        except Exception:
            bot = None

    # Start polling in background if possible
    try:
        updater.start_polling()
        LOGGER.info("PTB Updater started polling.")
    except Exception as e:
        LOGGER.exception("Updater.start_polling() failed: %s", e)

except Exception as e:
    LOGGER.exception("Failed to initialize python-telegram-bot Updater/Dispatcher: %s", e)
    updater = None
    dispatcher = None
    # ensure bot variable exists (may be None)
    try:
        if bot is None and TgBot is not None:
            bot = TgBot(token=TG_BOT_TOKEN)
    except Exception as _:
        bot = None

# Make sure these names exist so `from tobrot import app, bot, dispatcher, userBot` works
__all__ = ["app", "bot", "updater", "dispatcher", "userBot", "LOGGER", "DOWNLOAD_LOCATION",
           "TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]

LOGGER.info("tobrot module initialized. Exports available: %s", ", ".join(__all__))
