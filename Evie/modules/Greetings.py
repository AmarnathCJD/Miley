from telethon import events
from Evie import tbot, BOT_ID
from Evie.events import register
import os
from Evie.function import can_change_info, is_admin
from telethon import *
from telethon.tl import *
from telethon.utils import pack_bot_file_id

from Evie.modules.sql.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from Evie.modules.sql.welcome_sql import (
    add_goodbye_setting,
    get_current_goodbye_settings,
    rm_goodbye_setting,
    update_previous_goodbye,
)


@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        if event.user_joined:
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
            current_message = await event.reply(
                    current_saved_welcome_message.format(
                        mention=mention,
                        title=title,
                        first=first,
                        last=last,
                        fullname=fullname,
                        userid=userid,
                    ),
                    file=cws.media_file_id,
                )

@register(pattern="^/setwelcome")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, False, 0, tbot_api_file_id)
        await event.reply("Welcome message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], False, 0, None)
        await event.reply("Welcome message saved. ")


@register(pattern="^/clearwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.reply(
        "Welcome message cleared. "
        + "The previous welcome message was `{}`".format(cws.custom_welcome_message)
    )

