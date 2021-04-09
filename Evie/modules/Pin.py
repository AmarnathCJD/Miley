from Evie import tbot, CMD_HELP
import os
from telethon import types
from Evie.events import register

@register(pattern="^/pinned")
async def pn(event):
   message = await tbot.get_messages(event.chat_id, ids=types.InputMessagePinned())
   id = message.id
   chat = event.chat_id.replace("-100", "")
   await event.reply(f"The pinned message in {event.chat.title} is [here](http://t.me/{chat}/{id})")
