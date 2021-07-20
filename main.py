from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from pytgcalls import GroupCallFactory
from os import environ as e, remove
from youtubesearchpython import SearchVideos
import youtube_dl
API_KEY = e.get("API_KEY")
API_HASH = e.get("API_HASH")
TOKEN = e.get("TOKEN")
STRING_SESSION = e.get("STRING_SESSION")

bot = (TelegramClient (None, API_KEY, API_HASH)).start(bot_token=TOKEN)
vc = TelegramClient (StringSession(STRING_SESSION), API_KEY, API_HASH)

vc.start()
dict_1 = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
    }

@bot.on(events.NewMessage(pattern="^/playvc ?(.*)"))
async def playvc(e):
 song = e.pattern_match.group(1)
 search = SearchVideos(song, offset=1, mode="dict", max_results=5)
 final_text = ""
 q = -1
 kdawg = (search.result())["search_result"]
 for x in kdawg:
    q += 1
    final_text += f"\n{dict_1[q]}<b>{x.get('title')}</b>\n  ┗  🔗 <i><a href='t.me/missneko_bot?start=help'>Get Additional Information</a></i>"
 buttons = []
 bt = []
 for x in range(0, 5):
    cb_data = kdawg[x].get('id') + "|" + str(e.sender_id)
    d = Button.inline(dict_1[x], data="play_{}".format(cb_data))
    bt.append(d)
    if len(bt) == 3 or x == 4:
      buttons.append(bt)
      bt = []
 buttons.append([Button.inline("🗑️ Close Menu", data="close_menu|" + str(e.sender_id))])
 await e.respond(final_text, buttons=buttons, file=kdawg[0].get("thumbnails")[4], parse_mode="html")

x_info = """
🎥<b>Playing:</b> <a href="https://www.youtube.com/watch?v={}">{}</a>
⏳<b>Duration:</b> {}
💡<b>Info:</b> <a href="https://t.me/missneko_bot?start=help">Get Additional Information</a>
👤<b>Requested by:</b> {}
"""

@bot.on(events.CallbackQuery(pattern=r"play(\_(.*))"))
async def play_cb_(e):
 song_id, sender_id = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|", 1)
 if not int(sender_id) == e.sender_id:
    return await e.answer("This is not for you!", alert=True)
 song_id = song_id.strip()
 song = ((SearchVideos (song_id, max_results=1, mode="dict")).result()["search_result"])[0]
 song_name = song.get("title")
 x = await e.edit(f"Downloading **{song_name}** Now!")
 with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_id])
 await x.edit(x_info.format(song_id, song_name, song.get("duration"), e.sender.first_name))



 





bot.run_until_disconnected()
