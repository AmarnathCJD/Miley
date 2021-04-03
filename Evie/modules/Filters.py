from Evie import CMD_HELP, tbot
import os
from Evie.events import register
from Evie.function import is_admin, can_change_info
import asyncio
import re
from telethon.tl import types

from telethon import utils, Button
from telethon import events
from Evie.modules.sql.filters_sql import (
    add_filter,
    get_all_filters,
    remove_filter,
    remove_all_filters,
)

DELETE_TIMEOUT = 0

TYPE_TEXT = 0

TYPE_PHOTO = 1

TYPE_DOCUMENT = 2


@register(pattern="^/filter ?(.*)")
async def save(event):
 if not event.reply_to_msg_id:
     input = event.pattern_match.group(1)
     if input:
       arg = input.split(" ", 1)
     if len(arg) == 2:
      name = arg[0]
      msg = arg[1]
      snip = {"type": TYPE_TEXT, "text": msg}
     else:
      name = arg[0]
      if not name:
        await event.reply("You need to give the filter a name!")
        return
      await event.reply("You need to give the filter some content!")
      return
 else:
      message = await event.get_reply_message()
      name = event.pattern_match.group(1)
      if not message.media:
          msg = message.text
          snip = {"type": TYPE_TEXT, "text": msg}
      else:
          snip = {"type": TYPE_TEXT, "text": ""}
          media = None
          if isinstance(message.media, types.MessageMediaPhoto):
             media = utils.get_input_photo(message.media.photo)
             snip["type"] = TYPE_PHOTO
          elif isinstance(message.media, types.MessageMediaDocument):
             media = utils.get_input_document(message.media.document)
             snip["type"] = TYPE_DOCUMENT
          if media:
             snip["id"] = media.id
             snip["hash"] = media.access_hash
             snip["fr"] = media.file_reference
 add_filter(
            event.chat_id,
            name,
            snip["text"],
            snip["type"],
            snip.get("id"),
            snip.get("hash"),
            snip.get("fr"),
        )
 await event.reply(f"Saved filter `{name}`")

@register(pattern="^/listfilters$")
async def on_snip_list(event):
    if event.is_group:
        pass
    else:
        return
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = f"**List of filters in {event.chat.title}:**\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"- `{a_snip.keyword}`\n"
    else:
        OUT_STR = "No Filters. Start Saving using /savefilter"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Filters in the Current Chat",
                reply_to=event,
            )
    else:
        await event.reply(OUT_STR)

@register(pattern="^/stop (.*)")
async def on_snip_delete(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await event.reply(f"Filter '**{name}**' has been stopped!")

@register(pattern="^/stopall$")
async def on_all_snip_delete(event):
 if not event.is_group:
   return
 if not await is_admin(event, event.sender_id):
   await event.reply("You need to be an admin to do this.")
   return
 permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
 if not permissions.is_creator:
          return await event.reply(f"You need to be the chat owner of {event.chat.title} to do this.")
 TEXT = f"Are you sure you would like to clear **ALL** filters in {event.chat.title}? This action cannot be undone."
 await tbot.send_message(
            event.chat_id,
            TEXT,
            buttons=[
                [Button.inline("Delete all filters", data="confirm")],[Button.inline("Cancel", data="rt")],],
            reply_to=event.id
           )
@tbot.on(events.CallbackQuery(pattern=r"rt"))
async def start_again(event):
        permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not permissions.is_creator:
           return await event.answer("Yeah suck my dick")
        await event.edit("Clearing of all filters has been cancelled.")

@tbot.on(events.CallbackQuery(pattern=r"confirm"))
async def start_again(event):
        permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not permissions.is_creator:
           return await event.answer("Yeah suck my dick")
        remove_all_filters(event.chat_id)
        await event.edit("Deleted all chat filters.")


#balance Soon
