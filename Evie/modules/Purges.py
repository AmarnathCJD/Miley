from Evie import tbot, CMD_HELP, MONGO_DB_URI
from telethon import events, Button
from Evie.events import register
from Evie.function import can_del, is_admin
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from pymongo import MongoClient
import os

Mark = []
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
pugre = db.purge

def get_chat(id):
    return pugre.find_one({"id": id})

@tbot.on(events.NewMessage(pattern="^[!/]purge ?(.*)"))
async def purge(event):
 args = event.pattern_match.group(1)
 if args:
  try:
   k = int(args)
  except:
    return
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing DelMessage rights to use this command!")
 reply_msg = await event.get_reply_message()
 if not reply_msg:
  return await event.reply("Reply to a message to show me where to purge from.")
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 if args:
  limit = int(args)
  if limit == 1:
    return await event.reply("Oh please use `/del` ಥ‿ಥ")
 else:
  limit = 300
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")
 await tbot.send_message(event.chat_id, "Purge complete.")

@tbot.on(events.NewMessage(pattern="^[!/]purgefrom"))
async def mm(event):
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing delmessage rights to use this command!")
 reply_msg = await event.get_reply_message()
 if not reply_msg:
  return await event.reply("Reply to a message to show me where to purge from.")
 msg_id = reply_msg.id
 chats = pugre.find({})
 for c in chats:
  if event.chat_id == c["id"]:
    to_check = get_chat(id=event.chat_id)
    pugre.update_one(
           {
              "_id": to_check["_id"],
              "id": to_check["id"],
              "msg_id": to_check["msg_id"],
            },
             {"$set": {"msg_id": msg_id}},
            )
    return await tbot.send_message(event.chat_id, "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.", reply_to=msg_id)
 pugre.insert_one(
        {"id": event.chat_id, "msg_id": msg_id}
    )
 await tbot.send_message(event.chat_id, "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.", reply_to=msg_id)

@tbot.on(events.NewMessage(pattern="^[!/]purgeto"))
async def mm(event):
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing delmessage rights to use this command!")
 reply_msg = await event.get_reply_message()
 if not reply_msg:
   return await event.reply("Reply to a message to let me know what to delete.")
 msg_id = None
 chats = pugre.find({})
 for c in chats:
  if event.chat_id == c["id"]:
    msg_id = c["msg_id"]
 if msg_id == None:
   return await event.reply("You can only use this command after having used the /purgefrom command.")
 messages = []
 limit = 300
 delete_to = event.reply_to_msg_id
 messages.append(event.reply_to_msg_id)
 for id in range(msg_id, delete_to + 1):
   messages.append(id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")
 chats = pugre.find({})
 for c in chats:
   if event.chat_id == c["id"]:
     pugre.delete_one({"id": event.chat_id})
  
@tbot.on(events.NewMessage(pattern="^[!/]spurge ?(.*)"))
async def purge(event):
 args = event.pattern_match.group(1)
 if args:
  try:
   k = int(args)
  except:
    return
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing DelMessage rights to use this command!")
 reply_msg = await event.get_reply_message()
 if not reply_msg:
  return await event.reply("Reply to a message to show me where to purge from.")
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 if args:
  limit = int(args)
  if limit == 1:
    return await event.reply("Oh please use `/del` ಥ‿ಥ")
 else:
  limit = 300
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")

@tbot.on(events.NewMessage(pattern="^[!/]del"))
async def purge(event):
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing delmessage rights to use this command!")
 reply_msg = await event.get_reply_message()
 if not reply_msg:
   return await event.reply("Reply to a message to let me know what to delete.")
 chat = await event.get_input_chat()
 del_message = [reply_msg, event.message]
 try:
    await tbot.delete_messages(chat, del_message)
 except MessageDeleteForbiddenError:
    return await event.reply("I can't delete messages that are too old!")

@register(pattern="^/smellycat")
async def sc(event):
 await event.reply("Where are you...!\nSmelly cat smellly cat..\n( ･ั﹏･ั)")

__help__ = """
Need to delete lots of messages? That's what purges are for!

**Admin commands:**
- /purge: Delete all messages from the replied to message, to the current message.
- /purge <X>: Delete the following X messages after the replied to message.
- /spurge: Same as purge, but doesnt send the final confirmation message.
- /del: Deletes the replied to message.
- /purgefrom: Reply to a message to mark the message as where to purge from - this should be used followed by a /purgeto.
- /purgeto: Delete all messages between the replied to message, and the message marked by the latest /purgefrom.

**Examples:**
- Delete all messages from the replied to message, until now.
-> /purge
- Mark the first message to purge from (as a reply).
-> /purgefrom
- Mark the message to purge to (as a reply). All messages between the previously marked /purgefrom and the newly marked /purgeto will be deleted.
-> /purgeto
"""


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
