from Evie import tbot, CMD_HELP, MONGO_DB_URI, OWNER_ID, BOT_ID
from Evie.function import can_change_info, is_admin, get_user
from Evie.events import register
import Evie.modules.sql.warns_sql as sql
from telethon import events, Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import os

@tbot.on(events.NewMessage(pattern="^[!/]warn ?(.*)"))
async def wn(event):
 if event.is_private:
   return 
 if not await is_admin(event, event.sender_id):
   return await event.reply("You need to be an admin to do this!")
 if not await can_change_info(message=event):
   return await event.reply("You are missing the following rights to use this command: CanChangeInfo")
 falt = event.text
 if falt.startswith("!warns"):
   return await warns(event)
 elif falt.startswith("/warns"):
   return await warns(event)
 await warn_user(event)
 
async def warn_user(event):
 user, args = await get_user(event)
 if await is_admin(event, user.id):
   return await event.reply("Oya lets start warning admins!")
 user_id = user.id
 if user_id == BOT_ID or user_id == OWNER_ID:
   return await event.reply("Yeah like I Warn myself!?")
 chat_id = event.chat_id
 if args:
   reason = f"\n**Reason:** {args}"
 else:
   reason = ""
 limit, soft_warn = sql.get_warn_setting(event.chat_id)
 num_warns, reasons = sql.warn_user(user_id, event.chat_id, reason)
 if num_warns >= limit:
  sql.reset_warns(user_id, event.chat_id)
  strength = sql.get_warn_strength(event.chat_id)
  if strength == "ban":
    await warn_ban(user_id, event)
  elif strength == "kick":
    await warn_kick(user_id, event)
  elif strength == "mute":
    await warn_kick(user_id, event)
  elif strength == "tban":
    await warn_tban(user_id, event)
  elif strength == "tmute":
    await warn_tmute(user_id, event)
 else:
  try:
    pro = await tbot.get_entity(int(user_id))
    fname = pro.first_name
  except:
    fname = "User"
  text = f"User [{fname}](tg://user?id={user_id}) has {num_warns}/{limit} warnings;\nbe careful!{reason}"
  buttons= Button.inline("Remove warn (admin only)", data=f"rm_warn-{user_id}")
  await tbot.send_message(event.chat_id, text, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"rm_warn-(\d+)"))
async def rm_warn(event):
 user_id = int(event.pattern_match.group(1))
 if not await is_admin(event, event.sender_id):
   return await event.answer("You need to be an admin!")
 try:
    pro = await tbot.get_entity(int(user_id))
    fname = pro.first_name
  except:
    fname = "User"
 text = f"Admin [{event.sender.first_name}](tg://user?id={event.sender_id}) has removed [{fname}](tg://user?id={user_id})'s warning."
 sql.remove_warn(user_id, event.chat_id)
 await event.edit(text)
   
  
 
 
 
 
 
 
 
 
 

