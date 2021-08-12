import asyncio
import os
from asyncio import Queue as _Queue
from asyncio import QueueEmpty as Empty
from typing import Dict

from PIL import Image, ImageDraw, ImageFont
from pymongo import MongoClient
from pytgcalls import GroupCallFactory
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipant,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
)

from .. import bot, vc

MONGO_DB_URI = os.environ["MONGO_DB_URI"]
CLIENT_TYPE = GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON

instances: Dict[int, GroupCallFactory] = {}
active_chats: Dict[int, Dict[str, bool]] = {}
db = MongoClient(MONGO_DB_URI)["neko"]


class Queue(_Queue):
    _queue: list = []

    def clear(self):
        self._queue.clear()


queues: Dict[int, Queue] = {}


async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()


def get(chat_id: int) -> Dict[str, str]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return {}
    return {}


def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True


def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass


def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].clear()
    raise Empty


def init_instance(chat_id: int):
    if chat_id not in instances:
        instances[chat_id] = GroupCallFactory(vc, CLIENT_TYPE).get_file_group_call()

    instance = instances[chat_id]

    @instance.on_playout_ended
    async def ___(__, _):
        task_done(chat_id)

        if is_empty(chat_id):
            await stop(chat_id)
        else:
            instance.input_filename = get(chat_id)["file"]


def remove(chat_id: int):
    if chat_id in instances:
        del instances[chat_id]

    if not is_empty(chat_id):
        clear(chat_id)

    if chat_id in active_chats:
        del active_chats[chat_id]


def get_instance(chat_id: int) -> GroupCallFactory:
    init_instance(chat_id)
    return instances[chat_id]


async def start(chat_id: int):
    await get_instance(chat_id).start(chat_id)
    active_chats[chat_id] = {"playing": True, "muted": False}


async def stop(chat_id: int):
    await get_instance(chat_id).stop()

    if chat_id in active_chats:
        del active_chats[chat_id]


async def set_stream(chat_id: int, file: str):
    if chat_id not in active_chats:
        await start(chat_id)
    get_instance(chat_id).input_filename = file


def pause(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif not active_chats[chat_id]["playing"]:
        return False

    get_instance(chat_id).pause_playout()
    active_chats[chat_id]["playing"] = False
    return True


def resume(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif active_chats[chat_id]["playing"]:
        return False

    get_instance(chat_id).resume_playout()
    active_chats[chat_id]["playing"] = True
    return True


async def transcode(filename):
    outname = filename.replace(".mp3", "")
    proc = await asyncio.create_subprocess_shell(
        cmd=(
            "ffmpeg "
            "-y -i "
            f"{filename} "
            "-f s16le "
            "-ac 2 "
            "-ar 48000 "
            "-acodec pcm_s16le "
            f"{outname}.raw"
        ),
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    os.remove(filename)
    return f"{outname}.raw"


async def can_manage_call(event, user_id):
    try:
        p = await bot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, ChannelParticipantAdmin):
        if not p.participant.admin_rights.manage_call:
            await event.reply(
                "You are missing the following rights to use this command: ManageGroupCall."
            )
            return False
        return True


def gen_cover(
    requested_by="RoseLoverX",
    title="Vaaste, by dhvani Banushali",
    duration="5:00",
    views="6M",
    thumbnail=None,
):
    image = Image.new("RGBA", (1280, 720), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Miley/assets/basefont.otf", 32)
    draw.text((205, 550), f"Title: {title}", (51, 215, 255), font=font)
    draw.text((205, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((205, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (205, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    image.save("test.png")
