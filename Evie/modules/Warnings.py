from Evie import tbot, CMD_HELP, MONGO_DB_URI, OWNER_ID, BOT_ID
from Evie.function import can_change_info, is_admin
from Evie.events import register
from telethon import events, Button
import os


@tbot.on(events.NewMessage(pattern="^[!/]warn ?(.*)"))
async def wn(event):
 await event.reply(event.text)

