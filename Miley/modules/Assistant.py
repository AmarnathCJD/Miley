import requests
url = "https://iamai.p.rapidapi.com/ask"
from Miley import tbot, OWNER_ID
from Miley.events import bot
from telethon import events
from telethon import types
from telethon.tl import functions
import asyncio, os

@bot(pattern="q (.*)")
async def hmm(event):
  test = event.pattern_match.group(1)
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
   pro = "I am fairly yound and I was made by RoseloverX."
   try:
      async with tbot.action(event.chat_id, 'typing'):
           await event.reply(pro)
   except CFError as e:
           print(e)
  elif "Jessica" in result:
   pro = "My name is Luna"
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
           print(e)

@bot(pattern="^/quote")
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
           await event.reply('Error Pls Report @Mileysupport')


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
wait
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
