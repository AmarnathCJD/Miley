from Evie import tbot, CMD_HELP
from Evie.events import register
from Evie.function import can_change_info
import os
from telethon.tl import types, functions
from Evie import *
from Evie.modules.sql.notes_sql import add_note, get_all_notes, get_notes, remove_note
from telethon import events

@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def on_note(event):
    name = event.pattern_match.group(1)
    note = get_notes(event.chat_id, name)
    if not note is None:
      message_id = event.sender_id
      if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    await event.reply(note.reply, reply_to=message_id)

@register(pattern="^/save ?(.*)")
async def _(event):
    print(2)
    if event.is_group:
      if not is_admin(event, event.sender_id):
        await event.reply("You need to be an admin to do this.")
        return
      if not await can_change_info(message=event):
        await event.reply("You are missing the following rights to use this command:CanChangeInfo")
        return
    else:
        return
    if not event.reply_to_msg_id:
     input = event.pattern_match.group(1)
     if input:
       arg = input.split(" ", 1)
     if len(arg) == 2:
      name = arg[0]
      msg = arg[1]
    print(1)
    if msg:
        note = msg
        add_note(
            event.chat_id,
            name,
            note,
        )
        await event.reply(
            "Saved note `{}`".format(name=name)
        )
    else:
        await event.reply("Reply to a message with /addnote keyword to save the note")
