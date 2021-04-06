#test modules

from Evie import tbot
from Evie.events import register
from Evie.function import is_admin
import Evie.modules.sql.fsub_sql as sql
from telethon import events, functions, Button
import telethon


async def check_him(channel, user_id):
    try:
        result = await tbot(
            functions.channels.GetParticipantRequest(
                channel=channel, user_id=user_id
            )
        )
        return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False

@register(pattern="^/fsub ?(.*)")
async def fs(event):
  if not await is_admin(event, BOT_ID):
   return await event.reply("I'm not an admin Mind Promoting Me?!")
  args = event.pattern_match.group(1)
  if args:
    FK = sql.add_channel(event.chat_id, args)
    if FK:
      await event.reply("Set fsub")
      
@tbot.on(events.NewMessage(pattern=None))
async def f(event):
 chat_id = event.chat_id
 chat_db = sql.fs_settings(chat_id)
 if not chat_db:
   return
 if await is_admin(event, event.sender_id):
   return
 if chat_db:
  try:
    channel = chat_db.channel
    rip = await check_him(channel, event.sender_id)
    if rip is False:
      buttons = [[Button.link("Join Channel", "t.me\{}".format(channel))],
               [Button.inline("Unmute Me", data='unmutereq')],]
      text = "test"
      await tbot.send_message(event.chat_id, text, buttons=buttons)
  except Exception as e:
   print(e)
     
  
 
