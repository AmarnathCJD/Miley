from Evie import tbot,MONGO_DB_URI, BOT_ID
from pymongo import MongoClient
from telethon import events, Button

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
lock = db.lockzz

def get_chat(id):
    return lock.find_one({"id": id})
   
@tbot.on(events.NewMessage(pattern=None))
async def babe(event):
 chats = lock.find({})
 for c in chats:
  if event.chat_id == c["id"]:
   if c["phone"] == True:
    if event.text.startswith("+91"):
        await event.delete()
   elif c["email"] == True:
    if "@gmail.com" in event.text or "@yahoo.com" in event.text:
        await event.delete()
   elif c["audio"] == True:
    if event.media:
     if event.media.document.mime_type == "audio/m4a":
        await event.delete()
   elif c["command"] == True:
    if event.text.startswith("/"):
        await event.delete()
   elif c["forward"] == True:
    if not event.fwd_from == None:
        await event.delete()
   elif c["video"] == True:
    if event.media:
     if event.media.document.mime_type == "video/mp4":
         await event.delete()
   elif c["location"] == True:
     if event.media:
       if not event.media.geo == None:
         await event.delete()


addon = ["command", "forward", "video", "audio", "phone", "location", "email", "comment"]
from Evie import tbot, CMD_HELP
import os
from Evie.function import is_admin
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights


@tbot.on(events.NewMessage(pattern="^[!/]lock ?(.*)"))
async def lk(event):
 input_str = event.pattern_match.group(1)
 msg = None
 media = None
 sticker = None
 gif = None
 gamee = None
 ainline = None
 gpoll = None
 adduser = None
 cpin = None
 emlink = None
 changeinfo = None
 if input_str == "message" or input_str == "msg":
    msg = True
 elif input_str == "media":
    media = True
 elif input_str == "sticker":
    sticker = True
 elif input_str == "gif" or input_str == "gifs":
    gif = True
 elif input_str == "game" or input_str == "games":
    gamee = True
 elif input_str == "inline":
    ainline = True
 elif input_str == "poll":
    gpoll = True
 elif input_str == "invite":
    adduser = True
 elif input_str == "pin":
    cpin = True   
 elif input_str == "url":
    emlink = True
 elif input_str == "info":
    changeinfo = True
 elif input_str == "all":
    msg = True
    media = True
    sticker = True
    gif = True
    gamee = True
    ainline = True
    emlink = True
    gpoll = True
    adduser = True
    cpin = True
    changeinfo = True
 elif input_str in addon:
  forward = False
  command = False
  audio = False
  video = False
  phone = False
  location = False
  email = False
  comment = False
  if input_str == "forward":
     forward = True
  elif input_str == "command":
     command = True
  elif input_str == "phone":
     phone = True
  elif input_str == "audio":
     audio = True
  elif input_str == "video":
     video = True
  elif input_str == "location":
     location = True
  elif input_str == "email":
     email = True
  elif input_str == "comment":
     comment = True
  chats = lock.find({})
  cid = None
  for c in chats:
     if event.chat_id == c["id"]:
        cid = c["id"]
  if cid:
    to_check = get_chat(id=event.chat_id)
    lock.update_one(
                {
                    "_id": to_check["_id"],
                    "id": to_check["id"],
                    "forward": to_check["forward"],
                    "command": to_check["command"],
                    "phone": to_check["phone"],
                    "video": to_check["video"],
                    "audio": to_check["audio"],
                    "location": to_check["location"],
                    "email": to_check["email"],
                    "comment": to_check["comment"],
                },
                {"$set": {"forward": forward, "command": command, "phone": phone, "video": video, "audio": audio, "location": location, "email": email, "comment": comment}},
            )
    return await event.reply(f"Locked `{input_str}`")
  lock.insert_one(
        {"id": event.chat_id, "forward": forward, "command": command, "phone": phone, "video": video, "audio": audio, "location": location, "email": email, "comment": comment}
     )
  return await event.reply(f"Locked `{input_str}`")
 elif input_str == None:
   return await event.reply("You haven't specified a type to lock.")
 else:
   return await event.reply(f"Unknown lock types:\n- {input_str}\nCheck /locktypes!")
 lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        embed_links=emlink,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
 if await is_admin(event, BOT_ID):
  await event.reply(f"Locked `{input_str}`.")
  await tbot(
            EditChatDefaultBannedRightsRequest(event.chat_id, banned_rights=lock_rights)
        )
 

#Need to add lock comments
