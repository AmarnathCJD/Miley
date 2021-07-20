from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from pytgcalls import GroupCallFactory
from os import environ as e
from youtubesearchpython import SearchVideos

API_KEY = e.get("API_KEY")
API_HASH = e.get("API_HASH")
TOKEN = e.get("TOKEN")
STRING_SESSION = e.get("STRING_SESSION")

bot = (TelegramClient (None, API_KEY, API_HASH)).start(bot_token=TOKEN)
vc = TelegramClient (StringSession(STRING_SESSION), API_KEY, API_HASH)

vc.start()
dict_1 = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


@bot.on(events.NewMessage(pattern="^/playvc ?(.*)"))
async def playvc(e):
 song = e.pattern_match.group(1)
 search = SearchVideos(song, offset=1, mode="dict", max_results=5)
 final_text = ""
 q = -1
 kdawg = (search.result())["search_result"]
 for x in kdawg:
    q += 1
    final_text += f"\ndict_1[q]**{x.get('title')}**\n  ┗  🔗 __[Get Additional Information]__(t.me/missneko_bot?start=help)"
 buttons = []
 bt = []
 for x in range(0, 5):
    d = Button.inline(dict_1[x], data="play_{}".format(kdawg[x].get('id')))
    bt.append(d)
    if len(bt) == 3 or x == 4:
      buttons.append(bt)
      bt = []
 buttons.append([Button.inline("🗑️ Close Menu", data="close_menu")])
 await e.respond(final_text, buttons=buttons, file=kdawg[0].get("thumbnails")[3])

bot.run_until_disconnected()
