from Evie import tbot, CMD_HELP, BOT_ID
import os
from Evie.events import Ebot
from . import can_promote_users, get_user, is_admin, Cquery
from telethon import events, Button
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, ChannelParticipantsAdmins
from telethon.tl.functions.messages import ExportChatInviteRequest

btext = "It looks like you're anonymous. Tap this button to confirm your identity."

@tbot.on(events.NewMessage(pattern="^[!/?.]promote ?(.*)"))
async def _(event):
 if event.is_private:
      return await event.reply("This command is made to be used in group chats, not in pm!")
 if event.from_id:
  if not await is_admin(event, event.sender_id):
      return await event.reply("You need to be an admin to do this.")
  if not await can_promote_users(message=event):
      return await event.reply("You are missing the following rights to use this command:CanAddAdmins!")
  try:
     user, title = await get_user(event)
  except TypeError:
     pass
  if not title:
   title = "Admin"
  if await is_admin(event, user.id):
   return await event.reply("This user is already an admin!")
  try:
   await tbot(EditAdminRequest(event.chat_id, user.id, ChatAdminRights(
                    add_admins=False,
                    invite_users=True,
                    change_info=False,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True), rank=title))
   await event.respond(f"Promoted **{user.first_name}** in **{event.chat.title}**!")
  except:
   await event.reply("Seems like I don't have enough rights to do that.")
 elif event.from_id == None:
   try:
     user, title = await get_user(event)
   except TypeError:
     pass
   if not title:
    title = "Admin"
   nfo = f"{user.id}-{title}"
   buttons = Button.inline("Click to prove Admin", data="apromote_{}".format(nfo))
   await event.respond(btext, buttons=buttons)

@tbot.on(events.NewMessage(pattern="^[!/?.]superpromote ?(.*)"))
async def _(event):
 if event.is_private:
      return await event.reply("This command is made to be used in group chats, not in pm!")
 if event.from_id:
  if not await is_admin(event, event.sender_id):
      return await event.reply("You need to be an admin to do this.")
  if not await can_promote_users(message=event):
      return await event.reply("You are missing the following rights to use this command:CanAddAdmins!")
  try:
     user, title = await get_user(event)
  except:
     pass
  if not title:
   title = "Admin"
  if await is_admin(event, user.id):
   return await event.reply("This user is already an admin!")
  try:
   await tbot(EditAdminRequest(event.chat_id, user.id, ChatAdminRights(
                    add_admins=True,
                    invite_users=True,
                    change_info=True,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True), rank=title))
   await event.respond(f"Promoted **{user.first_name}** in **{event.chat.title}** With full Rights!")
  except:
   await event.reply("Seems like I don't have enough rights to do that.")   
   
   
@tbot.on(events.NewMessage(pattern="^[!/?.]demote ?(.*)"))
async def _(event):
 if event.is_private:
      return await event.reply("This command is made to be used in group chats, not in pm!")
 if event.from_id:
  if not await is_admin(event, event.sender_id):
      return await event.reply("You need to be an admin to do this.")
  if not await can_promote_users(message=event):
      return await event.reply("You are missing the following rights to use this command:CanAddAdmins!")
  try:
     user, title = await get_user(event)
  except:
     pass
  if not title:
   title = "Admin"
  if not await is_admin(event, user.id):
      return await event.reply("This user is not an admin!")
  try:
   await tbot(EditAdminRequest(event.chat_id, user.id, ChatAdminRights(
                    add_admins=False,
                    invite_users=None,
                    change_info=None,
                    ban_users=None,
                    delete_messages=None,
                    pin_messages=None), rank="Not Admin"))
   await event.respond(f"Demoted **{user.first_name}**!")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 elif event.from_id == None:
    try:
     user, title = await get_user(event)
    except:
     pass
    if not title:
     title = "Admin"
    title = None
    nfo = f"{event.chat_id}-{user.id}-demote-{title}"
    buttons = Button.inline("Click to prove Admin", data="anonymous_{}".format(nfo))
    await event.respond(btext, buttons=buttons)

