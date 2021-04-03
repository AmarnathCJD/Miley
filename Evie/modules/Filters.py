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

last_triggered_filters = {}  # pylint:disable=E0602

@register(pattern="^/addfilter ?(.*)")
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
          snip = {"type": "", "text": ""}
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

   
