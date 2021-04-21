from Evie import ubot, TOKEN, OWNER_ID
from telethon import events

@ubot.on(events.NewMessage(pattern="!logs"))
async def lg(event):
 if not event.sender_id == OWNER_ID:
   return
 await event.edit("Logs Modules Active..")
