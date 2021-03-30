from Evie import ubot
from telethon import events

@ubot.on(events.NewMessage(pattern=".eval ?(.*)"))
async def ubot(event):
  await event.reply("ok")
