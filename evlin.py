from Evie import tbot as lbot, TOKEN, OWNER_ID
from telethon import events

try:
    lbot.start(bot_token=TOKEN)
except Exception:
    print("failed to start logs module")

@lbot.on(events.NewMessage(pattern="!logs"))
async def lg(event):
 if not event.sender_id == OWNER_ID:
   return
 await event.reply("Logs Modules Active..")
