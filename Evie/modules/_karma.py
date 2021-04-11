from Evie import tbot, OWNER_ID, BOT_ID
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from Evie.modules.sql.karma_sql import (update_karma, get_karma, get_karmas,
                                   int_to_alpha, alpha_to_int)


regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"

@tbot.on(events.NewMessage(pattern=None))
async def kk(event):
 if event.is_private:
   return
 if event.text == None:
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
 chat_id = event.chat_id
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
 
 
 
 
 
 
 
 
