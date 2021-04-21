from Evie import tbot, TOKEN, OWNER_ID
from telethon import events

@tbot.on(events.NewMessage(pattern="!logs"))
async def lg(event):
 if not event.sender_id == OWNER_ID:
   return
 await event.reply("Logs Modules Active..")
