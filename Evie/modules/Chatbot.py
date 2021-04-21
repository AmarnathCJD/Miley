# Made by RoseLoverX
# Multi language added by @InukaASiTH

from Evie import tbot, OWNER_ID, BOT_ID
import Evie.modules.sql.ai_sql as sql
from google_trans_new import google_translator
translator = google_translator()
import requests

from telethon import events
from Evie.events import register

from Evie.function import can_change_info, is_admin

@register(pattern="^/addchat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
           if not await is_admin(event, event.sender_id):
              return await event.reply("Only admins can execute this command")
           if not await can_change_info(message=event):
              return await event.reply("You are missing CanChangeInfo right to use this command!")
    else:
        return
    chat = event.chat
    is_chat = sql.is_chat(event.chat_id)
    if not is_chat:
        ses_id = 'null'
        expires = 'null'
        sql.set_ses(event.chat_id, ses_id, expires)
        await event.reply("AI successfully enabled for this chat!")
        return
    await event.reply("AI Bot is already enabled for this chat!")

@register(pattern="^/rmchat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
           if not await is_admin(event, event.sender_id):
              return await event.reply("Only admins can execute this command")
           if not await can_change_info(message=event):
              return await event.reply("You are missing CanChangeInfo right to use this command!")
    else:
        return
    chat = event.chat
    is_chat = sql.is_chat(event.chat_id)
    if not is_chat:
        await event.reply("AI isn't enabled here in the first place!")
        return
    sql.rem_chat(event.chat_id)
    await event.reply("AI Bot disabled successfully!")

@tbot.on(events.NewMessage(pattern=None))
async def _(event):
  if event.media:
    return
  prof = str(event.text)
  if not event.is_private or not event.is_group:
    return
  if event.is_group:
   is_chat = sql.is_chat(event.chat_id)
   if not is_chat:
         return
   if event.reply_to_msg_id:
     reply_msg = await event.get_reply_message()
     if not reply_msg.sender_id == BOT_ID:
            return
   elif "Evie" in prof:
      pass
   elif "evie" in prof:
      pass
   else:
      return
  elif event.is_private:
    if event.text.startswith("!") or event.text.startswith("/"):
     return
  msg = prof.replace("Evie", "Aco")
  msg = prof.replace("evie", "Aco")
  if msg.startswith("/") or msg.startswith("@") or msg.startswith("."):
    return
  lan = translator.detect(msg)
  if not "en" in lan and not lan == "":
     test = translator.translate(msg, lang_tgt="en")
  else:
     test = msg
  url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
  test = test.replace("Evie", "Aco")
  test = test.replace("evie", "Aco")
  querystring = {
            "bid": "178",
            "key": "sX5A2PcYZbsN5EY6",
            "uid": "mashape",
            "msg": {test},
        }
  headers = {
            "x-rapidapi-key": "cf9e67ea99mshecc7e1ddb8e93d1p1b9e04jsn3f1bb9103c3f",
            "x-rapidapi-host": "acobot-brainshop-ai-v1.p.rapidapi.com",
        }
  response = requests.request("GET", url, headers=headers, params=querystring)
  result = response.text
  result = result.replace('{"cnt":"', "")
  result = result.replace('~', '')
  result = result.replace('"}', "")
  result = result.replace("Aco", "Evie")
  result = result.replace("<a href=\\", "<a href =")
  result = result.replace("<\/a>", "</a>")
  if not "en" in lan and not lan == "":
    finale = translator.translate(result, lang_tgt=lan[0])
  else:
    finale = result
  try:
    async with tbot.action(event.chat_id, 'typing'):
           await event.reply(finale)
  except:
       await event.reply(lodu)
