from telethon.tl import functions
from telethon.tl import types
import time, subprocess, shlex, os, asyncio, math
from Evie import tbot, BOT_ID
from typing import Tuple
import Evie.modules.sql.elevated_sql as sql
from Evie.modules.sql.chats_sql import add_chat, rmchat, is_chat, get_all_chat_id
from Evie.modules.sql.setbio_sql import set_bio, rm_bio, check_bio_status, is_bio, get_all_bio_id


async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod

async def bot_ban(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=BOT_ID,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

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

async def can_approve_users(message):
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

def sudo(iid):
  k = iid
  if sql.is_sudo(k):
   return True
  else:
   return False

def bio(iid):
 k = iid
 if is_bio(k):
  return True
 else:
  return False

async def get_user(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj, extra


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
            ((str(days) + " day(s), ") if days else "")
            + ((str(hours) + " hour(s), ") if hours else "")
            + ((str(minutes) + " minute(s), ") if minutes else "")
            + ((str(seconds) + " second(s), ") if seconds else "")
            + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

def humanbytes(size):
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

async def cb_progress(current, total, cb, start, type_of_ps, file_name=None):
    """Progress Bar For Showing Progress While Uploading / Downloading File - Inline"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )


async def fetch_audio(tbot, event):
    c_time = time.time()
    if not message.reply_to_message:
        await sz.edit("`Reply To A Video / Audio.`")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await sz.edit("Format Not Supported.")
        return
    if warner_stark.video:
        await sz.edit("Video Detected, Converting To Audio !")
        warner_bros = await tbot.download_media(
                warner_stark.video,
            progress=progress, progress_args=(message, c_time, f"Downloading Audio!")
        )
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a evie.mp3"
        await runcmd(stark_cmd)
        final_warner = "evie.mp3"
    elif warner_stark.audio:
        await sz.edit("Download Started !")
        final_warner = await tbot.download_media(
                warner_stark.video,
            progress=progress, progress_args=(message, c_time, f"Downloading Video!")
        )
    await sz.edit("Almost Done!")
    return final_warner

