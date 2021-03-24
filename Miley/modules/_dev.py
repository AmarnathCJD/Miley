from pymongo import MongoClient
from Miley import MONGO_DB_URI, DEV_USERS, OWNER_ID, BOT_ID, SUDO_USERS
from Miley.events import register
from Miley import tbot

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["miley"]
blacklist = db.black

@register(pattern="^/bllist ?(.*)")
async def approve(event):
   if event.sender_id == OWNER_ID:
      pass
   elif event.sender_id in DEV_USERS:
      pass
   else:
      return
   sender = event.sender_id
   bl = blacklist.find({})
   reply_msg = await event.get_reply_message()
   iid = reply_msg.sender_id
   if iid == OWNER_ID:
     return
   elif iid in DEV_USERS:
     return
   elif iid in SUDO_USERS:
     return
   if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("I am not gonna blacklist myself")
        return
   a = blacklist.find({})
   for i in a:
         if iid == i["user"]:
                await event.reply("This User is Already Blacklisted")
                return
   blacklist.insert_one({"user": iid})
   await event.reply("Successfully Blacklisted User")


@register(pattern="^/unbllist ?(.*)")
async def approve(event):
   if event.sender_id == OWNER_ID:
      pass
   elif event.sender_id in DEV_USERS:
      pass
   else:
      return
   sender = event.sender_id
   bl = blacklist.find({})
   reply_msg = await event.get_reply_message()
   iid = reply_msg.sender_id
   a = blacklist.find({})
   for i in a:
       if iid == i["user"]:
            blacklist.delete_one({"user": iid})
            await event.reply("Successfully Unblacklisted User")
            return
   await event.reply("This User isn't Blacklisted yet")
