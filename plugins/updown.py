import asyncio
import os

from core import command
from loguru import logger
from pyrogram import Client
from pyrogram.types import Message
from tools.constants import DOWNLOAD_PATH, SYCGRAM
from tools.helpers import Parameters, delete_this, show_cmd_tip, show_exception


@Client.on_message(command("upload"))
async def upload(cli: Client, msg: Message):
    """上传文件"""
    cmd, where = Parameters.get(msg)
    if not where:
        return await show_cmd_tip(msg, cmd)
    replied_msg_id = msg.reply_to_message.id \
        if msg.reply_to_message else None
    _, filename = os.path.split(where)
    try:
        res = await cli.send_document(
            chat_id=msg.chat.id,
            document=where,
            caption=f"```From {SYCGRAM}```",
            file_name=filename,
            reply_to_message_id=replied_msg_id
        )
    except Exception as e:
        return await show_exception(msg, e)
    else:
        if res:
            await delete_this(msg)
        else:
            await msg.edit_text("⚠️ Maybe fail to upload ...")


@Client.on_message(command("download"))
async def download(_: Client, msg: Message):
    """下载目标消息的文件"""
    cmd, where = Parameters.get(msg)
    replied_msg = msg.reply_to_message
    if not replied_msg:
        return await show_cmd_tip(msg, cmd)

    try:
        res = await replied_msg.download(
            file_name=DOWNLOAD_PATH if not where else where)
    except ValueError:
        return await show_cmd_tip(msg, cmd)
    except Exception as e:
        logger.error(e)
        return await show_exception(msg, e)
    else:
        if res:
            await msg.edit_text("✅ Download this successfully.")
            await asyncio.sleep(3)
            await delete_this(msg)
        else:
            await msg.edit_text("⚠️ Maybe fail to download ...")
