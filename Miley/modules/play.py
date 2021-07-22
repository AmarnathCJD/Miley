from telethon import Button
from youtubesearchpython import SearchVideos
from . import transcode, active_chats, put, set_stream
from ..utils import Mbot, Cbq
from .. import que
import youtube_dl

digits = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(id)s.mp3",
    "quiet": True,
}


@Mbot(pattern="^/play ?(.*)")
async def play_new(e):
    e.chat_id
    x_start = await e.respond("🔄 <b>Processing</b>", parse_mode="html")
    if e.pattern_match.group(1):
        song = e.text.split(None, 1)[1]
    else:
        return await x_start.edit("Please provide the name of the song to search.")
    search = SearchVideos(song, offset=1, mode="dict", max_results=5)
    search = search.result()["search_result"]
    q_no = -1
    text = ""
    buttons = []
    btn = []
    for _x in search:
        q_no += 1
        digit = digits[q_no]
        text += f"\n{digit}<b>{_x.get('title')}</b>\n  ┗  🔗 <i><a href='t.me/missneko_bot?start=help'>Get Additional Information</a></i>"
        cb_data = _x.get("id") + "|" + str(e.sender.id)
        btn.append(Button.inline(digit, data="playsong_{}".format(cb_data)))
        if len(btn) == 3 or q_no == 4:
            buttons.append(btn)
            btn = []
    buttons.append([Button.inline("🗑️ Close Menu", data="close_menu")])
    await x_start.delete()
    await e.respond(
        text,
        buttons=buttons,
        file=search[0].get("thumbnails")[4],
        parse_mode="html",
        link_preview=False,
    )

play_layout = """
🎥<b>Playing:</b> <a href="https://www.youtube.com/watch?v={}">{}</a>
⏳<b>Duration:</b> {}
💡<b>Info:</b> <a href="https://t.me/missneko_bot?start=help">Get Additional Information</a>
👤<b>Requested by:</b> {}
"""

@Cbq(pattern="playsong(\_(.*))")
async def play_song(e):
 song_id, sender_id = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split(
        "|", 1
    )
 if not int(sender_id) == e.sender_id:
   return await e.answer("Lmao", alert=True)
 song_id = song_id.strip()
 x = await e.edit(f"Downloading **{song_name}** Now!")
 with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_id])
 file_path = transcode(f'{song_id}.mp3')
 chat_id = e.chat_id
 song = (
        (SearchVideos(song_id, max_results=1, mode="dict")).result()["search_result"]
    )[0]
 if chat_id in active_chats:
   position = await put(chat_id, file=file_path)
   title = song.get("title")
   (que.get(chat_id)).append([title, e.sender_id, file_path])
   text = f"#⃣ Your requested song <b>queued</b> at position {position}!"
   await x.edit(text, parse_mode="html", buttons=None)
 else:
   que[chat_id] = []
   (que.get(chat_id)).append([title, e.sender_id, file_path])
   try:
    await set_stream(chat_id, file_path)
   except Exception as r:
    return await x.edit(f"Failed to join vc, Error: {r}"
   await x.edit(
        play_layout.format(song_id, song_name, song.get("duration"), e.sender.first_name),
        parse_mode="html",
        buttons=[
        [
            Button.inline("⏸️", data="pause"),
            Button.inline("⏭️", data="next"),
            Button.inline("⏹️", data="stop"),
        ],
        [Button.inline("➕ Group Playlist", data="group_playlist")],
        [Button.inline("➕ Personal Playlist", data="my_playlist")],
        [Button.inline("🗑️ Close Menu", data="close_menu")],
    ],
    )
   
   
 
