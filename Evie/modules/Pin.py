from Evie import tbot, CMD_HELP
import os
from telethon import types, functions, Button
from Evie.events import register
from Evie.function import is_admin


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
    
