from Evie import tbot, CMD_HELP
from Evie.events import register
import asyncio, wget, time, requests, os, json
from youtube_dl import YoutubeDL
from PIL import Image
from youtubesearchpython import SearchVideos
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtube_dl.utils import (
    DownloadError,
    ContentTooShortError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

@register(pattern="^/ytmusic ?(.*)")
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
    await asyncio.sleep(0.2)
    downloaded_thumb = wget.download(thumb_url)
    image = Image.open(downloaded_thumb)
    new_image = image.resize((1080, 540))
    new_image.save('image69.jpg')
    thumb = './image69.jpg'
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
                "preferredquality": "480",
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
    author = ytdl_data["uploader"]
    await pablo.edit(f"Preparing to upload song:\n**{vid_title}**\nby **{author}**\n**Requested By:** {event.sender.first_name}")
    await tbot.send_file(
        event.chat_id,
        file,
        thumb=thumb,
        supports_streaming=True,
        force_document=False,
        attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=author,
                    waveform='320',
                )
            ],
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark, thumb):
        if files and os.path.exists(files):
            os.remove(files)
 except Exception as e:
  await event.reply(f"{e}")

@register(pattern="^/video ?(.*)")
async def deezr(v_url):
 try:
    url = v_url.pattern_match.group(1)
    rkp = await v_url.reply("Processing ...")
    if not url:
        await rkp.edit("Error \nusage video <song name>")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("Failed to find that video song")
    type = "video"
    await rkp.edit("`Preparing to download ...`")
    if type == "video":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await rkp.edit("`Fetching data, please wait ...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("The download content was too short.")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "Video is not available from your geographic location due to geographic restrictions imposed by a website."
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("Max-downloads limit has been reached.")
        return
    except PostProcessingError:
        await rkp.edit("There was an error during post processing.")
        return
    except UnavailableVideoError:
        await rkp.edit("Media is not available in the requested format.")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"{XAME.code}: {XAME.msg}\n{XAME.reason}")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    title = rip_data["title"]
    if video:
         await rkp.edit(f"Preparing to Upload Video:\n**{title}**\n**Requested by:** {v_url.sender.first_name}")
         y = await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data["title"]
        )
         
 except Exception as e:
    await v_url.reply(f'{e}')
 try:
   os.system("rm -rf *.mp4")
   os.system("rm -rf *.webp")
   os.system("rm -rf *.jpg")
 except:
     pass

@register(pattern="^/song ?(.*)")
async def yt(event):
    ult = event
    url = event.pattern_match.group(1)
    x = await event.reply("Searching...")
    if not url:
        return await x.edit("**Error**\nUsage - `.song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await x.edit("`No matching song found...`")
    type = "audio"
    await x.edit(f"`Preparing to download {url}...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await x.edit("`Getting info...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await x.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await x.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await x.edit(
            "`Video is not available from your geographic location due to"
            + " geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await x.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await x.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await x.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        return await x.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await x.edit("`There was an error during info extraction.`")
    except Exception as e:
        return await x.edit(f"{str(type(e)): {str(e)}}")
    dir = os.listdir()
    if f"{rip_data['id']}.mp3.jpg" in dir:
        thumb = f"{rip_data['id']}.mp3.jpg"
    elif f"{rip_data['id']}.mp3.webp" in dir:
        thumb = f"{rip_data['id']}.mp3.webp"
    else:
        thumb = None
    upteload = """
Uploading...
Song name - **{}**
By - **{}**
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await x.edit(f"{upteload}")
    async with tbot.action(event.chat_id, 'audio'):
     await tbot.send_file(
        ult.chat_id,
        f"{rip_data['id']}.mp3",
        thumb=thumb,
        supports_streaming=True,
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    await x.delete()
    os.remove(f"{rip_data['id']}.mp3")
    try:
        os.remove(thumb)
    except BaseException:
        pass
    
__help__ = """
- /song <name>: get song from youtube
- /ytmusic <name>: get song from youtube music
- /video <name>: gets video song from youtube
"""
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

