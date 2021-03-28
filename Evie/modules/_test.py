from Evie.events import register
from pymongo import MongoClient
from Evie import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
sudo = sudo.black


@register(pattern="^/fucker ?(.*)")
async def surest(event):
  k = event.pattern_match.group(1)
  jam = sudo.find({})
  for i in jam:
     if k == i["user"]:
      await event.reply("it's a fucker")
  else:
      await event.reply("Not a fucker")
  
