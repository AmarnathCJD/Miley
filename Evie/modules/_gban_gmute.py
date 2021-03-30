from Evie import tbot, OWNER_ID, DEV_USERS, MONGO_DB_URI, BOT_ID
from pymongo import MongoClient
from Evie.function import is_admin
from Evie.modules._dev import sudo
from Evie.events import register
import asyncio

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
gbanned = db.gban

def get_reason(id):
    return gbanned.find_one({"user": id})


@register(pattern="^/gban ?(.*)")
async def gban(event):
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
   entity = await tbot.get_input_entity(iid)
   try:
     r_sender_id = entity.user_id
   except Exception:
        await event.reply("Couldn't fetch that user.")
        return
   fname = "User"
  else:
   r_sender_id = int(iid)
 else:
   reply_message = await event.get_reply_message()
   iid = reply_message.sender_id
   fname = reply_message.sender.first_name
   if input:
     reason = input
   else:
     reason = None
   r_sender_id = iid
 chats = gbanned.find({})
 if r_sender_id == OWNER_ID:
        await event.reply(f"Char Chavanni godhe pe\ngey Mere Lode Pe!.")
        return
 elif r_sender_id in DEV_USERS:
        await event.reply("This Person is a Dev, Sorry!")
        return
 elif r_sender_id == BOT_ID:
        await event.reply("Another one bits the dust! banned a betichod!")
        return
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
                "This User is already Gbanned, I'm updating it with the new Reason."
            )
            await event.client.send_message(
                chat,
                "**Global Ban Update**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**New Reason:** {}".format(
                    group, sender, event.sender_id, fname, r_sender_id, r_sender_id, reason
                ),
            )
            return

    gbanned.insert_one(
        {"bannerid": event.sender_id, "user": r_sender_id, "reason": reason}
    )
    if reason:
      await event.client.send_message(
        chat,
        "**New Global Ban**\n#GBAN\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**Reason:** {}".format(
            group, sender, event.sender_id, fname, r_sender_id, r_sender_id, reason
        ),
      )
    else:
      await event.client.send_message(
        chat,
        "**New Global Ban**\n#GBAN\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`".format(
            group, sender, event.sender_id, fname, r_sender_id, r_sender_id
        ),
      )
    k = await event.reply("Initiating Global Ban.!")
    await asyncio.sleep(6)
    await k.delete()
    await event.reply("Gban Completed")

    
