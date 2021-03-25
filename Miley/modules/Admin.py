from Miley import tbot
from telethon.errors import (
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)

from telethon.tl.functions.channels import EditAdminRequest, EditPhotoRequest

from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from telethon import *
from telethon.tl import *
from telethon.errors import *

import os
from time import sleep
from telethon import events
from telethon.errors import FloodWaitError, ChatNotModifiedError
from telethon.errors import UserAdminInvalidError
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import *

from Miley import *
from Miley.events import register

from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest

from Miley import CMD_HELP
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError


# =================== CONSTANT ===================
PP_TOO_SMOL = "The image is too small"
PP_ERROR = "Failure while processing image"
NO_ADMIN = "I am not an admin"
NO_PERM = "I don't have sufficient permissions!"

CHAT_PP_CHANGED = "Chat Picture Changed"
CHAT_PP_ERROR = (
    "Some issue with updating the pic,"
    "maybe you aren't an admin,"
    "or don't have the desired rights."
)
INVALID_MEDIA = "Invalid Extension"


BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


# ================================================


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


async def can_promote_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


async def can_ban_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


async def can_del(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.delete_messages
    )


async def can_pin_msg(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.pin_messages
    )


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await tbot.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


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

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await tbot.get_entity(user_id)
                return user_obj
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj


def find_instance(items, class_or_tuple):
    for item in items:
        if isinstance(item, class_or_tuple):
            return item
    return None

@register(pattern="^/promote(?: |$)(.*)")
async def promote(promt):
    if promt.is_group:
      if not promt.sender_id == OWNER_ID:
        if not await is_register_admin(promt.input_chat, promt.sender_id):
           await promt.reply("Only admins can execute this command!")
           return
        else:
          if not await can_promote_users(message=promt):
            await promt.reply("You are missing the following rights to use this command:CanPromoteMembers")
            return
    else:
        return

    user = await get_user_from_event(promt)
    if promt.is_group:
        if await is_register_admin(promt.input_chat, user.id):
            await promt.reply("Why will i promote an admin ?")
            return
        pass
    else:
        return

    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await tbot(EditAdminRequest(promt.chat_id, user.id, new_rights, "Admin"))
        await promt.reply("Promoted Successfully!")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except Exception:
        await promt.reply("Failed to promote.")
        return
