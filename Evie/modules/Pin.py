from Evie import tbot, CMD_HELP, OWNER_ID
import os, asyncio
from Evie.modules.sql.antipin_sql import add_chat, rmchat, is_chat, get_all_chat_id, is_pin, rmpin, add_pin
from telethon import types, functions, Button, events
from Evie.events import register
from Evie.function import is_admin, is_register_admin
from telethon.tl.functions.messages import UpdatePinnedMessageRequest

async def can_pin_msg(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.pin_messages
    )

@register(pattern="^/pinned")
async def pn(event):
   x = await event.reply("`Getting the pinned message..`")
   try:
     message = await tbot.get_messages(event.chat_id, ids=types.InputMessagePinned())
   except:
     return await x.edit("There are no pinned messages in this chat.")
   id = message.id
   chat = event.chat_id
   pro = f'{chat}'
   omk = pro.replace('-100', '')
   if event.chat.username:
     await x.edit(f"The pinned message in {event.chat.title} is [here](http://t.me/{event.chat.username}/{id}).", link_preview=False)
   else:
     await x.edit(f"The pinned message in {event.chat.title} is [here](http://t.me/{omk}/{id}).", link_preview=False)

@register(pattern="^/unpinall")
async def upinall(event):
  permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
  if not permissions.is_creator:
     if not await is_admin(event, event.sender_id):
       return await event.reply("You need to be an admin to do this!")
     if not await can_pin_msg(event):
       return await event.reply("You are missing the following rights to use this command:CanPinMessages")
  text = "Are you sure you want to unpin all messages?"
  buttons = [Button.inline('Yes', data='upin'),Button.inline('No', data='cpin')]
  await tbot.send_message(
                event.chat_id,
                text,
                buttons=buttons)
    

@tbot.on(events.CallbackQuery(pattern=r"cpin"))
async def start_again(event):
        if not await is_admin(event, event.sender_id):
          return await event.answer("You need to be an admin to do this!")
        if not await can_pin_msg(event):
          return await event.answer("No enough permission for you!")
        await event.edit("Unpin of all pinned messages has been cancelled.", buttons=None)

@tbot.on(events.CallbackQuery(pattern=r"upin"))
async def start_again(event):
        if not await is_admin(event, event.sender_id):
          return await event.answer("You need to be an admin to do this!")
        if not await can_pin_msg(event):
          return await event.answer("No enough permission for you!")
        await tbot.unpin_message(event.chat_id)
        await event.edit("All pinned messages have been unpinned.", buttons=None)
        

@register(pattern="^/pin(?: |$)(.*)")
async def pin(msg):
 try:
    if msg.is_group:
      if not msg.sender_id == OWNER_ID:
        if not await is_register_admin(msg.input_chat, msg.sender_id):
           await msg.reply("Only admins can execute this command!")
           return
        
    else:
        return
    if not await can_pin_msg(message=msg):
            await msg.reply("You are missing the following rights to use this command:CanPinMessages")
            return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await msg.reply("You need to reply to a message to pin it!")
        return
    k = await msg.get_reply_message()
    options = msg.pattern_match.group(1)
    chat = f'{msg.chat_id}'
    lik = chat.replace("-100", "")
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await tbot(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except Exception:
        await msg.reply("Failed to pin.")
        return
    try:
       await msg.reply(f"I have pinned [this message](http://t.me/{event.chat.username}/{k.id}).")
    except:
       pass
 except Exception as e:
    await msg.reply(f'{e}')

@register(pattern="^/antichannelpin ?(.*)")
async def kr(event):
 args = event.pattern_match.group(1)
 if args:
  if not await is_admin(event, event.sender_id):
     return await event.reply("You need to be an admin to do this!")
  if args == 'on' or args == 'enable':
    if not is_chat(event.chat_id):
              await event.reply("**Enabled** anti channel pins. Automatic pins from a channel will now be replaced with the previous pin.")
              return add_chat(event.chat_id)
    else:
       return await event.reply("**Enabled** anti channel pins. Automatic pins from a channel will now be replaced with the previous pin.")
  elif args == 'off' or args == 'disable':
    if is_chat(event.chat_id):
             await event.reply("**Disabled** anti channel pins. Automatic pins from a channel will not be removed.")
             return rmchat(event.chat_id)
    else:
       return await event.reply("**Disabled** anti channel pins. Automatic pins from a channel will not be removed.")
 else:
    if is_chat(event.chat_id):
      return await event.reply(f"Anti channel pins are currently **enabled** in {event.chat.title}.")
    else:
      return await event.reply(f"Anti channel pins are currently **disabled** in {event.chat.title}.")

@register(pattern="^/cleanlinked ?(.*)")
async def kr(event):
 args = event.pattern_match.group(1)
 if args:
  if not await is_admin(event, event.sender_id):
     return await event.reply("You need to be an admin to do this!")
  if args == 'on' or args == 'enable':
    if not is_pin(event.chat_id):
              await event.reply(f"**Enabled** linked channel post deletion in {event.chat.title}. Messages sent from the linked channel will be deleted.")
              return add_pin(event.chat_id)
    else:
       return await event.reply(f"**Enabled** linked channel post deletion in {event.chat.title}. Messages sent from the linked channel will be deleted.")
  elif args == 'off' or args == 'disable':
    if is_pin(event.chat_id):
             await event.reply(f"**Disabled** linked channel post deletion in {event.chat.title}.")
             return rmpin(event.chat_id)
    else:
       return await event.reply(f"**Disabled** linked channel post deletion in {event.chat.title}.")
 else:
    if is_pin(event.chat_id):
      return await event.reply(f"Linked channel post deletion is currently **enabled** in {event.chat.title}. Messages sent from the linked channel will be deleted.")
    else:
      return await event.reply(f"Linked channel post deletion is currently **disabled** in {event.chat.title}.")

@tbot.on(events.NewMessage(pattern=None))
async def pk(event):
 if event.is_private:
   return
 if not event.fwd_from:
  return
 if not is_pin(event.chat_id):
   return
 from telethon import functions, types
 result = await tbot(functions.channels.GetFullChannelRequest(
        channel=event.chat.username
    ))
 s = result.chats
 for x in s:
   if not x.username == event.chat.username:
     id = x.id
 if not id == None:
  cid = event.fwd_from.from_id.channel_id
  if cid == id:
   await event.delete()


@tbot.on(events.NewMessage(pattern=None))
async def pk(event):
 if event.is_private:
   return
 if not is_chat(event.chat_id):
   return
 if not event.fwd_from:
  return
 from telethon import functions, types
 result = await tbot(functions.channels.GetFullChannelRequest(
        channel=event.chat.username
    ))
 s = result.chats
 for x in s:
   if not x.username == event.chat.username:
     id = x.id
 if not id == None:
  cid = event.fwd_from.from_id.channel_id
  if cid == id:
   await tbot.unpin_message(event.chat_id, event.message.id)

__help__ = """
All the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!

**User commands:**
- /pinned: Get the current pinned message.

**Admin commands:**
- /pin: Pin the message you replied to. Add 'loud' or 'notify' to send a notification to group members.
- /permapin <text>: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
- /unpin: Unpin the current pinned message. If used as a reply, unpins the replied to message.
- /unpinall: Unpins all pinned messages.
- /antichannelpin: Auto unpins all messages from linked channel if enabled.
- /cleanlinked: deletes all posts forwarded from linked channel if enabled.
"""

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})


