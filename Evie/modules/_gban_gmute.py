from Evie import tbot, OWNER_ID, DEV_USERS, MONGO_DB_URI, BOT_ID
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
 if not iid.isnumeric():
   entity = await tbot.get_input_entity(iid)
   try:
     r_sender_id = entity.user_id
   except Exception:
        await event.reply("Couldn't fetch that user.")
        return
 else:
   r_sender_id = iid
 chats = gbanned.find({})
 if r_sender_id == OWNER_ID:
        await event.reply(f"Char Chavanni godhe pe\n{event.sender.first_name} Mere Lode Pe!.")
        return
 elif r_sender_id in SUDO_USERS:
        await event.reply("Can't act against my sudo user!")
        return
 elif r_sender_id in DEV_USERS:
        await event.reply("This Person is a Dev, Sorry!")
        return
 elif r_sender_id == BOT_ID:
        await event.reply("Another one bits the dust! banned a betichod!")
        return

    
