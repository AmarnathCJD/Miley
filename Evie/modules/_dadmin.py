from Evie import tbot, OWNER_ID, BOT_ID
from Evie.function import is_admin, can_ban_users, bot_ban
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon import events

@tbot.on(events.NewMessage(pattern="^[!/]dban$"))
async def dban(event): 
  x = (await event.get_reply_message()).sender_id
  if not event.sender_id == OWNER_ID:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if x:
      if x == BOT_ID or x == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, x):
        return await event.reply("Yeah lets start kicking admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!, Mind promoting me?!")
  reply_msg = await event.get_reply_message()
  if not reply_msg:      
     await event.reply("Reply to someone to delete the message and ban the user!")
     return
  zx = (await event.get_reply_message())
  await zx.delete()
  await tbot(EditBannedRequest(event.chat_id, x, ChatBannedRights(until_date=None, view_messages=True)))
  await event.reply("Successfully Banned!")

@tbot.on(events.NewMessage(pattern="^[!/]dkick$"))
async def dban(event): 
  x = (await event.get_reply_message()).sender_id
  if not event.sender_id == OWNER_ID:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if x:
      if x == BOT_ID or x == OWNER_ID:
        return await event.reply("Ask the chat creator to do it!")
      if await is_admin(event, x):
        return await event.reply("Yeah lets start kicking admins!")
    if not await can_ban_users(message=event):
        await event.reply("You don't have enough rights to do that!")
        return
  if not await bot_ban(message=event):
    return await event.reply("I don't have enough rights to do this!, Mind promoting me?!")
  reply_msg = await event.get_reply_message()
  if not reply_msg:      
     await event.reply("Reply to someone to delete the message and kick the user!")
     return
  zx = (await event.get_reply_message())
  await zx.delete()
  await tbot.kick_participant(event.chat_id, x)
  await event.reply("Successfully Kicked!")


