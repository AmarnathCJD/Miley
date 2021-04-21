from Evie import tbot, CMD_HELP
from Evie.events import register
from Evie.function import can_change_info, is_admin
import os
from telethon import custom, events, Button
from telethon.tl import types, functions
from Evie import *
from Evie.modules.sql.notes_sql import add_note, get_all_notes, get_notes, remove_note

from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
pnotes = db.pnotes

NAME = []

def get_chat(id):
    return pnotes.find_one({"id": id})

@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def on_note(event):
    global name
    name = event.pattern_match.group(1)
    note = get_notes(event.chat_id, name)
    if not note is None:
      message_id = event.sender_id
      if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    chats = pnotes.find({})
    mode = False
    for c in chats:
      if event.chat_id == c["id"]:
        mode = c["mode"]
    if mode == False:
      await event.reply(note.reply, reply_to=message_id)
    elif mode == True:
      text = f"Tap here to view '{name}' in your private chat."
      luv = f"{event.chat_id} {name}"
      buttons = Button.url("Click me", "t.me/MissEvie_Robot?start=notes_{}".format(luv))
    await event.reply(text, buttons=buttons)

@tbot.on(events.NewMessage(pattern=r"[!/]get (.*)"))
async def lebel(event):
    name = event.pattern_match.group(1)
    if not name:
      return await event.reply("Not enough arguments!")
    note = get_notes(event.chat_id, name)
    if not note is None:
      message_id = event.sender_id
      if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    chats = pnotes.find({})
    mode = False
    for c in chats:
      if event.chat_id == c["id"]:
        mode = c["mode"]
    if mode == False:
      await event.reply(note.reply, reply_to=message_id)
    else:
      text = f"Tap here to view '{name}' in your private chat."
      luv = f"{name}|{event.chat_id}"
      buttons = Button.url("Click me", "t.me/MissEvie_Robot?start=notes_{}".format(luv))

@register(pattern="^/start notes_(.*)")
async def rr(event):
 try:
  data = event.pattern_match.group(1)
  chat, name = data.split(" ", 1)
  chat = int(chat.strip())
  name = name.strip()
  if not event.is_private:
    return
  note = get_notes(chat, name)
  await event.reply(f"**{name}:**\n\n{note.reply}")
 except Exception as e:
   print(e)

async def no_arg(event):
 chats = pnotes.find({})
 mode = True
 for c in chats:
   if event.chat_id == c["id"]:
     mode = c["mode"]
 if mode == True:
   await event.reply("Your notes are currently being sent in private. Evie will send a small note with a button which redirects to a private chat.")
 elif mode == False:
   await event.reply("Your notes are currently being sent in the group.")

@register(pattern="^/save ?(.*)")
async def _(event):
    if event.is_group:
      if not await is_admin(event, event.sender_id):
        await event.reply("You need to be an admin to do this.")
        return
      if not await can_change_info(message=event):
        await event.reply("You are missing the following rights to use this command: CanChangeInfo")
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
     else:
      name = arg[0]
      if not name:
        await event.reply("You need to give the note a name!")
        return
      await event.reply("You need to give the note some content!")
      return
    if event.reply_to_msg_id:
     reply_message = await event.get_reply_message()
     msg = reply_message.text
     name = event.pattern_match.group(1)
     if not msg:
        return
     if not name:
        await event.reply("You need to give the note a name!")
        return
    note = msg
    add_note(
            event.chat_id,
            name,
            note,
        )
    await event.reply(f"Saved note `{name}`.")

@register(pattern="^/notes$")
async def on_note_list(event):
    if event.is_group:
        pass
    else:
        return
    all_notes = get_all_notes(event.chat_id)
    OUT_STR = f"List of notes in {event.chat.title}:\n"
    if len(all_notes) > 0:
        for a_note in all_notes:
            OUT_STR += f"- `{a_note.keyword}`\n"
        OUT_STR += "You can retrieve these notes\nby using `/get notename`, or \n`#notename`"
    else:
        OUT_STR = f"No notes in {event.chat.title}!"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "notes.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available notes",
                reply_to=event,
            )
    else:
        chats = pnotes.find({})
        mode = False
        for c in chats:
          if event.chat_id == c["id"]:
            mode = c["mode"]
        if mode == True:
            text = "Click below button to get notes list."
            buttons = Button.url("Click here", "t.me/MissEvie_Robot?start=listn_{}".format(event.chat_id))
            return await event.reply(text, buttons=buttons)
        await event.reply(OUT_STR)

