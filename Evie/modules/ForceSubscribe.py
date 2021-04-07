from Evie import tbot, BOT_ID
from Evie.events import register
from Evie.function import is_admin
import Evie.modules.sql.fsub_sql as sql
from telethon import events, functions, Button
import telethon
#ported by RoseLoverX
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.tl import types
from telethon.tl.functions.channels import GetFullChannelRequest

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

@register(pattern="^/(fsub|forcesubscribe) ?(.*)")
async def fs(event):
  if not await is_admin(event, event.sender_id):
    return await event.reply("You need to be an admin to do this!")
  permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
  if not permissions.is_creator:
          return await event.reply("❗**Group Creator Required**\nYou have to be the group creator to do that.")
  if not await is_admin(event, BOT_ID):
   return await event.reply("I'm not an admin Mind Promoting Me?!")
  args = event.pattern_match.group(2)
  channel = args.replace("@", "")
  if not args:
    chat_db = sql.fs_settings(event.chat_id)
    if chat_db:
      return await event.reply(f"Currently Forsubscribe is ✅Enabled.\nSubscribed to @{chat_db.channel}")
    else:
      return await event.reply("Forcesubscribe is currently ❌Disabled.")
  if args == "on" or args == "On":
     return await event.reply("❗Please Specify the Channel Username")
  elif args in ("off", "no", "disable"):
    sql.disapprove(event.chat_id)
    await event.reply("❌ **Force Subscribe is Disabled Successfully.**")
  else:
    try:
      ch_full = await tbot(GetFullChannelRequest(channel=channel))
    except:
      return await event.reply("❗**Invalid Channel Username.**")
    rip = await check_him(channel, BOT_ID)
    if rip is False:
      return await event.reply(f"❗**Not an Admin in the Channel**\nI am not an admin in the [channel](https://t.me/{args}). Add me as a admin in order to enable ForceSubscribe.", link_preview=False)
    sql.add_channel(event.chat_id, str(channel))
    await event.reply(f"✅ **Force Subscribe is Enabled** to @{channel}.")
  
    
      
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
    
       
      
 
