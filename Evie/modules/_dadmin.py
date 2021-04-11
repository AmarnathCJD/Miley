from Evie import tbot, OWNER_ID, BOT_ID
from Evie.function import is_admin, can_ban_users, bot_ban, get_user
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@tbot.on(events.NewMessage(pattern="^[!/]ban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  user, args = await get_user(event)
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  if args:
    reason = f'\n**Reason:** {args}'
  else:
    reason = ""
  await tbot(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
  await event.reply(f"Successfully Banned!{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]dban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if event.is_reply:
      x = (await event.get_reply_message()).sender_id
      if int(x) == BOT_ID or int(x) == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, x):
        return await event.reply("Yeah lets start banning admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if not event.is_reply:      
     await event.reply("Reply to someone to delete the message and ban the user!")
     return
  input = event.pattern_match.group(1)
  if input:
   reason = f'\n**Reason:** `{input}`'
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


@tbot.on(events.NewMessage(pattern="^[!/]sban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  await event.delete()
  user, args = await get_user(event)
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  await tbot(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))

@tbot.on(events.NewMessage(pattern="^[!/]unban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    user, args = await get_user(event)
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
  if args:
    reason = f'\n**Reason:** {args}'
  else:
    reason = ""
  await tbot(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
  await event.reply(f"Yep, this user can join!")

@tbot.on(events.NewMessage(pattern="^[!/]kick ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("I really wish I could kick admins...")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  user, args = await get_user(event)
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  if args:
    reason = f'\n**Reason:** {args}'
  else:
    reason = ""
  await tbot(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
  await event.reply(f"Kicked!{reason}")


@tbot.on(events.NewMessage(pattern="^[!/]dkick ?(.*)"))
async def dban(event): 
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
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
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
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
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  user, reason = await get_user(event)
  await event.delete()
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
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
  
@tbot.on(events.NewMessage(pattern="^[!/]mute ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start muting admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  user, args = await get_user(event)
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  if args:
    reason = f'\n**Reason:** {args}'
  else:
    reason = ""
  pro = await tbot(GetFullUserRequest(user.id))
  await tbot(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
  await event.reply(f"**{pro.first.name}** is muted in **{event.chat.title}**.{reason}")