@register(pattern="^/start listn_(.*)")
async def rr(event):
  if not event.is_private:
    return
  chat_id = int(event.pattern_match.group(1))
  all_notes = get_all_notes(chat_id)
  OUT_STR = "**Notes:**\n"
  for a_note in all_notes:
            luv = f"{a_note.keyword}|{chat_id}"
            OUT_STR += f"- [{a_note.keyword}](t.me/MissEvie_Robot?start=notes_{luv})\n"
  OUT_STR += "You can retrieve these notes by tapping on the notename."
  await event.reply(OUT_STR)

@register(pattern="^/clearall")
async def clear(event):
 if not event.is_group:
   return
 if not await is_admin(event, event.sender_id):
   await event.reply("You need to be an admin to do this.")
   return
 permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
 if not permissions.is_creator:
          return await event.reply(f"You need to be the chat owner of {event.chat.title} to do this.")
 TEXT = f"Are you sure you would like to clear **ALL** notes in {event.chat.title}? This action cannot be undone."
 await tbot.send_message(
            event.chat_id,
            TEXT,
            buttons=[
                [Button.inline("Delete all notes", data="confirm")],[Button.inline("Cancel", data="rt")],],
            reply_to=event.id
           )

@tbot.on(events.CallbackQuery(pattern=r"rt"))
async def start_again(event):
        permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not permissions.is_creator:
           return await event.answer("Yeah suck my dick")
        await event.edit("Clearing of all notes has been cancelled.")

@tbot.on(events.CallbackQuery(pattern=r"confirm"))
async def start_again(event):
        permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not permissions.is_creator:
           return await event.answer("Yeah suck my dick")
        all_notes = get_all_notes(event.chat_id)
        for i in all_notes:
           name = i.keyword
           remove_note(event.chat_id, name)
        await event.edit("Deleted all chat notes.")

@register(pattern="^/clear (.*)")
async def on_note_delete(event):
    if event.is_group:
      if not await is_admin(event, event.sender_id):
        await event.reply("You need to be an admin to do this.")
        return
      if not await can_change_info(message=event):
        await event.reply("You are missing the following rights to use this command: CanChangeInfo")
        return
    else:
        return
    name = event.pattern_match.group(1)
    remove_note(event.chat_id, name)
    await event.reply("Note **{}** deleted!".format(name))


@register(pattern="^/privatenotes ?(.*)")
async def pr(event):
 if not await is_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command!")
 if not await can_change_info(message=event):
   return await event.reply("You don't have enough rights to do this!")
 arg = event.pattern_match.group(1)
 if not arg:
    return await no_arg(event)
 arg.replace("yes", "on")
 arg.replace("no", "off")
 if not arg == "on" and not arg == "yes" and not arg == "no" and not arg == "off":
   return await event.reply("I only understand the following: yes/no/on/off")
 chats = pnotes.find({})
 if arg == "on":
   mode = True
   await event.reply("Evie will now send a message to your chat with a button redirecting to PM, where the user will receive the note.")
 elif arg == "off":
   mode = False
   await event.reply("Evie will now send notes straight to the group.")
 for c in chats:
   if event.chat_id == c["id"]:
     to_check = get_chat(id=event.chat_id)
     pnotes.update_one(
                {
                    "_id": to_check["_id"],
                    "id": to_check["id"],
                    "mode": to_check["mode"],
                },
                {"$set": {"mode": mode}},
            )
     return
 pnotes.insert_one(
        {"id": event.chat_id, "mode": mode}
    )


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
**Notes**
Save data for future users with notes!

Notes are great to save random tidbits of information; a phone number, a nice gif, a funny picture - anything!

**User commands:**
- /get `<notename>`: Get a note.
- `#notename`: Same as /get.

**Admin commands:**
- /save `<notename>` `<note text>`: Save a new note called "word". Replying to a message will save that message. Even works on media!
- /clear `<notename>`: Delete the associated note.
- /notes: List all notes in the current chat.
- /clearall: Delete **ALL** notes in a chat. This cannot be undone.
- /privatenotes: If notes need to be sent in private.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
