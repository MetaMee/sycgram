
from typing import Dict, List

# Some params of sycgram
SYCGRAM: str = "sycgram"
SYCGRAM_INFO: str = f"{SYCGRAM.title()} | INFO"
SYCGRAM_ERROR: str = f"{SYCGRAM.title()} | ERROR"
SYCGRAM_WARNING: str = f"{SYCGRAM.title()} | WARNING"
COMMAND_YML: str = './data/command.yml'
CMD_YML_REMOTE: str = "https://raw.githubusercontent.com/MetaMee/sycgram/main/data/command.yml"
UPDATE_CMD: str = "docker run --rm " \
    "-v /var/run/docker.sock:/var/run/docker.sock " \
    "containrrr/watchtower " \
    "--trace " \
    "--cleanup " \
    "--run-once " \
    f"{SYCGRAM}"


# ------------- Load --------------
DOWNLOAD_PATH: str = './data/download/'

# ------------- rate --------------
RATE_API: str = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies'
HTTP_HEADERS: Dict[str, str] = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

# ------------- speedtest --------------
SPEEDTEST_PATH_FILE: str = './data/speedtest'
SPEEDTEST_URL: str = "https://install.speedtest.net/app/cli/ookla-speedtest-1.1.1-linux-$(uname -m).tgz"
INSTALL_SPEEDTEST: str = f"""wget -qO- "{SPEEDTEST_URL}" | tar zx -C ./data speedtest"""
SPEEDTEST_RUN: str = f'{SPEEDTEST_PATH_FILE} --accept-license --accept-gdpr -f json'

# ------------- sticker --------------
# STICKER_BOT: int = 429000
STICKER_BOT: str = "@Stickers"
STICKER_IMG: str = './data/img/tmp.png'
STICKER_DESCRIP: str = b'A Telegram user has created the Sticker\xc2\xa0Set.'.decode(
    'utf-8')
GT_120_STICKERS: str = "Whoa! That's probably enough stickers for one set, " \
                       "give it a break. A set can't have more than 120 stickers at the moment."
UNACCEPTABLE_SET_NAME: str = 'Sorry, this short name is unacceptable.'
TAKEN_SET_NAME: str = 'Sorry, this short name is already taken.'
INVALID_SET_NAME: str = 'Invalid set selected.'
STICKER_ERROR_LIST: List[str] = [
    GT_120_STICKERS,
    UNACCEPTABLE_SET_NAME,
    TAKEN_SET_NAME,
    INVALID_SET_NAME,
]

# ------------- cc & trace --------------
REACTIONS= ['👍', '👎', '❤️', '🔥', '🥰', '👏',
                        '😁', '🤔', '🤯', '😱', '🤬', '😢',
                        '🎉', '🤩', '🤮', '💩']
CC_MAX_TIMES: int = 233

# ------------- ghost --------------
GHOST_INTERVAL: float = 1.5

# ------------- other --------------
TG_GROUP: str = 'group'
TG_SUPERGROUP: str = 'supergroup'
TG_CHANNEL: str = 'channel'
TG_BOT: str = 'bot'
TG_PRIVATE: str = 'private'
TG_GROUPS: List[str] = ['group', 'supergroup']

# ------------- Store -------------
STORE_CC_DATA: str = 'data:cc'
STORE_NOTES_DATA: str = 'data:notes'
STORE_TRACE_DATA: str = 'data:trace'
STORE_GHOST_DATA: str = 'data:ghost'
STORE_GHOST_CACHE: str = 'cache:ghost'
