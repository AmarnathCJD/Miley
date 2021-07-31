from ..utils import Mbot, Cbq
from .mongodb.playlist_db import get_playlist

digits = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

@Mbot(pattern="^/playlist")
async def playlist_show_(e):
    e.sender_id
    captions = """
<b><i>Neko's Playlist Feature</i></b>

Select The Playlist, You want to check!
"""
    buttons = [
        [
            Button.inline("Personal Playlist", data="p_play"),
            Button.inline("Group's Playlist", data="g_play"),
        ],
        [Button.inline("🗑️ Close Menu", data="close_menu")],
    ]
    await e.reply(captions, buttons=buttons, parse_mode="html")

@Cbq(pattern="p_play")
async def personnel_playlist_(e):
 x = get_playlist(e.sender_id)
 if not x:
   return await e.answer("You don't have a playlist to show!")
 if len(x) <= 5
  playlist_q = "{}'s **Playlist:**".format (e.sender.first_name)
  q = 0
  for _x in x:
   play = _x
   number = digits[q]
   playlist_q += f"\n{}- **{}**".format(number, play)
   q += 1
  await e.edit(playlist_q)
 else:
   await e.respond("5")
  
