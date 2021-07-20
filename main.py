from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from pytgcalls import GroupCallFactory
from os import environ as e

API_KEY = e.get("API_KEY")
API_HASH = e.get("API_HASH")
TOKEN = e.get("TOKEN")
STRING_SESSION = e.get("STRING_SESSION")

bot = (TelegramClient (None, API_KEY, API_HASH)).start(bot_token=TOKEN)
vc = TelegramClient (StringSession(STRING_SESSION), API_KEY, API_HASH)

vc.start()

@bot.on(events.NewMessage(pattern="^/playvc ?(.*)"))
async def playvc(e):
 song = e.pattern_match.group(1)
 await e.respond("command recived test")
 
