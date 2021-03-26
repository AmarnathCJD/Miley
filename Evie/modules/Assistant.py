from Evie import tbot, CMD_HELP
import os
import subprocess

import Evie.modules.sql.ai_sql as sql
import requests
from gtts import gTTS
from gtts import gTTSError
from requests import get
import requests
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon import events
import random
from telethon.tl.types import *

from Evie import *

from Evie.events import register

@register(pattern=r"^/evie(?: |$)([\s\S]*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        i = event.pattern_match.group(1)
        appid = WOLFRAM_ID
        server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={i}"
        res = get(server)
        if "Wolfram Alpha did not understand your input" in res.text:
            await event.reply("Sorry I can't understand")
        else:
            await event.reply(res.text, parse_mode="markdown")

    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await tbot.download_media(
            previous_message, TEMP_DOWNLOAD_DIRECTORY
        )
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.reply(
                "The required ENV variables for this module are not set. \nModule stopping"
            )
        else:
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"])
                if transcript_response != "":
                    string_to_show = "{}".format(transcript_response)
                    appid = WOLFRAM_ID
                    server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={string_to_show}"
                    res = get(server)
                    answer = res.text
                    try:
                        tts = gTTS(answer, tld="com", lang="en")
                        tts.save("results.mp3")
                    except AssertionError:
                        return
                    except ValueError:
                        return
                    except RuntimeError:
                        return
                    except gTTSError:
                        return
                    with open("results.mp3", "r"):
                        await tbot.send_file(
                            event.chat_id,
                            "results.mp3",
                            voice_note=True,
                            reply_to=event.id,
                        )
                    os.remove("results.mp3")
                    os.remove(required_file_name)
                if (
                    answer == "Wolfram Alpha did not understand your input"
                ):
                    try:
                        answer = "Sorry I can't understand"
                        tts = gTTS(answer, tld="com", lang="en")
                        tts.save("results.mp3")
                    except AssertionError:
                        return
                    except ValueError:
                        return
                    except RuntimeError:
                        return
                    except gTTSError:
                        return
                    with open("results.mp3", "r"):
                        await tbot.send_file(
                            event.chat_id,
                            "results.mp3",
                            voice_note=True,
                            reply_to=event.id,
                        )
                    os.remove("results.mp3")
                    os.remove(required_file_name)
            else:
                await event.reply("API Failure !")
                os.remove(required_file_name)


@register(pattern="^/howdoi (.*)")
async def howdoi(event):
    if event.fwd_from:
        return
    str = event.pattern_match.group(1)
    jit = subprocess.check_output(["howdoi", f"{str}"])
    pit = jit.decode()
    await event.reply(pit)

string = (
  "I belong To ROseLoverX",
  "Im Fairly Yound And Was Made by RoseLover",
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
    if message.lower() == "evie ?(.*)":
        return True
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
  if is_chat:
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

@register(pattern="^/quote")
async def qt(event):
 url = "https://andruxnet-random-famous-quotes.p.rapidapi.com/"

 querystring = {"cat":"famous","count":"1"}

 headers = {
    'x-rapidapi-key': "cf9e67ea99mshecc7e1ddb8e93d1p1b9e04jsn3f1bb9103c3f",
    'x-rapidapi-host': "andruxnet-random-famous-quotes.p.rapidapi.com"
    }

 response = requests.request("GET", url, headers=headers, params=querystring)
 k = response.text
 j = k.replace(',', '')
 q = j.replace("{", "")
 l = q.replace("}", "")
 n = l.replace('"author"', ' ')
 o = n.replace('"quote":', '')
 z = o.replace(":", "-")
 y = z.replace('."', '')
 X = y.replace('"', '')
 m = X.replace('category-Famous', '')
 Com = m.replace(']', '')
 text = Com.replace('[', '')
 try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(text)
 except CFError as e:
           await event.reply('Error Report @Eviesupport')

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
**For text assistant**
 - /evie <question>: Ask luna any question and it will give accurate reply. For eg: `/luna where is Taj Mahal`, `/luna what is the age of Virat Kohli` etc..
**For voice assistant**
 - /evie: Reply to a voice query and get the results in voice output (ENGLISH ONLY)
 
**For IamAI**
 - evie/Evie <question>: Ask evie questions, Advanced level.
 
**Terminal Assistant**
 - /howdoi <question>: Get all coding related answers from Luna. Syntax: `/howdoi print hello world in python`
 
 - /quote: Provides quotes of famous personalities

**NOTE**
The question should be a meaningful one otherwise you will get no response !
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
