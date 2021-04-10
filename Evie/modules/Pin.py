from Evie import tbot, CMD_HELP, OWNER_ID
import os
from telethon import types, functions, Button, events
from Evie.events import register
from Evie.function import is_admin, is_register_admin


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
   message = await tbot.get_messages(event.chat_id, ids=types.InputMessagePinned())
   id = message.id
   chat = event.chat_id
   pro = f'{chat}'
   omk = pro.replace('-100', '')
   if event.chat.username:
     await event.reply(f"The pinned message in {event.chat.title} is [here](http://t.me/{event.chat.username}/{id}).", link_preview=False)
   else:
     await event.reply(f"The pinned message in {event.chat.title} is [here](http://t.me/{omk}/{id}).", link_preview=False)

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
    await msg.reply("I have pinned this [message](http://t.me/{lik}/{to_pin.id}).")
 except Exception as e:
    await msg.reply(f'{e}')



@tbot.on(events.ChatAction)
async def handler(event):
  if event.new_pin:
     print(99)
