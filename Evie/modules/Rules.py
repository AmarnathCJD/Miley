from Evie import tbot, CMD_HELP, MONGO_DB_URI
from Evie.events import register
import os
from Evie.function import can_change_info, is_admin

from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
prules = db.privaterules
rrules = db.rulesbutton

from typing import Optional
import Evie.modules.sql.rules_sql as sql
from telethon import functions, types, events, Button
from telethon.tl import *

def get_chat(id):
    return prules.find_one({"id": id})

@tbot.on(events.NewMessage(pattern=r"[!/]rules"))
async def rules(event):
 if event.is_private:
   return
 rules = sql.get_rules(event.chat_id)
 if not rules:
   return await event.reply("This chat doesn't seem to have had any rules set yet... I wouldn't take that as an invitation though.")
 mode = None
 butto = "Rules"
 peek = rrules.find({})
 for c in peek:
   if event.chat_id == c["id"]:
     butto = c["mode"]
 chats = prules.find({})
 for c in chats:
   if event.chat_id == c["id"]:
     mode = c["mode"]
 if mode == "on" or mode == None:
   buttons = Button.url("{}".format(butto), "t.me/MissEvie_Robot?start=rules_{}".format(event.chat_id))
   text = "Click on the button to see the chat rules!"
   await event.reply(text, buttons=buttons)
 elif mode == "off":
   text = f"**The rules for** `{event.chat.title}` **are:**\n\n{rules}"
   await event.reply(text)

@register(pattern="^/start rules_(.*)")
async def rr(event):
 if not event.is_private:
   return
 chat_id = int(event.pattern_match.group(1))
 rules = sql.get_rules(chat_id)
 text = f"**The rules for** `{event.chat.title}` **are:**\n\n{rules}"
 await event.reply(text)

@register(pattern="^/privaterules ?(.*)")
async def pr(event):
 if not await is_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command!")
 rules = sql.get_rules(chat_id)
 if not rules:
   return await event.reply("You haven't set any rules yet; how about you do that first?")
 arg = event.pattern_match.group(1)
 if not arg:
    return await no_arg(event)
 if not arg == "on" or not arg == "yes" or not arg == "no" or not arg == "off":
   return await event.reply("I only understand the following: yes/no/on/off")
 chats = prules.find({})
 if arg == "on" or arg == "yes":
   mode = "on"
   await event.reply("Use of /rules will send the rules to the user's PM.")
 elif arg == "off" or arg == "no":
   mode = "off"
   await event.reply("All /rules commands will send the rules to Miley Test.")
 for c in chats:
   if event.chat_id == c["id"]:
     mode = c["mode"]
     to_check = get_chat(id=event.chat_id)
     prules.update_one(
                {
                    "_id": to_check["_id"],
                    "id": to_check["id"],
                    "mode": to_check["mode"],
                },
                {"$set": {"mode": mode}},
            )
     return
 prules.insert_one(
        {"id": event.chat_id, "mode": mode}
    )

async def no_arg(event):
 chats = prules.find({})
 mode = None
 for c in chats:
   if event.chat_id == c["id"]:
     mode = c["mode"]
 if mode == None or mode == "on":
   await event.reply("Use of /rules will send the rules to the user's PM.")
 elif mode == "off":
   await event.reply("All /rules commands will send the rules to Miley Test.")

@register(pattern="^/setrulesbutton ?(.*)")
async def rb(event):
 if not await is_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command!")
 rules = sql.get_rules(chat_id)
 if not rules:
   return await event.reply("You haven't set any rules yet; how about you do that first?")
 args = event.pattern_match.group(1)
 if len(args) > 20:
   return await event.reply("Only upto length of 20 Charectors Supported")
 if not args:
   return await no_ara(event)
 chats = rrules.find({})
 for c in chats:
   if event.chat_id == c["id"]:
     mode = c["mode"]
     to_check = get_chat(id=event.chat_id)
     rrules.update_one(
                   {
                    "_id": to_check["_id"],
                    "id": to_check["id"],
                    "mode": to_check["mode"],
                },
                {"$set": {"mode": args}},
            )
     return await event.reply("Updated the rules button name!")
 rrules.insert_one(
        {"id": event.chat_id, "mode": args}
    )

async def no_ara(event):
 chats = rrules.find({})
 mode = None
 for c in chats:
   if event.chat_id == c["id"]:
     mode = c["mode"]
 if mode == None:
   await event.reply("The rules button will be called:\n`Rules`\nTo change the button name, try this command again followed by the new name")
 else:
   await event.reply("The rules button will be called:\n`{mode}`\nTo change the button name, try this command again followed by the new name")

@register(pattern="^/resetrulesbutton")
async def rrb(event):
 if not await is_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command!")
 rules = sql.get_rules(chat_id)
 if not rules:
   return await event.reply("You haven't set any rules yet; how about you do that first?")
 chats = rrules.find({})
 for c in chats:
   if event.chat_id == c["id"]:
    rrules.delete_one({"id": event.chat_id})
 await event.reply("Reset the rules button name to default")

@register(pattern="^/setrules ?(.*)")
async def pp(event):
 if not event.is_group:
   return
 if event.is_group:
   if not await is_admin(event, event.sender_id):
     return await event.reply("You need to be an admin to do this!")
   if not await can_change_info(message=event):
     return await event.reply("You are missing CanChangeInfo right to do this!")
 input = event.pattern_match.group(1)
 if not event.reply_to_msg_id:
   if not input:
     return await event.reply("You need to give me rules to set!")
 if not event.reply_to_msg_id:
  rules = input
 else:
  rules = (await event.get_reply_message()).message
 chat_id = event.chat_id
 sql.set_rules(chat_id, rules)
 await event.reply(f"New rules for {event.chat.title} set successfully!")

@register(pattern="^/resetrules")
async def ll(event):
 if not event.is_group:
   return
 if event.is_group:
   if not await is_admin(event, event.sender_id):
     return await event.reply("You need to be an admin to do this!")
   if not await can_change_info(message=event):
     return await event.reply("You are missing CanChangeInfo right to do this!")
 chat_id = event.chat_id
 sql.set_rules(chat_id, "")
 await event.reply(f"Rules for {event.chat.tite} were successfully cleared!")

 
__help__ = """
Every chat works with different rules; this module will help make those rules clearer!

**User commands:**
- /rules: Check the current chat rules.

**Admin commands:**
- /setrules <text>: Set the rules for this chat. Supports markdown, buttons, fillings, etc.
- /privaterules <yes/no/on/off>: Enable/disable whether the rules should be sent in private.
- /resetrules: Reset the chat rules to default.
- /setrulesbutton: Set the rules button name when using {rules}.
- /resetrulesbutton: Reset the rules button name from {rules} to default.
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
