from Evie import tbot, CMD_HELP
import os, re, csv, json, time, uuid
from Evie.function import is_admin
from io import BytesIO
import Evie.modules.sql.feds_sql as sql
from telethon import *
from telethon.tl import *
from telethon.tl.types import User
from Evie import *
from telethon.tl.types import MessageMediaDocument, DocumentAttributeFilename
from Evie.events import register


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("Pass the user's username, id or reply!")
            return

        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj

def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = eval(getsql["fusers"])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner["owner"]
    if str(user_id) == getfedowner or int(user_id) == OWNER_ID:
        return True
    else:
        return False


@register(pattern="^/newfed ?(.*)")
async def new(event):
 if not event.is_private:
  return await event.reply("Create your federation in my PM - not in a group.")
 name = event.pattern_match.group(1)
 fedowner = sql.get_user_owner_fed_full(event.sender_id)
 if fedowner:
    for f in fedowner:
            text = "{}".format(f["fed"]["fname"])
    return await event.reply(f"You already have a federation called `{text}` ; you can't create another. If you would like to rename it, use /renamefed.")
 if not name:
  return await event.reply("You need to give your federation a name! Federation names can be up to 64 characters long.")
 if len(name) > 64:
  return await event.reply("Federation names can only be upto 64 charactors long")
 fed_id = str(uuid.uuid4())
 fed_name = name
 x = sql.new_fed(event.sender_id, fed_name, fed_id)
 if x:
   await event.reply("Created new federation with FedID: `{}`.\nUse this ID to join the federation! eg:\n`/joinfed {}`").format(fed_id, fed_id)
   
 
 

 
 


