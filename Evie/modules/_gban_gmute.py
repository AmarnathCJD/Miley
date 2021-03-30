from Evie import tbot, OWNER_ID, DEV_USERS, MONGO_DB_URI
from pymongo import MongoClient
from Evie.function import is_admin
from Evie.modules._dev import sudo
from Evie.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
gbanned = db.gban

def get_reason(id):
    return gbanned.find_one({"user": id})


@register(pattern="^/gban ?(.*)")
async def gban(event):
 id = event.sender_id
 if event.fwd_from:
        return
 if event.sender_id == OWNER_ID:
  pass
 elif event.sender_id in SUDO_USERS:
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
 else:
   reply_message = await event.get_reply_message()
   iid = reply_message.sender_id
   fname = reply_message.sender.first_name
   if input:
     reason = input
   else:
     reason = None
 entity = await tbot.get_input_entity(iid)
 try:
    r_sender_id = entity.user_id
 except Exception:
        await event.reply("Couldn't fetch that user.")
        return
 chats = gbanned.find({})
 await event.reply(f"{iid} {reason}")

    
