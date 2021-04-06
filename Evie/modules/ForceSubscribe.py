#test modules

from Evie import tbot
from Evie.events import register
import Evie.modules.sql.fsub_sql as sql


@register(pattern="^/fsub")
async def fs(event):
  args = event.pattern_match.group(1)
  if args:
    k = f"{event.chat_id}"
    chat = k.replace("-", "")
    FK = sql.add_channel(event.chat_id, args)
    if FK:
      await event.reply("Set fsub")
      
