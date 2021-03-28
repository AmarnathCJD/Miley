from telethon import events
from Evie import BOT_ID, tbot

@tbot.on(events.ChatAction)
async def handler(event):
    if event.user_added:
        if event.user_id == BOT_ID:
           await tbot.send_message(-1001326741686, "Testing")
