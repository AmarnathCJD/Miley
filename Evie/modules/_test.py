from Evie.events import register
from pymongo import MongoClient
from Evie import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
sudo = db.sudo


@register(pattern="^/fucker ?(.*)")
async def surest(event):
  k = event.pattern_match.group(1)
  users = sudo.find({})
  for c in users:
        if  k == c["user"]:
                 await event.reply("Fuked")

  
