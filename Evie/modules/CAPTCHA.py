from Evie import tbot, CMD_HELP, MONGO_DB_URI, BOT_ID
import os, asyncio, re
from telethon import Button, events
from Evie.function import gen_captcha, is_admin, can_change_info
from Evie.events import register
from captcha.image import ImageCaptcha
image_captcha = ImageCaptcha(width = 400, height = 270)
from random import shuffle
import random
from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
captcha = db.captl
welcome = db.wlc
cbutton = db.cbutton

from Evie.modules.sql.welcome_sql import get_current_welcome_settings

robot = "🤖"
tick = "✅"
wrong = ["❌", "⛔"]
brain = ["🧠", "🍋"]

maths = 2
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

def get_chat(id):
    return captcha.find_one({"id": id})

async def kick_restricted_after_delay(delay, event, user_id):
    await asyncio.sleep(delay)
    k = await tbot.get_permissions(event.chat_id, user_id)
    if not k.is_banned:
      return
    await event.delete()
    await tbot.kick_participant(event.chat_id, user_id)

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
  if not event.user_joined:
          return
  user_id = event.user_id
  chats = captcha.find({})
  type = mode = None
  time = 0
  for c in chats:
       if event.chat_id == c["id"]:
          type = c["type"]
          time = c["time"]
          mode = c["mode"]
  if mode == None or mode == "off":
      return
  if not type == None:
   if type == "multibutton":
      return await multibutton(event, time)
   elif type == "math":
      return await math(event, time)
   elif type == "button":
      return await button(event, time)
   elif type == "text":
      return await text(event, time)
  else:
    return

"""Multi button captcha"""
async def multibutton(event, time):
  user_id = event.user_id
  a_user = await event.get_user()
  mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
  cws = get_current_welcome_settings(event.chat_id)
  if cws:
     wlc = cws.custom_welcome_message
     if "|" in wlc:
       wc, options = wlc.split("|")
       wc = wc.strip()
     else:
       wc = wlc
     a_user = await event.get_user()
     title = event.chat.title
     mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
     first = a_user.first_name
     last = a_user.last_name
     if last:
         fullname = f"{first} {last}"
     else:
         fullname = first
     userid = a_user.id
     current_saved_welcome_message = wc
     text = current_saved_welcome_message.format(
                                mention=mention,
                                title=title,
                                first=first,
                                last=last,
                                fullname=fullname,
                                userid=userid,
                            )
     text += "\n\n**Captcha Verification**"
  else:
   text = f"Hey {event.user.first_name} Welcome to {event.chat.title}!"
  text += f"\n\nClick on the button which include this emoji {tick}."
  keyboard = [
            Button.inline(
                f"{random.choice(brain)}",
                data=f'pep-{a_user.id}'
            ),
            Button.inline(
                f"{tick}",
                data=f'pro-{a_user.id}'
            ),
            Button.inline(
                f"{random.choice(wrong)}",
                data=f"fk-{a_user.id}"
            ),
            Button.inline(
                f"{robot}",
                data=f'yu-{a_user.id}'
            )
        ]
  shuffle(keyboard)
  button_message = await event.reply(
            text,
            buttons=keyboard
        )
  WELCOME_DELAY_KICK_SEC = time
  try:
    await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
  except:
    pass
  if time:
   if not time == 0:
    asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
    await asyncio.sleep(0.5)

