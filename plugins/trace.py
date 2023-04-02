import asyncio

from core import command
from core.custom import is_traced
from loguru import logger
from pyrogram import Client
from pyrogram.errors import BadRequest, FloodWait, RPCError
from pyrogram.types import Message
from tools.constants import REACTIONS, STORE_TRACE_DATA
from tools.helpers import Parameters, delete_this
from tools.storage import SimpleStore
from pyrogram.enums import ParseMode 

@Client.on_message(is_traced(), group=-4)
async def trace_event(cli: Client, msg: Message):
    user = msg.from_user
    async with SimpleStore(auto_flush=False) as store:
        try:
            emoji = store.get_data(STORE_TRACE_DATA).get(user.id)
            await cli.send_reaction(
                msg.chat.id, msg.id, emoji
            )
        except BadRequest:
            failure = f"Group named <{msg.chat.title}> can't use {emoji} to react."
            store.data[STORE_TRACE_DATA].pop(user.id, None)
            store.flush()
            await cli.send_message('me', failure)
        except RPCError as e:
            logger.error(e)


@Client.on_message(command('trace'))
async def trace(cli: Client, msg: Message):
    """群组中追着丢emoji
    指令：-trace
    用法：-trace <emoji|clear|list> 用于回复一条消息
    """
    cmd, opt = Parameters.get(msg)
    replied_msg = msg.reply_to_message

    if not opt and not replied_msg:
        await msg.edit_text(f'❗️ Use `{cmd}` to reply a message.')
        return

    if opt != 'clear' and opt != 'list':
        emoji = '💩' if opt not in REACTIONS else opt
        user = replied_msg.from_user
        try:
            await cli.send_reaction(
                msg.chat.id,
                replied_msg.id,
                emoji
            )
        except RPCError as e:
            logger.warning(e)
            await msg.edit_text(f"❗️ Can't use {emoji} in this chat.")
            return

    async with SimpleStore() as store:
        trace_data = store.get_data(STORE_TRACE_DATA)
        if opt != 'clear' and opt != 'list':
            # 追踪列表中没有，则添加
            if not trace_data.get(user.id):
                trace_data[user.id] = emoji
                text = f"✅ 添加 {user.mention(style=ParseMode.MARKDOWN)} 到trace列表"
                logger.success(text)
            # 追踪列表有，则删除
            elif trace_data.pop(user.id, False):
                text = f"✅ 将 {user.mention(style=ParseMode.MARKDOWN)} 从trace列表移除"
                logger.success(text)
            # 删除失败？？
            else:
                text = f"❌ 竟然将 {user.mention(style=ParseMode.MARKDOWN)} 从trace列表移除失败！！!"
                logger.warning(text)
        elif opt == 'clear':
            trace_data.clear()
            text = "✅ 已清空trace名单"
        elif opt == 'list':
            tmp = '\n'.join(f"`{k}` | {v}" for k, v in trace_data.items())
            text = f"📢 trace名单：\n{tmp}"

    try:
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)

    except FloodWait as e:
        await asyncio.sleep(e.x)
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)

    except RPCError as e:
        logger.error(e)
        await msg.edit_text(f"Network error | `{e}`")

    finally:
        if opt != 'clear' and opt != 'list':
            await asyncio.sleep(3)
            await delete_this(msg)
        await logger.complete()
