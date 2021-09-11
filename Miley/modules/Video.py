import yt_dlp
from .. import vc
from ..utils import Cbq, Mbot
from . import (
    active_chats,
    can_manage_call,
    get,
    is_empty,
    pause,
    put,
    resume,
    set_stream,
    stop,
    task_done,
)

@Cbq(pattern="^/play ?(.*)")
async def _play(e):
 r = await e.get_reply_message()
 if r and r.video or r.audio:
   file = await e.client.download_media(r)
 if not r:
  try:
   q = e.text.split(" ", 1)[1]
  except IndexError:
   return await e.reply("Qoery was not found.")
  if q.startswith("http"):
   url = q
  else:
   
