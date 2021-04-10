
from Evie.

@tbot.on(events.NewMessage(pattern="^[!/]dban$"))
async def dban(event): 
  if not event.sender_id == 1087968824 or event.sender_id == 1704673514:
    if not await user_is_admin(event, event.sender_id):
       return await event.reply("Only Admins can execute this command!")
    if not await can_ban_users(message=event):
        await event.reply("I don't have enough rights to do that!")
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Reply to someone to delete the message and ban the user!")
        return
    x = (await event.get_reply_message()).sender_id
    zx = (await event.get_reply_message())
    await zx.delete()
    await telethn(EditBannedRequest(event.chat_id, x, ChatBannedRights(until_date=None, view_messages=True)))
    await event.reply("Successfully Banned!")
