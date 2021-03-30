from pymongo import MongoClient
from Evie import MONGO_DB_URI, DEV_USERS, OWNER_ID, BOT_ID, SUDO_USERS
from Evie.events import register
from Evie import tbot

import os
import sys
from os import execl
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
blacklist = db.black

from Evie.modules.sql.checkuser_sql import get_all_users
import Evie.modules.sql.elevated_sql as sql
from Evie.modules.sql.chats_sql import add_chat, rmchat, is_chat, get_all_chat_id
from Evie.modules.sql.setbio_sql import set_bio, rm_bio, check_bio_status, is_bio, get_all_bio_id


def sudo(iid):
  k = iid
  if sql.is_sudo(k):
   return True
  else:
   return False

def bio(iid):
 k = iid
 if is_bio(k):
  return True
 else:
  return False

from telethon import events
from Evie import BOT_ID, tbot

@tbot.on(events.ChatAction)
async def handler(event):
    if event.user_added:
        if event.user_id == BOT_ID:
           if not is_chat(event.chat_id):
                add_chat(event.chat_id)
           await tbot.send_message(-1001486931338, f"Evie Added to {event.chat.title}\n`{event.chat_id}`")
           await tbot.send_message(event.chat_id, "Heya :-D Now leave your group on my hands and let me manage it. If you need any help, head to @EvieSupport.")
              
@tbot.on(events.ChatAction)
async def handler(event):
    if event.user_kicked:
        if event.user_id == BOT_ID:
              rmchat(event.chat_id)


@register(pattern="^/stats")
async def stat(event):
    if event.sender_id == OWNER_ID:
     pass
    elif event.sender_id in DEV_USERS:
     pass
    else:
     return
    used = get_all_users()
    await event.reply(f"<b>I have <u>{len(used)}</u> Users In My Database.</b>", parse_mode="HTML")

@register(pattern="^/addsudo ?(.*)")
async def approve(event):
   if event.sender_id == OWNER_ID:
      pass
   else:
      return
   sender = event.sender_id
   reply_msg = await event.get_reply_message()
   iid = reply_msg.sender_id
   fname = reply_msg.sender.first_name
   if iid == OWNER_ID:
     return
   if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("Whokey")
        return
   if sql.is_sudo(iid):
      await event.reply("This is already a pro Sudo!")
      return
   await event.reply("Sucessfully set the Disaster level of this user to **Sudo User**.")
   sql.set_sudo(iid, fname)
   
@register(pattern="^/delsudo ?(.*)")
async def approve(event):
   if event.sender_id == OWNER_ID:
      pass
   else:
      return
   sender = event.sender_id
   bl = blacklist.find({})
   reply_msg = await event.get_reply_message()
   iid = reply_msg.sender_id
   if iid == OWNER_ID:
     return
   if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("Whokey")
        return
   if sql.is_sudo(iid):
         sql.rm_sudo(iid)
         await event.reply("Removed From **Sudo Users**.")
         return
   await event.reply("This is not event a Sudo User;(")
   

@register(pattern="^/sudolist")
async def sud(event):
 res = []
 k = sql.SUDO_USERS
 reply = "**SUDO_USERS:**\n\n"
 for i in k:
  sep = i
  value = k[i]
  reply += f"•💸{value} (`{sep}`)\n"
 await event.reply(reply)
 

@register(pattern="^/blacklist ?(.*)")
async def approve(event):
   if event.sender_id == OWNER_ID:
      pass
   elif event.sender_id in DEV_USERS:
      pass
   else:
      return
   sender = event.sender_id
   bl = blacklist.find({})
   reply_msg = await event.get_reply_message()
   iid = reply_msg.sender_id
   if iid == OWNER_ID:
     return
   elif iid in DEV_USERS:
     return
   elif iid in SUDO_USERS:
     return
   elif sudo(iid):
     return
   if event.sender_id == BOT_ID or int(iid) == int(BOT_ID):
        await event.reply("I am not gonna blacklist myself")
        return
   a = blacklist.find({})
   for i in a:
         if iid == i["user"]:
                await event.reply("This User is Already Blacklisted")
                return
   blacklist.insert_one({"user": iid})
   await event.reply("Successfully Blacklisted This Retard")
   loda=""
   try:
     for i in a:
       k = i["user"]
       loda += f"{k}\n"
   except Exception as ok:
       await e.reply(ok)
   await event.reply(loda)

@register(pattern="^/unblacklist ?(.*)")
async def approve(event):
   if event.sender_id == OWNER_ID:
      pass
   elif event.sender_id in DEV_USERS:
      pass
   else:
      return
   sender = event.sender_id
   bl = blacklist.find({})
   reply_msg = await event.get_reply_message()
   iid = reply_msg.sender_id
   a = blacklist.find({})
   for i in a:
       if iid == i["user"]:
            blacklist.delete_one({"user": iid})
            await event.reply("Successfully Unblacklisted User")
            return
   await event.reply("This User isn't Blacklisted yet")

@register(pattern="^/checkbl")
async def isbl(e):
   if e.sender_id == OWNER_ID:
      pass
   elif e.sender_id in DEV_USERS:
      pass
   else:
      return
   
   bl = blacklist.find({})
   reply = "Blacklisted Users\n"
   try:
     for i in bl:
       k = i["user"]
       reply += f"•`{k}`\n"
   except Exception as ok:
       await e.reply(ok)
   await e.reply(reply)
        
import subprocess
import asyncio
import traceback
import io
import os
import sys
import time
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
from telethon.errors import *


@register(pattern="^/exec (.*)")
async def msg(event):
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id in SUDO_USERS:
        await event.reply("This is a Assembler restricted command. You do not have permissions to run this.")
        return
    elif event.sender_id in DEV_USERS:
        await event.reply("This is a Assembler restricted command. You do not have permissions to run this.")
        return
    else:
        return
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    await event.reply(f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
)

@register(pattern="^/eval")
async def _(event):
    cmd = event.text.split(" ", maxsplit=1)[1]
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id in DEV_USERS or event.sender_id in SUDO_USERS:
        if "os.environ.get" in cmd:
          await event.reply("Can't access env variables.")
          return
        if "sys.exit" in cmd:
          await event.reply("You have no permission to shutdown Me.")
          return
        if "from Luna import abot" in cmd or "from Luna import STRING_SESSION" in cmd:
          await event.reply("Can't Acess Master Account.")
          return
        if "await tbot.send_message" in cmd or "from Luna import STRING_SESSION" in cmd:
          await event.reply("Ni Hoskta!")
          return
        pass
    else:
        return
    
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "`{}`".format(evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )

    else:
        await event.reply(final_output)

from Evie import ubot, OWNER_ID
from telethon import events


   


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, tbot, p)

async def fexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(_format.yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        f"async def __aexec(message, event , reply, client, p, chat): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )
