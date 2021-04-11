from Evie import tbot, OWNER_ID, BOT_ID
from Evie.function import is_admin, can_ban_users, bot_ban, get_user
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon import events

@tbot.on(events.NewMessage(pattern="^[!/]dban ?(.*)"))
async def dban(event): 
  if not event.sender_id == OWNER_ID:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if not event.is_reply:      
     await event.reply("Reply to someone to delete the message and ban the user!")
     return
    if event.is_reply:
      x = (await event.get_reply_message()).sender_id
      if int(x) == BOT_ID or int(x) == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, x):
        return await event.reply("Yeah lets start banning admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  input = event.pattern_match.group(1)
  if input:
   reason = f'\n**Reason:** {input}'
  else:
   reason = ""
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  reply_msg = await event.get_reply_message()
  zx = (await event.get_reply_message())
  await zx.delete()
  mk = (await event.get_reply_message()).sender_id
  await tbot(EditBannedRequest(event.chat_id, int(mk), ChatBannedRights(until_date=None, view_messages=True)))
  await event.reply(f"Successfully Banned!{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]dkick ?(.*)"))
async def dban(event): 
  if not event.sender_id == OWNER_ID:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if not event.is_reply:      
     await event.reply("Reply to someone to delete the message and kick the user!")
     return
    if event.is_reply:
      x = (await event.get_reply_message()).sender_id
      if int(x) == BOT_ID or int(x) == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, x):
        return await event.reply("Yeah lets start kicking admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  input = event.pattern_match.group(1)
  if input:
   reason = f'\n**Reason:** {input}'
  else:
   reason = ""
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  reply_msg = await event.get_reply_message()
  zx = (await event.get_reply_message())
  await zx.delete()
  mk = (await event.get_reply_message()).sender_id
  await tbot.kick_participant(event.chat_id, int(mk))
  await event.reply(f"Successfully Kicked!{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]dmute ?(.*)"))
async def dban(event): 
  if not event.sender_id == OWNER_ID:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if not event.is_reply:      
     await event.reply("Reply to someone to delete the message and mute the user!")
     return
    if event.is_reply:
      x = (await event.get_reply_message()).sender_id
      if int(x) == BOT_ID or int(x) == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, x):
        return await event.reply("Yeah lets start muting admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  input = event.pattern_match.group(1)
  if input:
   reason = f'\n**Reason:** {input}'
  else:
   reason = ""
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  reply_msg = await event.get_reply_message()
  zx = (await event.get_reply_message())
  await zx.delete()
  mk = (await event.get_reply_message()).sender_id
  await tbot(EditBannedRequest(event.chat_id, int(mk), ChatBannedRights(until_date=None, send_messages=True)))
  await event.reply(f"Successfully Muted!{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]skick ?(.*)"))
async def dban(event): 
  user, reason = await get_user(event)
  if not event.sender_id == OWNER_ID:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if user:
      if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, user.id):
        return await event.reply("Yeah lets start kicking admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  await tbot.kick_participant(event.chat_id, int(user.id))
  
