from Evie import tbot, OWNER_ID, DEV_USERS
from Evie.function import is_admin
from Evie.modules._dev import sudo
from Evie.events import register


@register(pattern="^/gban ?(.*)")
async def gban(event):
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

#balance Tomorrow
    
