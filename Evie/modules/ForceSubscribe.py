#test modules

from Evie import tbot, BOT_ID
from Evie.events import register
from Evie.function import is_admin
import Evie.modules.sql.fsub_sql as sql
from telethon import events, functions, Button
import telethon
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.tl import types

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

async def check_him(channel, uid):
    try:
        result = await tbot(
            functions.channels.GetParticipantRequest(
                channel=channel, user_id=uid
            )
        )
        return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False

async def rights(event):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=event.chat_id,
            user_id=BOT_ID,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


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
 user_id = event.sender_id
 if not chat_db:
   return
 if await is_admin(event, event.sender_id):
   return
 if chat_db:
  try:
    channel = chat_db.channel
    rip = await check_him(channel, event.sender_id)
    if rip is False:
      rk = f"{event.sender_id}"
      fname = event.sender.first_name
      grp = f"t.me/{channel}"
      buttons = [[Button.url("Join Channel", grp)],
               [Button.inline("Unmute Me", data="fs_{}".format(rk))],]
      text = "{}, you have **not subscribed** to our [channel](https://t.me/{}) yet❗.Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(fname, channel, channel)
      await tbot(EditBannedRequest(event.chat_id, event.sender_id, MUTE_RIGHTS))
      await tbot.send_message(event.chat_id, text, buttons=buttons, link_preview=False)
  except:
    if not await rights(event):
       await tbot.send_message(event.chat_id, "❗**I am not an admin here.**\nMake me admin with ban user permission")
     
@tbot.on(events.CallbackQuery(pattern=r"fs(\_(.*))"))
async def start_again(event):
 tata = event.pattern_match.group(1)
 data = tata.decode()
 user = data.split("_", 1)[1]
 if not event.sender_id == int(user):
  return await event.answer("You are not the muted user!")
 chat_id = event.chat_id
 chat_db = sql.fs_settings(chat_id)
 if chat_db:
    channel = chat_db.channel
    rip = await check_him(channel, event.sender_id)
    if rip is True:
     try:
       await event.delete()
       await tbot(EditBannedRequest(event.chat_id, int(user), UNMUTE_RIGHTS))
     except:
       if not await rights(event):
         return await tbot.send_message(event.chat_id, "❗ **I am not an admin here.**\nMake me admin with ban user permission")
    else:
     await event.answer("Please join the Channel!")
    
       
      
 
