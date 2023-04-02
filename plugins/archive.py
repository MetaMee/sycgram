import asyncio
from core import command
from pyrogram import Client
from pyrogram.types import Message


@Client.on_message(command("archive"))
async def archive(cli: Client, msg: Message):
    if await cli.archive_chats(msg.chat.id):
        await msg.edit_text(f"✅ Archive `{msg.chat.title}` successfully！")
    else:
        await msg.edit_text(f"❌ Failed to archive `{msg.chat.title}`！")
    await asyncio.sleep(2)
    await msg.delete()


@Client.on_message(command("unarchive"))
async def unarchive(cli: Client, msg: Message):
    if await cli.unarchive_chats(msg.chat.id):
        await msg.edit_text(f"✅ Unarchive `{msg.chat.title}` successfully！")
    else:
        await msg.edit_text(f"❌ Failed to unarchive `{msg.chat.title}`！")
    await asyncio.sleep(2)
    await msg.delete()
