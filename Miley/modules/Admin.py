from Miley import tbot, BOT_ID
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
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.add_admins
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
            await event.reply("You need to specify a user by replying, or providing a username or user id...!")
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

@register(pattern="^/promote ?(.*)")
async def promote(promt):
    text = promt.pattern_match.group(1)
    if text == None:
      title = 'Admin'
    else:
      title = text
    if promt.is_group:
      if not promt.sender_id == OWNER_ID:
        if not await is_register_admin(promt.input_chat, promt.sender_id):
           await promt.reply("Only admins can execute this command!")
           return
        
    else:
        return
    if not await can_promote_users(message=promt):
            await promt.reply("You are missing the following rights to use this command:CanPromoteMembers")
            return
    user = await get_user_from_event(promt)
    if user.id == BOT_ID:
       await promt.reply("I can't promote myself! Get an admin to do it for me.")
       return
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
        await tbot(EditAdminRequest(promt.chat_id, user.id, new_rights, title))
        await promt.reply("Promoted!")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except Exception:
        await promt.reply("Failed to promote.")
        return

@register(pattern="^/demote(?: |$)(.*)")
async def demote(dmod):
    if dmod.is_group:
      if not dmod.sender_id == OWNER_ID:
        if not await is_register_admin(dmod.input_chat, dmod.sender_id):
           await dmod.reply("Only admins can execute this command!")
           return
        else:
          if not await can_promote_users(message=dmod):
            await dmod.reply("You are missing the following rights to use this command:CanPromoteMembers")
            return
    else:
        return

    user = await get_user_from_event(dmod)
    if user.id == BOT_ID:
       await dmod.reply("Ya I won't Demote Myself! Get an admin to do it for You.")
       return
    if dmod.is_group:
        if not await is_register_admin(dmod.input_chat, user.id):
            await dmod.reply("This user is not an admin!")
            return
        pass
    else:
        return

    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await tbot(EditAdminRequest(dmod.chat_id, user.id, newrights, "Admin"))
        await dmod.reply("Demoted Successfully!")

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except Exception:
        await dmod.reply("Failed to demote.")
        return


@register(pattern="^/(ban|dban|unban) ?(.*)")
async def ban(bon):
    if not bon.is_group:
        return
    if bon.is_group:
      if not bon.sender_id == OWNER_ID:
       if not await is_register_admin(bon.input_chat, bon.sender_id):
           await bon.reply("Only admins can execute this command!")
           return
       if not await can_ban_users(message=bon):
            await bon.reply("You are missing the following rights to use this command:CanRestrictMembers")
            return
    k = bon.pattern_match.group(1)
    if k == 'dban':
       prev = await bon.get_reply_message()
       await prev.delete()
    user = await get_user_from_event(bon)
    if user.id == BOT_ID:
      await bon.reply("You know what I'm not going to do? Ban myself.")
      return
    if user:
        pass
    else:
        return

    if bon.is_group:
        if await is_register_admin(bon.input_chat, user.id):
            await bon.reply("Why would I ban an admin? That sounds like a pretty dumb idea.")
            return
        pass
    else:
        return

    try:
        await tbot(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
        await bon.reply(f"Another one bites the dust...!Banned [User](tg://user?id={user.id}).")

    except Exception:
        await bon.reply("I haven't got the rights to do this.")
        return

@register(pattern="^/unban ?(.*)")
async def unban(bon):
    
    if not bon.is_group:
        return
    if bon.is_group:
      if not bon.sender_id == OWNER_ID:
       if not await is_register_admin(bon.input_chat, bon.sender_id):
           await bon.reply("Only admins can execute this command!")
           return
       if not await can_ban_users(message=bon):
            await bon.reply("You are missing the following rights to use this command:CanRestrictMembers")
            return

    user = await get_user_from_event(bon)
    if user:
        pass
    else:
        await bon.reply("I don't know who you're talking about, you're going to need to specify a user...!")
        return

    if bon.is_group:
        if await is_register_admin(bon.input_chat, user.id):
            await bon.reply("Yeah, Ask RoseBot To do Stupidity!.")
            return
        pass
    else:
        return

    try:
        await tbot(EditBannedRequest(bon.chat_id, user.id, UNBAN_RIGHTS))
        await bon.reply("Fine, they can join again.")

    except BaseException:
        await bon.reply("This person hasn't been banned... how am I meant to unban them?")
        return