@tbot.on(events.CallbackQuery(pattern=r"fk-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("❌ Wrong Try Again!")
    keyboard = [
            Button.inline(
                f"{random.choice(brain)}",
                data=f'pep-{user_id}'
            ),
            Button.inline(
                f"{tick}",
                data=f'pro-{auser_id}'
            ),
            Button.inline(
                f"{random.choice(wrong)}",
                data=f"fk-{user_id}"
            ),
            Button.inline(
                f"{robot}",
                data=f'yu-{user_id}'
            )
        ]
    shuffle(keyboard)
    await event.edit(buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"pep-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("❌ Wrong Try Again!")
    keyboard = [
            Button.inline(
                f"{random.choice(brain)}",
                data=f'pep-{user_id}'
            ),
            Button.inline(
                f"{tick}",
                data=f'pro-{user_id}'
            ),
            Button.inline(
                f"{random.choice(wrong)}",
                data=f"fk-{user_id}"
            ),
            Button.inline(
                f"{robot}",
                data=f'yu-{user_id}'
            )
        ]
    shuffle(keyboard)
    await event.edit(buttons=keyboard)
    
@tbot.on(events.CallbackQuery(pattern=r"yu-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("❌ Wrong Try Again!")
    keyboard = [
            Button.inline(
                f"{random.choice(brain)}",
                data=f'pep-{user_id}'
            ),
            Button.inline(
                f"{tick}",
                data=f'pro-{user_id}'
            ),
            Button.inline(
                f"{random.choice(wrong)}",
                data=f"fk-{user_id}"
            ),
            Button.inline(
                f"{robot}",
                data=f'yu-{user_id}'
            )
        ]
    shuffle(keyboard)
    await event.edit(buttons=keyboard)
  
@tbot.on(events.CallbackQuery(pattern=r"pro-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("Verified Successfully ✅")
    await tbot(EditBannedRequest(event.chat_id, user_id, UNMUTE_RIGHTS))
    await event.edit(buttons=None)

"""Math captcha"""
async def math(event, time):
 try:
  user_id = event.user_id
  mode = "Click here to prove you're human"
  chats = cbutton.find({})
  for c in chats:
    if event.chat_id == c["id"]:
       mode = c["mode"]
  try:
    await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
  except:
    pass
  cws = get_current_welcome_settings(event.chat_id)
  if cws:
     wlc = cws.custom_welcome_message
     if "|" in wlc:
       wc, options = wlc.split("|")
       wc = wc.strip()
     else:
       wc = wlc
     a_user = await event.get_user()
     title = event.chat.title
     mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
     first = a_user.first_name
     last = a_user.last_name
     if last:
         fullname = f"{first} {last}"
     else:
         fullname = first
     userid = a_user.id
     text = wc.format(
                                mention=mention,
                                title=title,
                                first=first,
                                last=last,
                                fullname=fullname,
                                userid=userid,
                            )
     text += "\n\n**Captcha Verification:**"
  else:
   text = f"Hey {event.user.first_name} Welcome to {event.chat.title}!"
  buttons = Button.url(mode, "t.me/MissEvie_Robot?start=math_{}".format(event.chat_id))
  await event.reply(text, buttons=buttons)
  WELCOME_DELAY_KICK_SEC = time
  if time:
   if not time == 0:
    asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
    await asyncio.sleep(0.5)
 except Exception as e:
   await event.reply(f"{e}")

@register(pattern="^/start math_(.*)")
async def h(event):
  if not event.is_private:
   return
  chat = int(event.pattern_match.group(1))
  x = random.randint(1,150)
  y = random.randint(1,150)
  a = x + y
  d = random.randint(10, 100)
  b = random.randint(90, 100)
  c = random.randint(50, 100)
  e = random.randint(70, 100)
  f = random.randint(10, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe_{}'.format(chat)
            ),
            Button.inline(
                f"{c}",
                data='nide_{}'.format(chat)
            ),],
            [Button.inline(
                f"{d}",
                data='nipa_{}'.format(chat)
            ),
            Button.inline(
                f"{e}",
                data='suze_{}'.format(chat)
            ),
            Button.inline(
                f"{f}",
                data='papu_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.5)
  await tbot.send_message(event.chat_id, f"\n**Human Verification:**\n\nWhat is the sum of **{x} + {y}?**\n\nChoose the correct option from Below to get verified.💸", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"sikle(\_(.*))"))
async def bak(event):
 tata = event.pattern_match.group(1)
 data = tata.decode()
 chat_id = int(data.split("_", 1)[1])
 user_id = event.sender_id
 await event.edit("Successfully Verified✅, now you can message in the chat!", buttons=None)
 try:
   await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
 except:
   pass
 global maths
 maths = 3

@tbot.on(events.CallbackQuery(pattern=r"babe(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global maths
  maths -= 1
  if maths == 0:
     maths += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  await event.answer("Wrong try again!")
  x = random.randint(1,150)
  y = random.randint(1,150)
  a = x + y
  d = random.randint(10, 100)
  b = random.randint(90, 100)
  c = random.randint(50, 100)
  e = random.randint(70, 200)
  f = random.randint(10, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe_{}'.format(chat)
            ),
            Button.inline(
                f"{c}",
                data='nide_{}'.format(chat)
            ),],
            [Button.inline(
                f"{d}",
                data='nipa_{}'.format(chat)
            ),
            Button.inline(
                f"{e}",
                data='suze_{}'.format(chat)
            ),
            Button.inline(
                f"{f}",
                data='papu_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.5)
  await event.edit(f"\n**Human Verification:**\n\nWhat is the sum of **{x} + {y}?**\n\nChoose the correct option from Below to get verified.💸\n**{maths}** Chances Left!", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"suze(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global maths
  maths -= 1
  if maths == 0:
     maths += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  await event.answer("Wrong try again!")
  x = random.randint(1,150)
  y = random.randint(1,150)
  a = x + y
  d = random.randint(10, 100)
  b = random.randint(50, 100)
  c = random.randint(70, 200)
  e = random.randint(90, 100)
  f = random.randint(10, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe_{}'.format(chat)
            ),
            Button.inline(
                f"{c}",
                data='nide_{}'.format(chat)
            ),],
            [Button.inline(
                f"{d}",
                data='nipa_{}'.format(chat)
            ),
            Button.inline(
                f"{e}",
                data='suze_{}'.format(chat)
            ),
            Button.inline(
                f"{f}",
                data='papu_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  await event.edit(f"\n**Human Verification:**\n\nWhat is the sum of **{x} + {y}?**\n\nChoose the correct option from Below to get verified.💸\n**{maths}** Chances Left!", buttons=keyboard)


@tbot.on(events.CallbackQuery(pattern=r"nide(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global maths
  maths -= 1
  if maths == 0:
     maths += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  await event.answer("Wrong try again!")
  x = random.randint(1,150)
  y = random.randint(1,150)
  a = x + y
  d = random.randint(10, 100)
  b = random.randint(90, 100)
  c = random.randint(50, 200)
  e = random.randint(70, 100)
  f = random.randint(10, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe_{}'.format(chat)
            ),
            Button.inline(
                f"{c}",
                data='nide_{}'.format(chat)
            ),],
            [Button.inline(
                f"{d}",
                data='nipa_{}'.format(chat)
            ),
            Button.inline(
                f"{e}",
                data='suze_{}'.format(chat)
            ),
            Button.inline(
                f"{f}",
                data='papu_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  await event.edit(f"\n**Human Verification:**\n\nWhat is the sum of **{x} + {y}?**\n\nChoose the correct option from Below to get verified.💸\n**{maths}** Chances Left!", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"papu(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global maths
  maths -= 1
  if maths == 0:
     maths += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  await event.answer("Wrong try again!")
  x = random.randint(1,150)
  y = random.randint(1,150)
  a = x + y
  d = random.randint(10, 100)
  b = random.randint(90, 100)
  c = random.randint(70, 200)
  e = random.randint(50, 100)
  f = random.randint(10, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe_{}'.format(chat)
            ),
            Button.inline(
                f"{c}",
                data='nide_{}'.format(chat)
            ),],
            [Button.inline(
                f"{d}",
                data='nipa_{}'.format(chat)
            ),
            Button.inline(
                f"{e}",
                data='suze_{}'.format(chat)
            ),
            Button.inline(
                f"{f}",
                data='papu_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  await event.edit(f"\n**Human Verification:**\n\nWhat is the sum of **{x} + {y}?**\n\nChoose the correct option from Below to get verified.💸\n**{maths}** Chances Left!", buttons=keyboard)


@tbot.on(events.CallbackQuery(pattern=r"nipa(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global maths
  maths -= 1
  if maths == 0:
     maths += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  await event.answer("Wrong try again!")
  x = random.randint(1,150)
  y = random.randint(1,150)
  a = x + y
  d = random.randint(10, 100)
  b = random.randint(90, 100)
  c = random.randint(70, 200)
  e = random.randint(50, 100)
  f = random.randint(10, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe_{}'.format(chat)
            ),
            Button.inline(
                f"{c}",
                data='nide_{}'.format(chat)
            ),],
            [Button.inline(
                f"{d}",
                data='nipa_{}'.format(chat)
            ),
            Button.inline(
                f"{e}",
                data='suze_{}'.format(chat)
            ),
            Button.inline(
                f"{f}",
                data='papu_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  await event.edit(f"\n**Human Verification:**\n\nWhat is the sum of **{x} + {y}?**\n\nChoose the correct option from Below to get verified.💸\n**{maths}** Chances Left!", buttons=keyboard)

"""Text Captcha"""
async def text(event, time):
  user_id = event.user_id
  mode = "Click here to prove you're human"
  chats = cbutton.find({})
  for c in chats:
    if event.chat_id == c["id"]:
       mode = c["mode"]
  try:
    await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
  except:
    pass
  cws = get_current_welcome_settings(event.chat_id)
  if cws:
     a_user = await event.get_user()
     title = event.chat.title
     mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
     first = a_user.first_name
     last = a_user.last_name
     if last:
         fullname = f"{first} {last}"
     else:
         fullname = first
     userid = a_user.id
     current_saved_welcome_message = cws.custom_welcome_message
     text = current_saved_welcome_message.format(
                                mention=mention,
                                title=title,
                                first=first,
                                last=last,
                                fullname=fullname,
                                userid=userid,
                            )
     text += "\n\n**Captcha Verification**"
  else:
   text = f"Hey {event.user.first_name} Welcome to {event.chat.title}!"
  buttons = Button.url(mode, "t.me/MissEvie_Robot?start=captcha_{}".format(event.chat_id))
  await event.reply(text, buttons=buttons)
  WELCOME_DELAY_KICK_SEC = time
  if time:
   if not time == 0:
    asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
    await asyncio.sleep(0.5)

chance = 3
 
@register(pattern="^/start captcha_(.*)")
async def h(event):
  if not event.is_private:
   return
  chat = int(event.pattern_match.group(1))
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='exec_{}'.format(chat)
            ),],
            [Button.inline(
                f"{c}",
                data='sli_{}'.format(chat)
            ),
            Button.inline(
                f"{d}",
                data='paku_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.1)
  await tbot.send_message(event.chat_id, "Please choose the text from image", file='./captcha.png', buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"pip(\_(.*))"))
async def bak(event):
 tata = event.pattern_match.group(1)
 data = tata.decode()
 chat_id = int(data.split("_", 1)[1])
 user_id = event.sender_id
 await event.edit("Successfully Verified✅, now you can message in the chat!", buttons=None)
 try:
   await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
 except:
   pass
 global chance
 chance = 3

@tbot.on(events.CallbackQuery(pattern=r"exec(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global chance
  chance -= 1
  await event.answer("Wrong try again!")
  if chance == 0:
     chance += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='exec_{}'.format(chat)
            ),],
            [Button.inline(
                f"{c}",
                data='sli_{}'.format(chat)
            ),
            Button.inline(
                f"{d}",
                data='paku_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  text = f"Try again you have {chance} chances left"
  await event.edit(text, file="./captcha.png", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"sli(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global chance
  chance -= 1
  await event.answer("Wrong try again❌")
  if chance == 0:
     chance += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='exec_{}'.format(chat)
            ),],
            [Button.inline(
                f"{c}",
                data='sli_{}'.format(chat)
            ),
            Button.inline(
                f"{d}",
                data='paku_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  text = f"Try again you have {chance} chances left"
  await event.edit(text, file="./captcha.png", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"paku(\_(.*))"))
async def bak(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat = int(data.split("_", 1)[1])
  global chance
  chance -= 1
  await event.answer("Wrong try again❌")
  if chance == 0:
     chance += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='exec_{}'.format(chat)
            ),],
            [Button.inline(
                f"{c}",
                data='sli_{}'.format(chat)
            ),
            Button.inline(
                f"{d}",
                data='paku_{}'.format(chat)
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.2)
  text = f"Try again you have {chance} chances left"
  await event.edit(text, file="./captcha.png", buttons=keyboard)

"""Button Captcha"""
async def button(event, time):
  mode = "Click here to prove you're human"
  chats = cbutton.find({})
  for c in chats:
    if event.chat_id == c["id"]:
       mode = c["mode"]
  user_id = event.user_id
  buttons= Button.inline(mode, data=f"check-bot-{user_id}")
  cws = get_current_welcome_settings(event.chat_id)
  if cws:
     a_user = await event.get_user()
     title = event.chat.title
     mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
     first = a_user.first_name
     last = a_user.last_name
     if last:
         fullname = f"{first} {last}"
     else:
         fullname = first
     userid = a_user.id
     current_saved_welcome_message = cws.custom_welcome_message
     text = current_saved_welcome_message.format(
                                mention=mention,
                                title=title,
                                first=first,
                                last=last,
                                fullname=fullname,
                                userid=userid,
                            )
     text += "\n\n**Captcha Verification**:"
  else:
   text = f"Hey {event.user.first_name} Welcome to {event.chat.title}!"
  button_message = await event.reply(
            text,
            buttons=buttons
        )
  try:
    await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
  except:
    pass
  WELCOME_DELAY_KICK_SEC = time
  if time:
   if not time == 0:
    asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
    await asyncio.sleep(0.5)

@tbot.on(events.CallbackQuery(pattern=r"check-bot-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    if event.sender_id == user_id:
      try:
            await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
      except:
         pass
      await event.answer("Yep you are verified as a human being")
      await event.edit(buttons=None)


"""Commands Section"""

positive = ["on", "enable", "yes"]
negative = ["off", "disable", "no"]
mode = None
time = 0
type = "button"

@tbot.on(events.NewMessage(pattern="^[!/]captcha ?(.*)"))
async def c(event):
 input = event.pattern_match.group(1)
 chats = captcha.find({})
  for c in chats:
    if event.chat_id == c["id"]:
      mode = c["mode"]
      type = c["type"]
      time = c["time"]
 if not input:
  if mode == None or mode == "off":
   await event.reply("Welcome captcha is currently disabled for this chat.")
  elif mode == "on":
   await event.reply("Welcome CAPTCHAs are currently enabled")
 elif input in positive:
   await event.reply("Enabled welcome CAPTCHAs!")
   for c in chats:
    if event.chat_id == c["id"]:
     return captcha.update_one({"id": event.chat_id}, {"$set": {"mode": "on"}},)
   captcha.insert_one({"id": event.chat_id, "mode": "on", "type": type, "time": time})




@tbot.on(events.NewMessage(pattern="^[!/]setcaptchatext ?(.*)"))
async def ba(event):
 if event.is_private:
  return await event.reply("This command is specific to groups")
 if not await is_admin(event, event.sender_id):
   return await event.reply("You need to be an admin to do this!")
 if not await is_admin(event, BOT_ID):
   return await event.reply("I need to be admin with the right to restrict to enable CAPTCHAs.")
 arg = event.pattern_match.group(1)
 if not arg:
    mode = "Click here to prove you're human"
    chats = cbutton.find({})
    for c in chats:
      if event.chat_id == c["id"]:
        mode = c["mode"]
    text = f"Users will be welcomed with a button containing the following:\n`{mode}`\nTo change the text, try this command again followed by your new text"
    return await event.reply(text)
 if len(arg) > 20:
    return await event.reply("Only upto length of 20 Charectors Supported")
 chats = cbutton.find({})
 for c in chats:
   if event.chat_id == c["id"]:
     cbutton.delete_one({"id": event.chat_id})
 cbutton.insert_one(
        {"id": event.chat_id, "mode": arg}
    )
 await event.reply("Updated the captcha button text!")

@register(pattern="^/resetcaptchatext")
async def rrb(event):
 if event.is_private:
  await event.reply("This command is specific to groups")
 if not await is_admin(event, event.sender_id):
   return await event.reply("Only admins can execute this command!")
 if not await is_admin(event, BOT_ID):
   return await event.reply("I need to be admin with the right to restrict to enable CAPTCHAs.")
 chats = cbutton.find({})
 for c in chats:
   if event.chat_id == c["id"]:
    cbutton.delete_one({"id": event.chat_id})
 await event.reply("Reset the captcha button name to default")




file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
Some chats get a lot of users joining just to spam. This could be because they're trolls, or part of a spam network.
To slow them down, you could try enabling CAPTCHAs. New users joining your chat will be required to complete a test to confirm that they're real people.'

**Admin commands:**
- /captcha <yes/no/on/off>: All users that join will need to solve a CAPTCHA. This proves they aren't a bot!
- /captchamode <button/multibutton/math/text>: Choose which CAPTCHA type to use for your chat.
- /captcharules <yes/no/on/off>: Require new users accept the rules before being able to speak in the chat.
- /captchatime <Xw/d/h/m>: Unmute new users after X time. If a user hasn't solved the CAPTCHA yet, they get automatically unmuted after this period.
- /captchakick <yes/no/on/off>: Kick users that haven't solved the CAPTCHA.
- /captchakicktime <Xw/d/h/m>: Set the time after which to kick CAPTCHA'd users.
- /setcaptchatext <text>: Customise the CAPTCHA button.
- /resetcaptchatext: Reset the CAPTCHA button to the default text.

**Examples:**
- Enable CAPTCHAs
->` /captcha on`
- Change the CAPTCHA mode to text.
->` /captchamode text`
- Enable CAPTCHA rules, forcing users to read the rules before being allowed to speak.
->` /captcharules on`

NOTE:
captchakicktime now only accept time in Seconds, will fix soon.
captchas Work with or without welcome messages being set.
not finsihed writing.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})

