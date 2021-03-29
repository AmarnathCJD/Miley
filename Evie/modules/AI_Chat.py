from Evie import tbot, OWNER_ID
import Evie.modules.sql.ai_sql as sql
import Evie.modules.sql.chatbot_sql as ly
import emoji
from google_trans_new import google_translator
translator = google_translator()
def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)

string = (
  "I belong To RoseLoverX!",
  "Im Fairly Yound And Was Made by RoseLover!",
)

@register(pattern="^/eaichat$")
async def _(event):
    if event.is_group:
        if event.sender_id == OWNER_ID:
            pass
        else:
            return
    else:
        return

    chat = event.chat
    send = await event.get_sender()
    user = await tbot.get_entity(send)
    is_chat = sql.is_chat(chat.id)
    k = ly.is_chat(chat.id)
    if k:
        await event.reply('Disable LydiaAI First!')
        return
    if not is_chat:
        ses_id = 'null'
        expires = 'null'
        sql.set_ses(chat.id, ses_id, expires)
        await event.reply("IamAI successfully enabled for this chat!")
        return
    await event.reply("IamAI is already enabled for this chat!")
    return ""


@register(pattern="^/daichat$")
async def _(event):
    if event.is_group:
        if not event.sender_id == OWNER_ID:
          return
    else:
        return
    chat = event.chat
    send = await event.get_sender()
    user = await tbot.get_entity(send)
    is_chat = sql.is_chat(chat.id)
    if not is_chat:
        await event.reply("IamAI isn't enabled here in the first place!")
        return ""
    sql.rem_chat(chat.id)
    await event.reply("IamAI disabled successfully!")


@tbot.on(events.NewMessage(pattern=None))
async def check_message(event):
    if event.is_group:
        pass
    else:
        return
    message = str(event.text)
    reply_msg = await event.get_reply_message()
    if reply_msg:
        if reply_msg.sender_id == BOT_ID:
            return True
    else:
        return False

@tbot.on(events.NewMessage(pattern=None))
async def _(event):
  if event.is_group:
        pass
  else:
        return
  msg = str(event.text)
  chat = event.chat
  is_chat = sql.is_chat(chat.id)
  if not is_chat:
        return
  if msg:
        if not await check_message(event):
            return
  
  url = "https://iamai.p.rapidapi.com/ask"
  test = msg
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
    try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(result)
    except CFError as e:
           await event.reply(lodu)
