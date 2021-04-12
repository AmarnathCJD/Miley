from Evie import tbot, OWNER_ID, BOT_ID
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from Evie.modules.sql.karma_sql import (update_karma, get_karma, get_karmas,
                                   int_to_alpha, alpha_to_int)
from Evie.modules.sql.karma_sql import add_chat, rmchat, is_chat, get_all_chat_id
from Evie.events import register
from Evie.function import is_admin


regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|Na|Gey|noob)$"

@tbot.on(events.NewMessage(pattern=None))
async def kk(event):
 if event.is_private:
   return
 if not is_chat(event.chat_id):
   return
 if event.media:
   return
 if not event.text:
   return
 if event.text in regex_upvote:
   pass
 else:
   return
 if not event.reply_to_msg_id:
   return
 previous_message = await event.get_reply_message()
 user_id = previous_message.sender_id
 if not event.sender_id == OWNER_ID:
   if event.sender_id == user_id or user_id == BOT_ID:
      return
 arg = await tbot(GetFullUserRequest(user_id))
 fname = arg.user.first_name
 chat_id = int(event.chat_id)
 current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
 if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma + 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
 else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
 await tbot.send_message(event.chat_id, f"Incremented Karma of [{fname}](tg://user?id={user_id}) By 1 \nTotal Points: {karma}")
 

@tbot.on(events.NewMessage(pattern=None))
async def rv(event):
 if event.is_private:
   return
 if not is_chat(event.chat_id):
   return
 if event.media:
   return
 if event.text == None:
   return
 if event.text in regex_downvote:
   pass
 else:
   return
 if not event.reply_to_msg_id:
   return
 previous_message = await event.get_reply_message()
 user_id = previous_message.sender_id
 if not event.sender_id == OWNER_ID:
   if event.sender_id == user_id or user_id == BOT_ID:
      return
 arg = await tbot(GetFullUserRequest(user_id))
 fname = arg.user.first_name
 chat_id = int(event.chat_id)
 current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
 if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma - 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
 else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
 await tbot.send_message(event.chat_id, f"Decremented Karma Of [{fname}](tg://user?id={user_id}) By 1 \nTotal Points: {karma}")
 

@register(pattern=^/setkarma ?(.*)")
async def st(event):
 if not event.sender_id == OWNER_ID:
    return
 args = int(event.pattern_match.group(1))
 if not args:
   return await event.reply("Invalid args")
 previous_message = await event.get_reply_message()
 if previous_message:
   user_id = previous_message.sender_id
 else:
   user_id = event.sender_id
 arg = await tbot(GetFullUserRequest(user_id))
 fname = arg.user.first_name
 current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
 if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma + args
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
 else:
        karma = args
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
 await tbot.send_message(event.chat_id, f"Changed Karma Of [{fname}](tg://user?id={user_id}) By {args} \nTotal Points: {karma}")


@register(pattern="^/karma ?(.*)")
async def kr(event):
 args = event.pattern_match.group(1)
 if args:
  if not await is_admin(event, event.sender_id):
     return await event.reply("You need to be an admin to do this!")
  if args == 'on' or args == 'enable':
    if not is_chat(event.chat_id):
              await event.reply("Karma has been enabled for this Chat!")
              return add_chat(event.chat_id)
    else:
       return await event.reply("Karma is already enabled for this chat")
  elif args == 'off' or args == 'disable':
    if is_chat(event.chat_id):
             await event.reply("Karma has been disabled for this Chat!")
             return rmchat(event.chat_id)
    else:
       return await event.reply("Karma is not enabled here in the first place!")
 chat_id = event.chat_id
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return
 if not is_chat(event.chat_id):
  return await event.reply("Karma is disabled for this Chat!")
 if not event.reply_to_msg_id:
        karma = await get_karmas(chat_id)
        msg = f"**Karma list of {event.chat.title}:- **\n"
        limit = 0
        karma_dicc = {}
        for i in karma:
           user_id = await alpha_to_int(i)
           user_karma = karma[i]['karma']
           karma_dicc[str(user_id)] = user_karma
           karma_arranged = dict(
           sorted(karma_dicc.items(), key=lambda item: item[1], reverse=True))
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                arg = await tbot.get_entity(int(user_idd))
                user_name = arg.username
            except Exception:
                user_name = user_idd
                continue
            msg += f"{user_name} : `{karma_count}`\n"
            limit += 1
        await event.reply(msg)
 else:
  previous_message = await event.get_reply_message()
  user_id = previous_message.sender_id
  karma = await get_karma(chat_id, await int_to_alpha(user_id))
  if karma:
       karma = karma['karma']
       await event.reply(f'**Total Points**: __{karma}__')
  else:
       karma = 0
       await event.reply(f'**Total Points**: __{karma}__')


 

 
 
