import asyncio

from core import command
from loguru import logger
from pyrogram import Client
from pyrogram.errors import BadRequest, FloodWait
from pyrogram.types import Message
from tools.constants import STORE_NOTES_DATA
from tools.helpers import Parameters, show_cmd_tip
from tools.storage import SimpleStore


@Client.on_message(command('note'))
async def note(_: Client, msg: Message):
    """
    用法一：-note <save|del> <序号>
    用法二：-note <序号|list|clear>
    作用：发送已保存的笔记
    """
    cmd, opts = Parameters.get_more(msg)
    if not (1 <= len(opts) <= 2):
        return await show_cmd_tip(msg, cmd)

    replied_msg = msg.reply_to_message
    async with SimpleStore() as store:
        notes_data = store.get_data(STORE_NOTES_DATA)
        if len(opts) == 2 and opts[0] == 'save' and replied_msg:
            if replied_msg:
                notes_data[opts[1]] = replied_msg.text or replied_msg.caption
                text = "😊 Notes saved successfully."
            else:
                return await show_cmd_tip(msg, cmd)
        elif len(opts) == 2 and opts[0] == 'del':
            if notes_data.pop(opts[1], None):
                text = "😊 Notes deleted successfully."
            else:
                text = "❓ Can't find the note to delete."
        elif len(opts) == 1:
            option = opts[0]
            if option == 'list':
                tmp = '\n'.join(
                    f'```{k} | {v[0:30]} ...```' for k, v in notes_data.items())
                text = f"已保存的笔记：\n{tmp}"
            elif option == 'clear':
                notes_data.clear()
                text = "✅ All saved notes have been deleted."
            else:
                res = notes_data.get(option)
                text = res if res else f"😱 No saved notes found for {option}"
        else:
            return await show_cmd_tip(msg, cmd)

    try:
        await msg.edit_text(text)
    except BadRequest as e:
        logger.error(e)  # 存在消息过长的问题，应拆分发送。（就不拆 😊）
    except FloodWait as e:
        logger.warning(e)
        await asyncio.sleep(e.x)
        await msg.edit_text(text)
    finally:
        await logger.complete()
