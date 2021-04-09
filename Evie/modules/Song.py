from Evie import tbot
from Evie.events import register
import asyncio, wget, time, requests, os
from youtube_dl import YoutubeDL
from PIL import Image
from youtubesearchpython import SearchVideos
from telethon.tl.types import DocumentAttributeAudio

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

@register(pattern="^/dsong ?(.*)")
async def deezr(event):
    pablo = await event.reply("Searching For Song.....")
    sgname = event.pattern_match.group(1)
    if not sgname:
        await pablo.edit(
            "Please Give Me A Valid Input."
        )
        return
    link = f"https://api.deezer.com/search?q={sgname}&limit=1"
    dato = requests.get(url=link).json()
    match = dato.get("data")
    try:
        urlhp = match[0]
    except IndexError:
        await pablo.edit("Song Not Found. Try Searching Some Other Song")
        return
    urlp = urlhp.get("link")
    thumbs = urlhp["album"]["cover_big"]
    thum_f = wget.download(thumbs)
    polu = urlhp.get("artist")
    replo = urlp[29:]
    urlp = f"https://starkapis.herokuapp.com/deezer/{replo}"
    datto = requests.get(url=urlp).json()
    mus = datto.get("url")
    sname = f"{urlhp.get('title')}.mp3"
    doc = requests.get(mus)
    await pablo.edit("Downloading Song From Deezer!")
    with open(sname, "wb") as f:
        f.write(doc.content)
    c_time = time.time()
    audio=open(sname, "rb"),
    async with tbot.action(event.chat_id, 'audio'):
     await tbot.send_file(
        event.chat_id,
        audio,
        thumb=thum_f,
        supports_streaming=True,
        force_document=False,
        attributes=[
                DocumentAttributeAudio(
                    duration=int(urlhp.get("duration")),
                    title=str(urlhp.get("title")),
                    performer=str(polu.get("name")),
                    waveform='256',
                )],
         )
    
    await pablo.delete()


