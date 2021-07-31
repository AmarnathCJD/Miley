from ..utils import Cbq, Mbot
from .mongodb.playlist_db import get_playlist

digits = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6⃣", "7⃣", "8⃣"]
from telethon import Button


@Mbot(pattern="^/playlist")
async def playlist_show_(e):
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
    if len(x) < 9:
        playlist_q = "**{}**'s **Playlist:**".format(e.sender.first_name)
        q = 0
        for _x in x:
            play = _x
            number = digits[q]
            playlist_q += "\n{}- ".format(number, play)
            q += 1
        await e.edit(playlist_q)
    else:
        await e.respond("9")
