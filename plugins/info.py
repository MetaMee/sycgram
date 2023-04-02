from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.helpers import get_fullname


@Client.on_message(command("id"))
async def get_id(_: Client, msg: Message):
    """直接使用或者回复目标消息，从而获取各种IDs"""
    text = f"Message ID: `{msg.id}`\n\n" \
           f"Chat Title: `{msg.chat.title or msg.chat.first_name}`\n" \
           f"Chat Type: `{msg.chat.type}`\n" \
           f"Chat ID: `{msg.chat.id}`"

    replied_msg = msg.reply_to_message
    if replied_msg and replied_msg.from_user:
        user = replied_msg.from_user
        text = f"Repiled Message ID: `{replied_msg.id}`\n\n" \
               f"User Nick: `{get_fullname(user)}`\n"\
               f"User Name: `@{user.username}`\n" \
               f"User ID: `{user.id}`\n\n" \
               f"{text}"
    elif replied_msg and replied_msg.sender_chat:
        sender_chat = replied_msg.sender_chat
        text = f"Repiled Message ID: `{replied_msg.id}`\n\n" \
               f"Chat Title: `{sender_chat.title}`\n" \
               f"Chat Type: `{sender_chat.type}`\n" \
               f"Chat ID: `{sender_chat.id}`\n\n" \
               f"{text}"

    await msg.edit_text(text)
