from Evie import tbot
from telethon import events


regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"

@tbot.on(events.NewMessage(pattern=None))
async def kk(event):
 if event.text in regex_upvote:
   await event.reply(regex_upvote)
