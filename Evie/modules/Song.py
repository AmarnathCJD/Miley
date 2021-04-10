from Evie import tbot
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
    await asyncio.sleep(0.2)
    downloaded_thumb = wget.download(thumb_url)
    image = Image.open(downloaded_thumb)
    new_image = image.resize((1920, 1080))
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
    await pablo.edit(f"Preparing to upload song:\n**{vid_title}**\nby **{author}**")
    async with tbot.action(event.chat_id, 'audio'):
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
                    performer=(ytdl_data["uploader"]),
                    waveform='256',
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
    if video:
        await rkp.edit(f"Sending the video song ...")
        async with tbot.action(v_url.chat_id, 'video'):
         y = await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            attributes=[
                DocumentAttributeVideo(
                    duration=int(rip_data["duration"]),
                    w=800,
                    h=540,
             )
             ],
            caption=rip_data["title"],
        )
        try:
            os.system("rm -rf *.mp4")
            os.system("rm -rf *.webp")
            os.system("rm -rf *.jpg")
        except:
           pass
 except Exception as e:
    await v_url.reply(f'{e}')
