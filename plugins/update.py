import asyncio
import sys
from subprocess import PIPE, Popen

from core import command
from loguru import logger
from pyrogram import Client
from pyrogram.types import Message
from tools.constants import (SYCGRAM, SYCGRAM_ERROR, SYCGRAM_INFO,
                             SYCGRAM_WARNING, UPDATE_CMD)
from tools.helpers import Parameters, show_cmd_tip, show_exception
from tools.updates import (get_alias_of_cmds, is_latest_version,
                           pull_and_update_command_yml, reset_cmd_alias,
                           update_cmd_alias, update_cmd_prefix)
from pyrogram.enums import ParseMode 

@Client.on_message(command("restart"))
async def restart(_: Client, msg: Message):
    """重启"""
    text = f"**{SYCGRAM_INFO}**\n> # `Restarting {SYCGRAM} ...`"
    await msg.edit_text(text=text, parse_mode=ParseMode.MARKDOWN)
    sys.exit()


@Client.on_message(command("update"))
async def update(_: Client, msg: Message):
    """更新sycgram到主分支的最新版本"""
    # arg - 是否强制更新
    _, arg = Parameters.get(msg)
    arg = False if arg != "force" else True
    version_info = f"**{SYCGRAM_INFO}**\n> # `The current version is the latest.`"

    if not arg:
        try:
            res = await is_latest_version()
        except Exception as e:
            return await show_exception(msg, e)
        if res:
            return await msg.edit_text(version_info, parse_mode=ParseMode.MARKDOWN)
        else:
            text = f"**{SYCGRAM_INFO}**\n> # `Updating to the latest version.`"
    else:
        text = f"**{SYCGRAM_INFO}**\n> # `Forcing to update to the latest version.`"

    await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    try:
        await pull_and_update_command_yml()
        p = Popen(UPDATE_CMD, stdout=PIPE, shell=True)
        p.communicate()
    except asyncio.exceptions.TimeoutError:
        text = f"**{SYCGRAM_WARNING}**\n> # `Update Timeout！`"
    except Exception as e:
        text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
    else:
        text = version_info
    finally:
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)


@Client.on_message(command("prefix"))
async def prefix(_: Client, msg: Message):
    """更改所有指令的前缀"""
    _, pfx = Parameters.get(msg)
    punctuation = list("""!#$%&*+,-./:;=?@^~！？。，；·\\""")
    if pfx == "reset":
        try:
            await pull_and_update_command_yml(is_update=False)
        except Exception as e:
            return await show_exception(msg, e)
        else:
            await msg.edit_text("✅ Restore command.yml to default.")
            sys.exit()

    elif len(pfx) == 0 or len(pfx) > 1 or pfx not in punctuation:
        text = f"**{SYCGRAM_WARNING}**\n> # `Prefix must be one of {' '.join(punctuation)}`"
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        return
    try:
        update_cmd_prefix(pfx)
    except Exception as e:
        text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
        logger.error(e)
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    else:
        text = f"**{SYCGRAM_INFO}**\n> # `Restarting prefix of all commands.`"
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        sys.exit()


@Client.on_message(command("alias"))
async def alias(_: Client, msg: Message):
    """
    cmd: alias
    format: -alias <set> <source> <to> or -alias <reset> <source> or -alias <list>
    usage: 修改指令别名
    """
    cmd, args = Parameters.get_more(msg)
    if len(args) == 3 and args[0] == 'set':
        _, source, to = args
        try:
            update_cmd_alias(source, to)
        except Exception as e:
            text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
            logger.error(e)
            await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        else:
            text = f"**{SYCGRAM_INFO}**\n> # `Updating alias of <{source}> to <{to}> ...`"
            await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
            sys.exit()

    elif len(args) == 2 and args[0] == 'reset':
        _, source = args
        try:
            reset_cmd_alias(source)
        except Exception as e:
            text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
            logger.error(e)
            await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        else:
            text = f"**{SYCGRAM_INFO}**\n> # `Resetting alias of <{source}> ...`"
            await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
            sys.exit()

    elif len(args) == 1 and args[0] == 'list':
        try:
            data = get_alias_of_cmds()
            tmp = ''.join(f"`{k}` | `{v}`\n" for k, v in data.items())
            text = f"**⭐️ 指令别名：**\n**源名** | **别名**\n{tmp}"
        except Exception as e:
            text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
            logger.error(e)
            await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        else:
            await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)

    else:
        await show_cmd_tip(msg, cmd)
