from Evie import tbot, OWNER_ID, BOT_ID, CMD_HELP
from Evie.events import register
from Evie.function import is_admin, can_ban_users, bot_ban, get_user
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon import events
import time, os
from telethon.tl.functions.users import GetFullUserRequest
import telethon
from telethon import Button

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

async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await message.reply(f"Invalid time type specified. Expected m,h, or d, got: {unit}")
            return ""

        if unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            return 
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return

@tbot.on(events.NewMessage(pattern="^[!/]ban ?(.*)"))
async def dban(event):
 if event.is_private:
   return await event.reply("This command is made to be used in group chats, not in pm!")
 user, args = await get_user(event)
 user_id = user.id
 sender_id = event.sender_id
 if not sender_id == OWNER_ID:
    if not await is_admin(event, sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
 if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
 if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
 if args:
    reason = f'\n**Reason:** {args}'
 else:
    reason = ""
 await tbot.edit_permissions(event.chat_id, user_id, view_messages=False)
 await event.reply(f"Successfully Banned!{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]dban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not await bot_ban(message=event):
     return
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
  await tbot.edit_permissions(event.chat_id, int(mk), view_messages=False)
  await event.reply(f"Successfully Banned!{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]sban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not await bot_ban(message=event):
     return
  user, args = await get_user(event)
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start banning admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  await event.delete()
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  await tbot.edit_permissions(event.chat_id, user.id, view_messages=False)

@tbot.on(events.NewMessage(pattern="^[!/]unban ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  user, args = await get_user(event)
  if await is_admin(event, user.id):
        return await event.reply("Yeah admins! Can't be unbanned")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if args:
    reason = f'\n**Reason:** {args}'
  else:
    reason = ""
  await tbot.edit_permissions(event.chat_id, user.id)
  await event.reply(f"Yep, this user can join!")

@tbot.on(events.NewMessage(pattern="^[!/]kick ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  user, args = await get_user(event)
  if args == "me":
    retuen
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("I really wish I could kick admins...")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
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
  await tbot.edit_permissions(event.chat_id, int(mk), send_messages=False)
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
  user, args = await get_user(event)
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start muting admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  if args:
    reason = f'\n**Reason:** {args}'
  else:
    reason = ""
  replied_user = await tbot(GetFullUserRequest(user.id))
  await tbot.edit_permissions(event.chat_id, user.id, send_messages=False)
  await event.reply(f"**{replied_user.user.first_name}** is muted in **{event.chat.title}**.{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]unmute ?(.*)"))
async def dban(event):
  if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
  user, args = await get_user(event)
  if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if await is_admin(event, user.id):
        return await event.reply("Yeah lets start muting admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if user:
    if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  if args:
    reason = f'\nReason: `{args}`'
  else:
    reason = ""
  replied_user = await tbot.get_entity(user.id)
  await tbot.edit_permissions(event.chat_id, user.id, send_messages=True)
  await event.reply(f"Yep, **{replied_user.first_name}** can start talking again in **{event.chat.title}**.{reason}")

@tbot.on(events.NewMessage(pattern="^[!/]smute ?(.*)"))
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
        return await event.reply("Yeah lets start muting admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
  await tbot(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))

@tbot.on(events.NewMessage(pattern="^[!/]tmute ?(.*)"))
async def tmute(event):
 if event.is_private:
    return await event.reply("This command is made to be used in group chats, not in pm!")
 user, args = await get_user(event)
 if not event.sender_id == OWNER_ID:
    if not await is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if user:
      if user.id == BOT_ID or user.id == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, user.id):
        return await event.reply("Yeah lets start muting admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
 if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!")
 if not args:
   return await event.reply("You haven't specified a time to mute this user for!")
 input = args.split(" ", 1)
 if len(input) == 2:
   time = input[0]
   reason = input[1]
 elif len(input) == 1:
   time = input[0]
   reason = None
 if len(time) == 1:
   return await event.reply(f"Invalid time type specified. Expected m,h, or d, got: {time}")
 mutetime = await extract_time(event, time)
 await tbot.edit_permissions(event.chat_id, user.id, send_messages=False, until_date=mutetime)
 replied_user = await tbot.get_entity(user.id)
 await event.respond(f'Muted **{replied_user.first_name}** for {args}!')

@register(pattern="^/kickme$")
async def pk(event):
 if event.is_private:
   return
 if await is_admin(event, event.sender_id):
   return await event.reply("Ha, I'm not kicking you, you're an admin! You're stuck with everyone here.")
 try:
    await tbot.kick_participant(event.chat_id, event.sender_id)
    await event.reply("Ok kicked!")
 except:
    await event.reply("Failed to kick!")
 

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
Some people need to be publicly banned; spammers, annoyances, or just trolls.

This module allows you to do that easily, by exposing some common actions, so everyone will see!

**User commands:**
- /kickme: Users that use this, kick themselves.

**Admin commands:**
- /ban: Ban a user.
- /dban: Ban a user by reply, and delete their message.
- /sban: Silently ban a user, and delete your message.
- /tban: Temporarily ban a user.
- /unban: Unban a user.
- /mute: Mute a user.
- /dmute: Mute a user by reply, and delete their message.
- /smute: Silently mute a user, and delete your message.
- /tmute: Temporarily mute a user.
- /unmute: Unmute a user.
- /kick: Kick a user.
- /dkick: Kick a user by reply, and delete their message.
- /skick: Silently kick a user, and delete your message
**Now Supports Anonymous Admins Also -Soon**
"""
CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