@tbot.on(events.NewMessage(pattern="^[!/?.]adminlist"))
async def admeene(event):
 if event.is_private:
      return await event.reply("This command is made to be used in group chats, not in pm!")
 if not await is_admin(event, BOT_ID):
      return
 mentions = f"Admins in **{event.chat.title}:**"
 async for user in tbot.iter_participants(
            event.chat_id, filter=ChannelParticipantsAdmins
        ):
           if not user.bot:
            if not user.deleted:
              if user.username:
                link_unf = '- @{}'
                link = link_unf.format(user.username)
                mentions += f"\n{link}"
 mentions += "\n\nNote: These values are up-to-date"
 await event.reply(mentions)

@Ebot(pattern="^/invitelink")
async def link(event):
 if event.is_private:
    return await event.reply("This cmd is made to be used in groups, not in PM!")
 if event.from_id:
  link = await tbot(ExportChatInviteRequest(event.chat_id))
  await event.reply(f"`{link.link}`", link_preview=False)
 elif event.from_id == None:
  buttons = Button.inline("Click to prove Admin", data="invitelink")
  await event.respond(btext, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"invitelink"))
async def _(event):
 if not await is_admin(event, event.sender_id):
  return await event.answer("You need to be an admin to do this.")
 link = await tbot(ExportChatInviteRequest(event.chat_id))
 await event.edit(f"`{link.link}`", link_preview=False, buttons=None)

@tbot.on(events.CallbackQuery(pattern=r"apromote(\_(.*))"))
async def _(event):
 tata = event.pattern_match.group(1)
 data = tata.decode()
 input = data.split("_", 1)[1]
 user_id, title = input.split("-", 1)
 user_id = user_id.strip()
 title = title.strip()
 if not await is_admin(event, event.sender_id):
      return await event.answer("You need to be an admin to do this.")
 if not await can_promote_users(message=event):
      return await event.edit("You are missing the following rights to use this command:CanAddAdmins!")
 if await is_admin(event, user_id):
   return await event.edit("This user is already an admin")
 if not title:
  title = "Admin"
 try:
   await tbot(EditAdminRequest(event.chat_id, user.id, ChatAdminRights(
                    add_admins=False,
                    invite_users=True,
                    change_info=True,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True), rank=title))
   await event.edit(f"Promoted **{user.first_name}** in **{event.chat.title}**!")
 except:
   await event.edit("Seems like I don't have enough rights to do that.")
 
@tbot.on(events.CallbackQuery(pattern=r"ademote(\_(.*))"))
async def _(event):
 tata = event.pattern_match.group(1)
 data = tata.decode()
 input = data.split("_", 1)[1]
 user_id, title = input.split("-", 1)
 user_id = user_id.strip()
 title = title.strip()
 if not await is_admin(event, event.sender_id):
      return await event.answer("You need to be an admin to do this.")
 if not await can_promote_users(message=event):
      return await event.edit("You are missing the following rights to use this command:CanAddAdmins!")
 if not await is_admin(event, user_id):
   return await event.edit("This user is not an Admin!")
 try:
   await tbot(EditAdminRequest(event.chat_id, user.id, ChatAdminRights(
                    add_admins=False,
                    invite_users=None,
                    change_info=None,
                    ban_users=None,
                    delete_messages=None,
                    pin_messages=None), rank="Not Admin"))
   await event.edit(f"Demoted **{user.first_name}**!")
 except:
   await event.edit("Seems like I don't have enough rights to do that.")
 
 
 
__help__ = """
**Admin Commands:**
- /promote: promote a user.
- /demote: demotes a user.
- /superpromote: promotes a user with full rights except anonymous.
- /adminlist: shows the admins of the chat.
- /invitelink: gets the chat invite link.
"""

