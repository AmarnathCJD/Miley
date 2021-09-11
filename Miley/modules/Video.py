import yt_dlp
from .. import vc
from ..utils import Cbq, Mbot
from youtubesearchpython import VideosSearch as vs

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

@Cbq(pattern="^/play (audio|video)?(.*)")
async def _play(e):
 r = await e.get_reply_message()
 if r and r.video or r.audio:
   file = await e.client.download_media(r)
 if not r:
  try:
   q = e.text.split(" ", 1)[1]
  except IndexError:
   return await e.reply("Qoery was not found.")
  q = q.replace(("audio", "video"), "")
  if q.startswith("http"):
   url = q
  else:
   try:
        v = vs(q, limit=1).result()["result"][0]
   except (IndexError, KeyError, TypeError):
        return await e.reply("No song/video result found for your query!")
  print("soon")
