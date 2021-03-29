from Evie import tbot, OWNER_ID, BOT_ID
import Evie.modules.sql.ai_sql as sql
import Evie.modules.sql.chatbot_sql as ly
from google_trans_new import google_translator
translator = google_translator()
import requests


from telethon import events
from Evie.events import register

string = (
  "I belong To RoseLoverX!",
  "Im Fairly Yound And Was Made by RoseLover!",
)
from Evie.function import can_change_info


@register(pattern="^/eaichat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
           if not await can_change_info(message=event):
              return
    else:
        return
    chat = event.chat
    is_chat = sql.is_chat(chat.id)
    k = ly.is_chat(chat.id)
    if k:
        ly.rem_chat(chat.id)
    if not is_chat:
        ses_id = 'null'
        expires = 'null'
        sql.set_ses(chat.id, ses_id, expires)
        await event.reply("AI successfully enabled for this chat!")
        return
    await event.reply("AI Bot is already enabled for this chat!")
    return ""


@register(pattern="^/daichat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
          return
    else:
        return
    chat = event.chat
    is_chat = sql.is_chat(chat.id)
    if not is_chat:
        await event.reply("AI isn't enabled here in the first place!")
        return
    sql.rem_chat(chat.id)
    await event.reply("AI Bot disabled successfully!")


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
  if event.is_group:
        pass
  else:
        return
  
  reply_msg = await event.get_reply_message()
  if not reply_msg.sender_id == BOT_ID:
           return
               
  prof = str(event.text)
  chat = event.chat
  is_chat = sql.is_chat(chat.id)
  if not is_chat:
        return
  msg = prof
  if msg.startswith("/") or msg.startswith("@"):
    return
  lan = translator.detect(msg)
  if not "en" in lan and not lan == "":
     test = translator.translate(msg, lang_tgt="en")
  else:
     test = msg
  
  url = "https://iamai.p.rapidapi.com/ask"
  r = ('\n    \"consent\": true,\n    \"ip\": \"::1\",\n    \"question\": \"{}\"\n').format(test)
  k = f"({r})"
  new_string = k.replace("(", "{")
  lol = new_string.replace(")","}")
  payload = lol
  headers = {
    'content-type': "application/json",
    'x-forwarded-for': "<user's ip>",
    'x-rapidapi-key': "33b8b1a671msh1c579ad878d8881p173811jsn6e5d3337e4fc",
    'x-rapidapi-host': "iamai.p.rapidapi.com"
    }

  response = requests.request("POST", url, data=payload, headers=headers)
  lodu = response.json()
  result = (lodu['message']['text'])
  if "Thergiakis" in result:
   pro = random.choice(string)
   try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(pro)
   except CFError as e:
           print(e)
  elif "Jessica" in result:
   pro = "Yeah, My name is Evie"
   try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(pro)
   except CFError as e:
           print(e)
  else:
    if not "en" in lan and not lan == "":
      finale = translator.translate(result, lang_tgt=lan[0])
    else:
      finale = result
    try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(finale)
    except CFError as e:
           await event.reply(lodu)
