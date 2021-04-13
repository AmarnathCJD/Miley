#Soon!
from telethon import events
from Evie import tbot
from Evie.function import is_nsfw
@tbot.on(events.NewMessage())        
async def ws(event):
 if event.is_private:
   return
 if not event.photo:
   return
 hmmstark = await is_nsfw(event)
 if hmmstark is True:
   await event.delete()
