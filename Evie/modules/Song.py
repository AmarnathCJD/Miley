from Evie import tbot
from Evie.events import register
import asyncio, wget, time, requests, os
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos


@register(pattern="^/song ?(.*)")
async def yt(event):
 try:
    input_str = event.pattern_match.group(1)
    pablo = await event.reply(f"Getting {input_str} From Youtube Servers. Please Wait.")
    if not input_str:
        await pablo.edit(
            "Please Give Me A Valid Input."
        )
        return
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    try:
        result_s = rt["search_result"]
    except:
        await pablo.edit(
            f"Song Not Found With Name {input_str}."
        )
        return
    url = result_s[0]["link"]
    result_s[0]["duration"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**Song Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    file_stark = f"{ytdl_data['id']}.mp3"
    file=open(file_stark, "rb")
    async with tbot.action(event.chat_id, 'audio'):
       await tbot.send_file(
        event.chat_id,
        file,
        thumb=downloaded_thumb,
        voice_note=True,
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
 except Exception as e:
  await event.reply(f"{e}")
