"""
Fully Written by RoseLoverX
"""
from Evie import tbot, CMD_HELP, OWNER_ID
import os, re, csv, json, time, uuid
from Evie.function import is_admin
from io import BytesIO
import Evie.modules.sql.feds_sql as sql
from Evie.modules.sql.feds_sql import FEDS_SUBSCRIBER as luv
from telethon import *
from telethon import Button
from telethon.tl import *
from telethon.tl.types import User
from Evie import *
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageMediaDocument, DocumentAttributeFilename
from Evie.events import register

"""
Fully Written by RoseLoverX
"""

from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
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


"""
Fully Written by RoseLoverX
"""

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
        fname = previous_message.sender.first_name
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            return

        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj

def is_user_fed_admin(fed_id, user_id):
    fed_admins = sql.all_fed_users(fed_id)
    if fed_admins is False:
        return False
    if int(user_id) in fed_admins or int(user_id) == OWNER_ID:
        return True
    else:
        return False


def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = eval(getsql["fusers"])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner["owner"]
    if str(user_id) == getfedowner or int(user_id) == OWNER_ID:
        return True
    else:
        return False


"""
Fully Written by RoseLoverX
"""
@register(pattern="^/newfed ?(.*)")
async def new(event):
 if not event.is_private:
  return await event.reply("Create your federation in my PM - not in a group.")
 name = event.pattern_match.group(1)
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if fedowner:
    for f in fedowner:
            text = "{}".format(f["fed"]["fname"])
    return await event.reply(f"You already have a federation called `{text}` ; you can't create another. If you would like to rename it, use /renamefed.")
 if not name:
  return await event.reply("You need to give your federation a name! Federation names can be up to 64 characters long.")
 if len(name) > 64:
  return await event.reply("Federation names can only be upto 64 charactors long.")
 fed_id = str(uuid.uuid4())
 fed_name = name
 x = sql.new_fed(event.sender_id, fed_name, fed_id)
 return await event.reply(f"Created new federation with FedID: `{fed_id}`.\nUse this ID to join the federation! eg:\n`/joinfed {fed_id}`")

@register(pattern="^/delfed")
async def smexy(event):
 if not event.is_private:
  return await event.reply("Delete your federation in my PM - not in a group.")
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
  return await event.reply("It doesn't look like you have a federation yet!")
 for f in fedowner:
            fed_id = "{}".format(f["fed_id"])
            name = f["fed"]["fname"]
 await tbot.send_message(
            event.chat_id,
            "Are you sure you want to delete your federation? This action cannot be undone - you will lose your entire ban list, and '{}' will be permanently gone.".format(name),
            buttons=[
                [Button.inline("Delete Federation", data="rmfed_{}".format(fed_id))],
                [Button.inline("Cancel", data="nada")],
            ],
        )

