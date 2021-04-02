from Evie import tbot, OWNER_ID, DEV_USERS, MONGO_DB_URI, BOT_ID
from pymongo import MongoClient
from Evie.function import is_admin, sudo
from telethon import events
from Evie.events import register

from Evie.modules.sql.chats_sql import get_all_chat_id

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

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
gbanned = db.gban

def get_reason(id):
    return gbanned.find_one({"user": id})

GBAN_LOGS = [] #for now
chat = str(GBAN_LOGS)
GBANLOGS = -1001486931338

@register(pattern="^/gban ?(.*)")
async def gban(event):
 sender = event.sender.first_name
 group = event.chat.title
 if event.fwd_from:
        return
 if event.sender_id == OWNER_ID:
  pass
 elif event.sender_id in DEV_USERS:
  pass
 elif sudo(id):
  pass
 else:
  return
 input = event.pattern_match.group(1)
 if input:
   arg = input.split(" ", 1)
 if not event.reply_to_msg_id:
  if len(arg) == 2:
    iid = arg[0]
    reason = arg[1]
  else:
    iid = arg[0]
    reason = "None"
  if not iid.isnumeric():
   username = iid.replace("@", "")
   entity = await tbot.get_input_entity(iid)
   try:
     r_sender_id = entity.user_id
   except Exception:
        await event.reply("Couldn't fetch that user.")
        return
  else:
   r_sender_id = int(iid)
  fname = r_sender_id
 else:
   reply_message = await event.get_reply_message()
   iid = reply_message.sender_id
   username = reply_message.sender.username
   fname = reply_message.sender.first_name
   if input:
     reason = input
   else:
     reason = "None"
   r_sender_id = iid
 if r_sender_id == OWNER_ID:
        await event.reply(f"Char Chavanni godhe pe\ngey Mere Lode Pe!.")
        return
 elif r_sender_id in DEV_USERS:
        await event.reply("This Person is a Dev, Sorry!")
        return
 elif r_sender_id == BOT_ID:
        await event.reply("Another one bits the dust! banned a betichod!")
        return
 elif sudo(r_sender_id):
        await event.reply("Yeah Nibba that's a Sudo User🤨")
        return
 chats = gbanned.find({})
 for c in chats:
      if r_sender_id == c["user"]:
          to_check = get_reason(id=r_sender_id)
          gbanned.update_one(
                {
                    "_id": to_check["_id"],
                    "bannerid": to_check["bannerid"],
                    "user": to_check["user"],
                    "reason": to_check["reason"],
                },
                {"$set": {"reason": reason, "bannerid": event.sender_id}},
            )
          await event.reply(
                "This user is already gbanned, I am updating the reason of the gban with your reason."
            )
          await tbot.send_message(GBANLOGS, "#GBAN UPDATE\n**Originated From:** {}\n\n**Sudo:** [{}](tg://user?id={})\**User:** [{}](tg://user?id={})\n**ID:** `{}`\**New Reason:** {}".format(
                                   group, sender, event.sender_id, fname, r_sender_id, r_sender_id, reason)       
          return

 gbanned.insert_one(
        {"bannerid": event.sender_id, "user": r_sender_id, "reason": reason}
    )
 k = await event.reply("⚡Snaps the BanHammer⚡")
 cheater = get_all_chat_id()
 done = 0
 for i in cheater:
   try:
       chat = int(i.chat_id)
       await tbot(
                    EditBannedRequest(chat, f"{username}", BANNED_RIGHTS)
               )
       done = done + 1
   except Exception:
       pass
 await event.reply(f"GlobalBan Completed\n**Time Taken**: Soon!")

@register(pattern="^/ungban ?(.*)")
async def ugban(event):
 sender = event.sender.first_name
 group = event.chat.title
 id = event.sender_id
 if event.fwd_from:
        return
 if event.sender_id == OWNER_ID:
  pass
 elif event.sender_id in DEV_USERS:
  pass
 elif sudo(id):
  pass
 else:
  return
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
   username = iid.replace("@", "")
   entity = await tbot.get_input_entity(iid)
   try:
     r_sender_id = entity.user_id
   except Exception:
        await event.reply("Couldn't fetch that user.")
        return
   fname = r_sender_id
  else:
   r_sender_id = int(iid)
 else:
   reply_message = await event.get_reply_message()
   iid = reply_message.sender_id
   username = reply_message.sender.username
   fname = reply_message.sender.first_name
   if input:
     reason = input
   else:
     reason = None
   r_sender_id = iid
 if r_sender_id == OWNER_ID:
        await event.reply(f"Yeah FuckOff!")
        return
 elif r_sender_id in DEV_USERS:
        await event.reply("No!")
        return
 elif r_sender_id == BOT_ID:
        await event.reply("Who Dafaq Made You Sudo?!")
        return
 elif sudo(r_sender_id):
        await event.reply("Yeah Nibba that's a Sudo User🤨")
        return
 chats = gbanned.find({})
 for c in chats:
        if r_sender_id == c["user"]:
            to_check = get_reason(id=r_sender_id)
            gbanned.delete_one({"user": r_sender_id})
            await event.reply("Globally Pardoned This User.!🏳️")
            return
 await event.reply("Yeah that user is not in my Gbanned list.!?")




"""
@tbot.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
      if is_admin(event, BOT_ID):
        chats = gbanned.find({})
        for c in chats:
          if event.user_id == c["user"]:
              try:
               chat = event.chat_id
               await tbot(
                    EditBannedRequest(chat, event.user_id, BANNED_RIGHTS)
                 )
               await tbot.send_message(event.chat_id, f"Gbanned User Joined\n**ID:** `{event.user_id}`\n\n**Quick Action:** Banned")
              except Exception:
                   pass
              
"""


#ungban Soon!
#gmute_ungmute Soon!
#gban_logs Soon!
