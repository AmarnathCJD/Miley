from Evie import tbot, BOT_ID, OWNER_ID
from telethon import events, functions, Button
import telethon

@tbot.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        if not event.user_id == BOT_ID:
         if not event.user_id == OWNER_ID:
           chat = int(-1001309757591)
           rip = await check_him(chat, event.user_id)
           if rip is False:
             await event.reply(
                "**To Use This Bot, Please Join My Channel. :)**",
                buttons=[Button.url("Join Channel", Config.JTU_LINK)],
            )
            return
           else:
             await event.reply("Helmo Vro")





async def check_him(chnnl_id, chnnl_link, starkuser):
    try:
        result = await tbot(
            functions.channels.GetParticipantRequest(
                channel=chnnl_id, user_id=starkuser
            )
        )
        return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False