@tbot.on(events.CallbackQuery(pattern=r"rmfed(\_(.*))"))
async def delete_fed(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    fed_id = data.split("_", 1)[1]
    delete = sql.del_fed(fed_id)
    await event.edit("You have deleted your federation! All chats linked to it are now federation-less.")

@tbot.on(events.CallbackQuery(pattern=r"nada"))
async def delete_fed(event):
  await event.edit("Federation deletion canceled")

@register(pattern="^/renamefed ?(.*)")
async def cgname(event):
 if not event.is_private:
   return await event.reply("You can only rename your fed in PM.")
 user_id = event.sender_id
 newname = event.pattern_match.group(1)
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
  return await event.reply("It doesn't look like you have a federation yet!")
 if not newname:
  return await event.reply("You need to give your federation a new name! Federation names can be up to 64 characters long.")
 for f in fedowner:
            fed_id = f["fed_id"]
            name = f["fed"]["fname"]
 sql.rename_fed(fed_id, user_id, newname)
 return await event.reply(f"Tada! I've renamed your federation from '{name}' to '{newname}'. [FedID: `{fed_id}`].")

@register(pattern="^/chatfed")
async def cf(event):
 chat = event.chat_id
 if event.is_private:
   return
 if not await is_admin(event, event.sender_id):
   return await event.reply("You need to be an admin to do this.")
 fed_id = sql.get_fed_id(chat)
 if not fed_id:
  return await event.reply("This chat isn't part of any feds yet!")
 info = sql.get_fed_info(fed_id)
 name = info["fname"]
 await event.reply(f"Chat {event.chat.title} is part of the following federation: {name} [ID: `{fed_id}`]")
 
@register(pattern="^/joinfed ?(.*)")
async def jf(event):
 if not event.is_group:
   return
 if not await is_admin(event, event.sender_id):
   await event.reply("You need to be an admin to do this.")
   return
 permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
 if not permissions.is_creator:
          return await event.reply(f"You need to be the chat owner of {event.chat.title} to do this.")
 args = event.pattern_match.group(1)
 if not args:
   return await event.reply("You need to specify which federation you're asking about by giving me a FedID!")
 if len(args) < 8:
   return await event.reply("This isn't a valid FedID format!")
 getfed = sql.search_fed_by_id(args)
 name = getfed["fname"]
 if not getfed:
  return await event.reply("This FedID does not refer to an existing federation.")
 fed_id = sql.get_fed_id(event.chat_id)
 if fed_id:
    sql.chat_leave_fed(event.chat_id)
 x = sql.chat_join_fed(args, event.chat.title, event.chat_id)
 return await event.reply(f'Successfully joined the "{name}" federation! All new federation bans will now also remove the members from this chat.')
 
@register(pattern="^/leavefed")
async def lf(event):
 if not event.is_group:
   return
 if not await is_admin(event, event.sender_id):
   await event.reply("You need to be an admin to do this.")
   return
 permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
 if not permissions.is_creator:
          return await event.reply(f"You need to be the chat owner of {event.chat.title} to do this.")
 chat = event.chat_id
 fed_id = sql.get_fed_id(chat)
 if not fed_id:
   return await event.reply("This chat isn't currently in any federations!")
 fed_info = sql.get_fed_info(fed_id)
 name = fed_info["fname"]
 sql.chat_leave_fed(chat)
 return await event.reply(f'Chat {event.chat.title} has left the " {name} " federation.')

@register(pattern="^/fpromote ?(.*)")
async def p(event):
 if event.is_private:
  return await event.reply("This command is made to be run in a group where the person you would like to promote is present.")
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
   return await event.reply("Only federation creators can promote people, and you don't seem to have a federation to promote to!")
 args = await get_user_from_event(event)
 if not args:
   return await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
 chat = event.chat
 for f in fedowner:
            fed_id = f["fed_id"]
            name = f["fed"]["fname"]
 user_id = args.id
 fban, fbanreason, fbantime = sql.get_fban_user(fed_id, int(args.id))
 replied_user = await tbot(GetFullUserRequest(user_id))
 fname = replied_user.user.first_name
 print(69)
 if fban:
  if fbanreason != '':
   return await event.reply(f"User {fname} is fbanned in {name}. You should unfban them before promoting.\n\nReason:\n{fbanreason}")
  else:
   return await event.reply(f"User {fname} is fbanned in {name}. You should unfban them before promoting.")
 getuser = sql.search_user_in_fed(fed_id, user_id)
 if getuser:
   return await event.reply(f"[{fname}](tg://user?id={args.id}) is already an admin in {name}!")
 print(4)
 try:
  mk = f"{user_id}|{name[:5]}|{fed_id}"
  km = f"{user_id}|{event.sender_id}"
  await tbot.send_message(
            event.chat_id,
            f"Please get [{fname}](tg://user?id={args.id}) to confirm that they would like to be fed admin for {name}",
            buttons=[
                Button.inline("Confirm", data="fkfed_{}".format(mk)),
                Button.inline("Cancel", data="smex_{}".format(km)),
            ],
        )
 except Exception as e:
    print(e)
            

"""
Fully Written by RoseLoverX
"""
@tbot.on(events.CallbackQuery(pattern=r"fkfed(\_(.*))"))
async def smex_fed(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  input = data.split("_", 1)[1]
  user, owner, fed_id= input.split("|")
  user = user.strip()
  name = owner.strip()
  fed_id = fed_id.strip()
  rt = await tbot(GetFullUserRequest(int(user)))
  fname = rt.user.first_name
  if not event.sender_id == int(user):
    return await event.answer("You are not the user being fpromoted")
  res = sql.user_join_fed(fed_id, int(user))
  if res:
     return await event.edit(f"User [{fname}](tg://user?id={user}) is now an admin of {name} [{fed_id}]")

"""
Fully Written by RoseLoverX
"""
@tbot.on(events.CallbackQuery(pattern=r"smex(\_(.*))"))
async def smex(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  input = data.split("_", 1)[1]
  user, owner= input.split("|")
  user = user.strip()
  owner = owner.strip()
  if event.sender_id == int(owner):
     rt = await tbot(GetFullUserRequest(int(owner)))
     fname = rt.user.first_name
     await event.edit(f"Fedadmin promotion cancelled by [{fname}](tg://user?id={owner})")
     return
  if event.sender_id == int(user):
     rt = await tbot(GetFullUserRequest(int(user)))
     fname = rt.user.first_name
     await event.edit(f"Fedadmin promotion has been refused by [{fname}](tg://user?id={user}).")
     return
  await event.answer("You are not the user being fpromoted")

@register(pattern="^/fdemote ?(.*)")
async def fd(event):
 if event.is_private:
  return await event.reply("This command is made to be run in a group where the person you would like to promote is present.")
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
   return await event.reply("Only federation creators can promote people, and you don't seem to have a federation to promote to!")
 args = await get_user_from_event(event)
 if not args:
   return await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
 chat = event.chat
 for f in fedowner:
            fed_id = f["fed_id"]
            name = f["fed"]["fname"]
 user_id = args.id
 if sql.search_user_in_fed(fed_id, user_id) is False:
    return await event.reply(f"This person isn't a federation admin for '{name} ', how could I demote them?")
 replied_user = await tbot(GetFullUserRequest(user_id))
 fname = replied_user.user.first_name
 sql.user_demote_fed(fed_id, user_id)
 return await event.reply(f"User [{fname}](tg://user?id={user_id}) is no longer an admin of {name} ({fed_id})")
 
@register(pattern="^/fedinfo ?(.*)")
async def info(event):
 if not event.is_private:
   if not await is_admin(event, event.sender_id):
     return await event.reply("This command can only be used in private.")
 input = event.pattern_match.group(1)
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not input:
  if not fedowner:
   return await event.reply("You need to give me a FedID to check, or be a federation creator to use this command!")
 if input:
   fed_id = input
   info = sql.get_fed_info(fed_id)
   if not info:
      return await event.reply("There is no federation with this FedID.")
   name = info["fname"]
 elif fedowner:
   for f in fedowner:
            fed_id = f["fed_id"]
            name = f["fed"]["fname"]
   info = sql.get_fed_info(fed_id)
 if info:
  owner = int(info["owner"])
  getfban = sql.get_all_fban_users(fed_id)
  getfchat = sql.all_fed_chats(fed_id)
  FEDADMIN = sql.all_fed_users(fed_id)
  TotalAdminFed = len(FEDADMIN)
  
  caption = "Fed info:\n"
  caption += f"FedID: `{fed_id}`\n"
  caption += f"Name: {name}\n"
  caption += f"Creator: [this person](tg://user?id={owner})\n"
  caption += f"Number of admins: `{TotalAdminFed}`\n"
  caption += f"Number of bans: `{len(getfban)}`\n"
  caption += f"Number of connected chats: `{len(getfchat)}`\n"
  try:
     subs = sql.get_subscriber(fed_id)
  except:
     subs = []
  caption += f"Number of subscribed feds: `{len(subs)}`"
  if len(getmy) == 0:
   caption += "\n\nThis federation is not subscribed to any other feds."
  else:
     caption += "\n\nSubscribed to the following feds:"
     for x in getmy:
                nfo = sql.get_fed_info(x)
                nme = nfo["fname"]
                caption += f"\n- {nme} (`{x}`)"
  buttons = Button.inline("Check Fed Admins", data="fedadm_{}".format(fed_id))
  await tbot.send_message(event.chat_id, caption, buttons=buttons)


"""
Fully Written by RoseLoverX
"""
@tbot.on(events.CallbackQuery(pattern=r"fedadm(\_(.*))"))
async def smex_fed(event):
  if event.is_group:
    if not await is_admin(event, event.sender_id):
      return await event.answer("You need to be an admin to do this")
  await event.edit(buttons=None)
  tata = event.pattern_match.group(1)
  data = tata.decode()
  input = data.split("_", 1)[1]
  fed_id = input
  info = sql.get_fed_info(fed_id)
  try:
        text = "Admins in federation '{}':\n".format(info["fname"])
        owner = await tbot.get_entity(int(info["owner"]))
        try:
            owner_name = owner.first_name + " " + owner.last_name
        except:
            owner_name = owner.first_name
        text += f"- [{owner_name}](tg://user?id={owner.id}) (`{owner.id}`)\n"

        members = sql.all_fed_members(fed_id)
        for x in members:
          try:
            user = await tbot.get_entity(int(x))
            unamee = user.first_name
            text += f"- [{unamee}](tg://user?id={user.id}) (`{user.id}`)"
          except Exception:
            text += f"- {x}/n"
  except Exception as e:
   print(e)
  await event.reply(text)

"""
Fully Written by RoseLoverX
"""
@register(pattern="^/fban ?(.*)")
async def _(event):
    user = event.sender
    chat = event.chat_id
    if event.is_group:
        fed_id = sql.get_fed_id(chat)
        if not fed_id:
           return await event.reply("This chat isn't in any federations.")
    else:
      fedowner = sql.get_user_owner_fed_full(event.sender_id)
      if not fedowner:
          return await event.reply("It doesn't look like you have a federation yet!")
      for f in fedowner:
            fed_id = "{}".format(f["fed_id"])
    info = sql.get_fed_info(fed_id)
    name = info["fname"]
    if is_user_fed_admin(fed_id, user.id) is False:
      return await event.reply(f"You aren't a federation admin for {name}!")
    input = event.pattern_match.group(1)
    if input:
      arg = input.split(" ", 1)
    if not event.reply_to_msg_id:
     if len(arg) == 2:
        iid = arg[0]
        reason = arg[1]
     else:
        iid = arg[0]
        reason = None
     if not iid.isnumeric():
        entity = await tbot.get_input_entity(iid)
        try:
          r_sender_id = entity.user_id
        except Exception:
           await event.reply("Couldn't fetch that user.")
           return
     else:
        r_sender_id = int(iid)
     try:
        replied_user = await tbot(GetFullUserRequest(r_sender_id))
        fname = replied_user.user.first_name
        username = replied_user.user.username
        lname = replied_user.user.last_name
     except Exception:
        fname = "User"
        username = None
        lname = None
    else:
        reply_message = await event.get_reply_message()
        iid = reply_message.sender_id
        fname = reply_message.sender.first_name
        lname = reply_message.sender.last_name
        username = reply_message.sender.username
        if input:
          reason = input
        else:
          reason = None
        r_sender_id = iid
    if r_sender_id == BOT_ID or r_sender_id == OWNER_ID:
        return await event.reply("Oh you're a funny one aren't you! I am _not_ going to fedban myself.")
    name = info["fname"]
    if is_user_fed_owner(fed_id, int(r_sender_id)) is True:
           return await event.reply(f"I'm not banning a fed admin from their own fed! [{name}]")
    if is_user_fed_admin(fed_id, int(r_sender_id)) is True:
           return await event.reply(f"I'm not banning a fed admin from their own fed! [{name}]")
    fban_user_id = int(r_sender_id)
    fban_user_name = fname
    fban_user_lname = lname
    fban_user_uname = username
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, int(r_sender_id))
    if fban:
      if fbanreason == '' and reason == None:
         return await event.reply(f'User [{fname}](tg://)/user?id={r_sender_id}) is already banned in {name}. There is no reason set for their fedban yet, so feel free to set one.')
      if reason == fbanreason:
         return await event.reply(f'User [{fname}](tg://user?id={r_sender_id}) has already been fbanned, with the exact same reason.')
      if reason == None:
       if fbanreason == '':
         return await event.reply(f'User [{fname}](tg://user?id={r_sender_id}) is already banned in {name}.')
       else:
         return await event.reply(f'User [{fname}](tg://user?id={r_sender_id}) is already banned in {name}, with reason:\n`{fbanreason}`.')
    if not fban:
       x = sql.fban_user(
                fed_id,
                fban_user_id,
                fban_user_name,
                fban_user_lname,
                fban_user_uname,
                reason,
                int(time.time()),
            )
       sax = "**New FedBan**\n"
       sax += f"**Fed:** {name}\n"
       sax += f"**FedAdmin:** [{event.sender.first_name}](tg://user?id={event.sender_id})\n"
       sax += f"**User:** [{fname}](tg://user?id={r_sender_id})\n"
       sax += f"**User ID:** `{r_sender_id}`\n"
       sax += f"**Reason:** {reason}"
    else:
            fed_name = info["fname"]
            temp = sql.un_fban_user(fed_id, fban_user_id)
            if not temp:
                await event.reply("Failed to update the reason for fedban!")
                return
            x = sql.fban_user(
                fed_id,
                fban_user_id,
                fban_user_name,
                fban_user_lname,
                fban_user_uname,
                reason,
                int(time.time()),
            )
            sax = "**FedBan Reason Update**\n"
            sax += f"**Fed:** {name}\n"
            sax += f"**FedAdmin:** [{event.sender.first_name}](tg://user?id={event.sender_id})\n"
            sax += f"**User:** [{fname}](tg://user?id={r_sender_id})\n"
            sax += f"**User ID:** `{r_sender_id}`\n"
            if not fbanreason == '':
              sax += f"**Previous Reason:** {fbanreason}\n"
            sax += f"**New Reason:** {reason}"
    await tbot.send_message(
                event.chat_id,
                sax)
    getfednotif = sql.user_feds_report(info["owner"])
    if getfednotif:
      if int(info["owner"]) != int(chat):
         await tbot.send_message(
                int(info["owner"]),
                sax)
    get_fedlog = sql.get_fed_log(fed_id)
    if get_fedlog:
        if int(get_fedlog) != int(chat):
           await tbot.send_message(
                int(get_fedlog),
                sax)
    fed_chats = list(sql.all_fed_chats(fed_id))
    if len(fed_chats) != 0:
        for fedschat in fed_chats:
                try:
                    await tbot(
                        EditBannedRequest(int(fedschat), int(fban_user_id), BANNED_RIGHTS)
                        )
                except Exception:
                    pass
    subscriber = list(sql.get_subscriber(fed_id))
    if len(subscriber) != 0:
           for fedsid in subscriber:
                 all_fedschat = sql.all_fed_chats(fedsid)
                 for fedschat in all_fedschat:
                     try:
                        await tbot(
                        EditBannedRequest(int(fedschat), int(fban_user_id), BANNED_RIGHTS)
                        )
                     except Exception:
                            continue
    

"""
Fully Written by RoseLoverX
"""
@register(pattern="^/unfban ?(.*)")
async def unfban(event):
    user = event.sender
    chat = event.chat_id
    if event.is_group:
        fed_id = sql.get_fed_id(chat)
        if not fed_id:
           return await event.reply("This chat isn't in any federations.")
    else:
      fedowner = sql.get_user_owner_fed_full(event.sender_id)
      if not fedowner:
          return await event.reply("It doesn't look like you have a federation yet!")
      for f in fedowner:
            fed_id = "{}".format(f["fed_id"])
    info = sql.get_fed_info(fed_id)
    name = info["fname"]
    if is_user_fed_admin(fed_id, user.id) is False:
      return await event.reply(f"You aren't a federation admin for {name}!")
    input = event.pattern_match.group(1)
    if input:
      arg = input.split(" ", 1)
    if not event.reply_to_msg_id:
     if len(arg) == 2:
        iid = arg[0]
        reason = arg[1]
     else:
        iid = arg[0]
        reason = None
     if not iid.isnumeric():
        entity = await tbot.get_input_entity(iid)
        try:
          r_sender_id = entity.user_id
        except Exception:
           await event.reply("Couldn't fetch that user.")
           return
     else:
        r_sender_id = int(iid)
     try:
        replied_user = await tbot(GetFullUserRequest(r_sender_id))
        fname = replied_user.user.first_name
        username = replied_user.user.username
        lname = replied_user.user.last_name
     except Exception:
        fname = "User"
        username = None
        lname = None
    else:
        reply_message = await event.get_reply_message()
        iid = reply_message.sender_id
        fname = reply_message.sender.first_name
        lname = reply_message.sender.last_name
        username = reply_message.sender.username
        if input:
          reason = input
        else:
          reason = None
        r_sender_id = iid
    if r_sender_id == BOT_ID or r_sender_id == OWNER_ID:
        return await event.reply("Oh you're a funny one aren't you! How do you think I would have fbanned myself hm?.")
    name = info["fname"]
    fban_user_id = int(r_sender_id)
    fban_user_name = fname
    fban_user_lname = lname
    fban_user_uname = username
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, int(r_sender_id))
    if not fban:
      return await event.reply(f"This user isn't banned in the current federation, {name}. [{fed_id}]")
    temp = sql.un_fban_user(fed_id, fban_user_id)
    if temp:
      sxa = "**New un-FedBan**\n"
      sxa += f"**Fed:** {name}\n"
      sxa += f"**FedAdmin:** [{event.sender.first_name}](tg://user?id={event.sender_id})\n"
      sxa += f"**User:** [{fname}](tg://user?id={r_sender_id})\n"
      sxa += f"**User ID:** `{r_sender_id}`\n"
      if reason:
        sxa += f"**Reason:** {reason}"
      await tbot.send_message(
                event.chat_id,
                sxa)
      getfednotif = sql.user_feds_report(info["owner"])
      if getfednotif:
        if int(info["owner"]) != int(chat):
          await tbot.send_message(
                int(info["owner"]),
                sxa)
      get_fedlog = sql.get_fed_log(fed_id)
      if get_fedlog:
         if int(get_fedlog) != int(chat):
           await tbot.send_message(
                int(get_fedlog),
                sxa)
     
@register(pattern="^/setfedlog ?(.*)")
async def log(event):
 chat = event.chat_id
 if not is_admin(event, event.sender_id):
   return await event.reply("You need to be an admin to do this")
 args = event.pattern_match.group(1)
 if not args:
   fedowner = sql.get_user_owner_fed_full(event.sender_id)
   if not fedowner:
     return await event.reply("Only fed creators can set a fed log - but you don't have a federation!")
   for f in fedowner:
            args = "{}".format(f["fed_id"])
            name = f["fed"]["fname"]
 else:
   if len(args) < 8:
      return await event.reply("This isn't a valid FedID format!")
   getfed = sql.search_fed_by_id(args)
   name = getfed["fname"]
   if not getfed:
     return await event.reply("This FedID does not refer to an existing federation.")
 setlog = sql.set_fed_log(args, chat)
 await event.reply(f"This has been set as the fed log for {name} - all fed related actions will be logged here.")

@register(pattern="^/unsetfedlog")
async def ligunset(event):
 chat = event.chat_id
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
     return await event.reply("Only fed creators can unset a fed log - but you don't have a federation!")
 for f in fedowner:
            args = f["fed_id"]
            name = f["fed"]["fname"]
 setlog = sql.set_fed_log(args, None)
 await event.reply(f"The {name} federation has had its log location unset.")

"""
Fully Written by AmarnathCdj aka RoseloverX
"""
@register(pattern="^/subfed ?(.*)")
async def sub(event):
 args = event.pattern_match.group(1)
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
     return await event.reply("Only federation creators can subscribe to a fed. But you don't have a federation!")
 for f in fedowner:
            fed_id = f["fed_id"]
            name = f["fed"]["fname"]
 if not args:
  return await event.reply("You need to specify which federation you're asking about by giving me a FedID!")
 if len(args) < 8:
      return await event.reply("This isn't a valid FedID format!")
 getfed = sql.search_fed_by_id(args)
 if not getfed:
    return await event.reply("This FedID does not refer to an existing federation.")
 sname = getfed["fname"]
 if args == fed_id:
   return await event.reply("... What's the point in subscribing a fed to itself?")
 try:
   subs = sql.MYFEDS_SUBSCRIBER
 except:
   subs = []
 if len(subs) <= 5:
  return await event.reply("You can subscribe to at most 5 federations. Please unsubscribe from other federations before adding more.")
 subfed = sql.subs_fed(args, fed_id)
 addsub = sql.add_sub(fed_id, args)
 await event.reply(f"Federation {name} has now subscribed to {sname}. All fedbans in {sname} will now take effect in both feds.")

"""
Fully Written by RoseLoverX aka AmarnathCdj
"""

@register(pattern="^/unsubfed ?(.*)")
async def unsub(event):
 args = event.pattern_match.group(1)
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if not fedowner:
     return await event.reply("Only federation creators can unsubscribe from a fed. But you don't have a federation!")
 for f in fedowner:
            fed_id = f["fed_id"]
            name = f["fed"]["fname"]
 if not args:
  return await event.reply("You need to specify which federation you're asking about by giving me a FedID!")
 if len(args) < 8:
      return await event.reply("This isn't a valid FedID format!")
 getfed = sql.search_fed_by_id(args)
 if not getfed:
    return await event.reply("This FedID does not refer to an existing federation.")
 sname = getfed["fname"]
 unsubfed = sql.unsubs_fed(args, fed_id)
 await event.reply(f"Federation {name} is no longer subscribed to {sname}. Bans in {sname} will no longer be applied.\nPlease note that any bans that happened because the user was banned from the subfed will need to be removed manually.")
 
@register(pattern="^/fstat ?(.*)")
async def fstat(event):
 if event.is_group:
   if not await is_admin(event, event.sender_id):
     return await event.reply("You need to be an admin to do this!")
 args = event.pattern_match.group(1)
 if args:
  if len(args) > 12:
    info = sql.get_fed_info(args)
    if not info:
      return await event.reply("There is no federation with this FedID.")
    name = info["fname"]
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        user_id = msg.sender_id
        fname = msg.sender.first_name
    else:
        user_id = event.sender_id
        fname = event.sender.first_name
  elif len(args) < 12:
   person = await get_user_from_event(event)
   user_id = person.id
   replied_user = await tbot(GetFullUserRequest(user_id))
   fname = replied_user.user.first_name
 else:
   if event.reply_to_msg_id:
      msg = await event.get_reply_message()
      user_id = msg.sender_id
      fname = msg.sender.first_name
   else:
      user_id = event.sender_id
      fname = event.sender.first_name
 mex = await event.reply(f"Checking fbans for {fname}...")
 uname, fbanlist = sql.get_user_fbanlist(str(user_id))
 if len(fbanlist) == 0:
   return await mex.edit(f"User {fname} hasn't been banned in any chats due to fedbans.")
 
 
 
