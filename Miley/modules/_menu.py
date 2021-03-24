from Miley import CMD_LIST, CMD_HELP, tbot
import io
import re
from math import ceil

from telethon import custom, events, Button

from Miley.events import register

from telethon import types
from telethon.tl import functions

from pymongo import MongoClient
from Miley import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["miley"]
pagenumber = db.pagenumber

caption = "Hey! I am Miley, here to help you manage your groups! I perform most of the Admin functions and make your group automated!\n\nJoin @Mileybotnews for updates.\n@Mileybotsupport for help and support\n\nYou can checkout more about me via following buttons."

@register(pattern="^/start$")
async def start(event):
 if not event.is_group:
        await tbot.send_message(
            event.chat_id,
            caption,
            buttons=[
                [
                    Button.inline("Advanced", data="advanced_menu"),
                    Button.inline("Commands", data="help_menu"),
                ],
                  [
                    Button.url(
                        "Add Me To Your Group!", "t.me/missmiley_robot?startgroup=true"
                    ),
                ],
            ],
        )
 else:
    await event.reply("Heya :) PM me if you have any questions on how to use me!")
