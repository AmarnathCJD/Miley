from Evie import tbot, CMD_HELP, MONGO_DB_URI
import os, asyncio
from telethon import Button, events
from random import shuffle
from pyrogram import emoji
from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
captcha = db.captcha
"""
async def kick_restricted_after_delay(delay, event, user_id):
    
    await asyncio.sleep(delay)
    join_message = event.get_reply_message()
    group_chat = event.chat_id
    user_id = user_id
    await join_message.delete()
    await event.delete()
    await _ban_restricted_user_until_date(group_chat, user_id, duration=delay).
"""

keyboard = [
            Button.inline(
                f"{emoji.BRAIN}",
                data="fk"
            ),
            Button.inline(
                f"{emoji.CHECK_MARK_BUTTON}",
                data='pro'
            ),
            Button.inline(
                f"{emoji.CROSS_MARK}",
                data="fk-{a_user.id}"
            ),
            Button.inline(
                f"{emoji.ROBOT}",
                data='yu'
            )
        ]

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
  if not event.user_joined:
          return
  chats = captcha.find({})
  for c in chats:
       if not event.chat_id == c["id"]:
          return
       if event.chat_id == c["id"]:
          type = c["type"]
  if not type == "button":
     return
  a_user = await event.get_user()
  mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
  text = (f"Welcome, {mention}\nAre you human?\n\nClick on the button which include this emoji {emoji.CHECK_MARK_BUTTON}.")
  keyboard = [
            Button.inline(
                f"{emoji.BRAIN}",
                data="fk"
            ),
            Button.inline(
                f"{emoji.CHECK_MARK_BUTTON}",
                data='pro'
            ),
            Button.inline(
                f"{emoji.CROSS_MARK}",
                data=f"fk-{a_user.id}"
            ),
            Button.inline(
                f"{emoji.ROBOT}",
                data='yu'
            )
        ]
  shuffle(keyboard)
  button_message = await event.reply(
            text,
            buttons=keyboard
        )
  


@tbot.on(events.CallbackQuery(pattern=r"fk-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("Ee Wrong Try Again!")
    shuffle(keyboard)
    await event.edit(buttons=keyboard)
    
  
  
  
    
          
  
  
  
