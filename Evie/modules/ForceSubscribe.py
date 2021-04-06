#test modules

from Evie import tbot
from Evie.events import register
import Evie.modules.sql.fsub_sql as sql


@register(pattern="^/fsub")
async def fs(event):
  args = event.pattern_match.group(1)
  if args:
    set_fsub(event.chat_id, args)
    await event.reply("Set fsub")
      
