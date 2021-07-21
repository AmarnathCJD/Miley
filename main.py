import io
import logging
import sys
import traceback
from os import environ as e

import youtube_dl
from pytgcalls import GroupCallFactory
from telethon import Button, TelegramClient, events
from telethon.sessions import StringSession
from youtubesearchpython import SearchVideos

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
from dotenv import load_dotenv

load_dotenv()
import asyncio

API_KEY = e.get("API_KEY")
API_HASH = e.get("API_HASH")
TOKEN = e.get("TOKEN")
STRING_SESSION = e.get("STRING_SESSION")
CLIENT_TYPE = GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON

bot = (TelegramClient(None, API_KEY, API_HASH)).start(bot_token=TOKEN)
vc = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)

vc.start()
dict_1 = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(id)s.mp3",
    "quiet": True,
}

from mtest import vc_db


@bot.on(events.NewMessage(pattern="^/playvc ?(.*)"))
async def playvc(e):
    song = e.pattern_match.group(1)
    search = SearchVideos(song, offset=1, mode="dict", max_results=5)
    final_text = ""
    q = -1
    kdawg = (search.result())["search_result"]
    for x in kdawg:
        q += 1
        final_text += f"\n{dict_1[q]}<b>{x.get('title')}</b>\n  ┗  🔗 <i><a href='t.me/missneko_bot?start=help'>Get Additional Information</a></i>"
    buttons = []
    bt = []
    for x in range(0, 5):
        cb_data = kdawg[x].get("id") + "|" + str(e.sender_id)
        d = Button.inline(dict_1[x], data="play_{}".format(cb_data))
        bt.append(d)
        if len(bt) == 3 or x == 4:
            buttons.append(bt)
            bt = []
    buttons.append(
        [Button.inline("🗑️ Close Menu", data="close_menu|" + str(e.sender_id))]
    )
    await e.respond(
        final_text,
        buttons=buttons,
        file=kdawg[0].get("thumbnails")[4],
        parse_mode="html",
    )


x_info = """
🎥<b>Playing:</b> <a href="https://www.youtube.com/watch?v={}">{}</a>
⏳<b>Duration:</b> {}
💡<b>Info:</b> <a href="https://t.me/missneko_bot?start=help">Get Additional Information</a>
👤<b>Requested by:</b> {}
"""


@bot.on(events.CallbackQuery(pattern=r"play(\_(.*))"))
async def play_cb_(e):
    song_id, sender_id = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split(
        "|", 1
    )
    if not int(sender_id) == e.sender_id:
        return await e.answer("This is not for you!", alert=True)
    song_id = song_id.strip()
    song = (
        (SearchVideos(song_id, max_results=1, mode="dict")).result()["search_result"]
    )[0]
    song_name = song.get("title")
    x = await e.edit(f"Downloading **{song_name}** Now!")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_id])
    file_path = f"{song_id}.mp3"
    out = f"{song_id}.raw"
    proc = await asyncio.create_subprocess_shell(
        cmd=(
            "ffmpeg "
            "-y -i "
            f"{file_path} "
            "-f s16le "
            "-ac 2 "
            "-ar 48000 "
            "-acodec pcm_s16le "
            f"{out}"
        ),
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    if proc.returncode != 0:
        return await x.edit("FFmpeg Error during media processing.")
    buttons = [
        [
            Button.inline("⏸️", data="pause"),
            Button.inline("⏭️", data="next"),
            Button.inline("⏹️", data="stop"),
        ],
        [Button.inline("➕ Group Playlist", data="group_playlist")],
        [Button.inline("➕ Personal Playlist", data="my_playlist")],
        [Button.inline("🗑️ Close Menu", data="close_menu")],
    ]
    await x.edit(
        x_info.format(song_id, song_name, song.get("duration"), e.sender.first_name),
        parse_mode="html",
        buttons=buttons,
    )
    group_call = GroupCallFactory(vc, CLIENT_TYPE).get_file_group_call(out, "out.raw")
    await group_call.start(e.chat_id)
    vc_db[e.chat_id] = group_call


@bot.on(events.CallbackQuery(pattern=r"pause"))
async def pause_playout(e):
    try:
        group_call = vc_db[e.chat_id]
    except KeyError:
        return await e.reply("M")
    try:
        await group_call.pause_playout()
    except TypeError:
        pass
    text = "🎧 Voicechat Paused by <a href='tg://user?id={}'>{}</a>!".format(
        e.sender_id, e.sender.first_name
    )
    buttons = [
        [
            Button.inline("▶️", data="playboy"),
            Button.inline("⏭️", data="next"),
            Button.inline("⏹️", data="stop"),
        ],
        [Button.inline("Close Menu", data="close_menu")],
    ]
    await e.edit(text, buttons=buttons, parse_mode="html")


@bot.on(events.CallbackQuery(pattern=r"playboy"))
async def resume_playout(e):
    try:
        group_call = vc_db[e.chat_id]
    except KeyError:
        return await e.reply("M")
    try:
        await group_call.resume_playout()
    except TypeError:
        pass
    text = "🎧 Voicechat Resumed by <a href='tg://user?id={}'>{}</a>!".format(
        e.sender_id, e.sender.first_name
    )
    buttons = [
        [
            Button.inline("⏸️", data="pause"),
            Button.inline("⏭️", data="next"),
            Button.inline("⏹️", data="stop"),
        ],
        [Button.inline("Close Menu", data="close_menu")],
    ]
    await e.edit(text, buttons=buttons, parse_mode="html")


@bot.on(events.CallbackQuery(pattern=r"stop"))
async def stop_playout(e):
    try:
        group_call = vc_db[e.chat_id]
    except KeyError:
        return await e.reply("M")
    try:
        await group_call.stop_playout()
    except TypeError:
        pass
    text = "🎧 Voicechat End/Stopped by <a href='tg://user?id={}'>{}</a>!".format(
        e.sender_id, e.sender.first_name
    )
    await e.edit(text, buttons=None, parse_mode="html")


@bot.on(events.NewMessage(pattern="^/eval ?(.*)"))
async def val(event):
    cmd = event.text.split(" ", maxsplit=1)[1]
    if event.sender_id == 1743998809:
        pass
    else:
        return
    if event.reply_to:
        await event.get_reply_message()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "`{}`".format(evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
            )

    else:
        await event.respond(final_output)


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, bot, p)


bot.run_until_disconnected()
