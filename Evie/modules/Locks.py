from Evie import tbot,MONGO_DB_URI
from pymongo import MongoClient

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
