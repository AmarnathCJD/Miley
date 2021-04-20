from Evie import tbot,MONGO_DB_URI
from pymongo import MongoClient
from telethon import events, Button

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
lock = db.locks

@tbot.on(events.NewMessage(pattern=None))
async def babe(event):
 chats = lock.find({})
 for c in chats:
  if event.chat_id == c["id"]:
   if not event.via_bot_id == None:
      if c["inline"] == True:
        await event.delete()

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
 if input_str == "msg":
    msg = True
 elif input_str == "media":
    media = True
 elif input_str == "sticker":
    sticker = True
 elif input_str == "gif":
    gif = True
 elif input_str == "game":
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
 

