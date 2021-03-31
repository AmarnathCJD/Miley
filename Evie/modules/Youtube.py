from youtubesearchpython import VideosSearch
from Evie import tbot
from html import unescape
import os
from telethon import types
from telethon.tl import functions
from Evie.events import register

from telethon import events


@tbot.on(events.InlineQuery(pattern=r"yt (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    k = event.pattern_match.group(1)
    if ":" in k:
         testinput,evlin = event.pattern_match.group(1).split(";")
    else:
         testinput = event.pattern_match.group(1)
         evlin = 5
    urllib.parse.quote_plus(testinput)
    lund = event.sender_id
    if lund == lund:
        results = []
        search = SearchVideos(f"{testinput}", offset=1, mode="dict", max_results=int(evlin))
        mi = search.result()
        moi = mi["search_result"]
        if search == None:
            resultm = builder.article(
                title="No Results.",
                description="Try Again With correct Spelling",
                text="**No Matching Found**",
                buttons=[
                    [Button.switch_inline("Search Again", query="yt ", same_peer=True)],
                ],
            )
            await event.answer([resultm])
            return
        for mio in moi:
            mo = mio["link"]
            thum = mio["title"]
            proboyx = mio["id"]
            thums = mio["channel"]
            td = mio["duration"]
            tw = mio["views"]
            kekme = f"https://img.youtube.com/vi/{proboyx}/hqdefault.jpg"
            okayz = f"**Title :** `{thum}` \n**Link :** {mo} \n**Channel :** `{thums}` \n**Views :** `{tw}` \n**Duration :** `{td}`"
            hmmkek = f"Channel : {thums} \nDuration : {td} \nViews : {tw}"
            results.append(
                await event.builder.article(
                    title=thum,
                    description=hmmkek,
                    text=okayz,
                    buttons=Button.switch_inline(
                        "Search Again", query="yt ", same_peer=True
                    ),
                )
            )
        await event.answer(results)


@register(pattern="^/ytinfo (.*)")
async def yts_search(video_q):
    query = video_q.pattern_match.group(1)    
    videosSearch = VideosSearch(query, limit = 1)  
    h = videosSearch.result()
    title= (h['result'][0]['title'])
    ptime= (h['result'][0]['publishedTime'])
    dur= (h['result'][0]['duration'])
    views= (h['result'][0]['viewCount']['short'])
    des= (h['result'][0]['descriptionSnippet'][0]['text'])
    chn= (h['result'][0]['channel']['name'])
    chnl= (h['result'][0]['channel']['link'])
    vlink= (h['result'][0]['link'])
    final = f"""**Extracted information from youtube**:
**Title**: `{title}`
**Published Time**: `{ptime}`
**Duration**: `{dur}`
**Views**: `{views}`
**Description**: `{des}`
**Channel Name**: `{chn}`
**Channel Link**: `{chnl}`
**Video Link**: `{vlink}`
"""
    await video_q.reply(final)

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - Inline Youtube Search
**Syntax:** @MissEvie_Robot yt <query>:<max results(optional)>
 - /ytinfo <video link>: Returns information about the youtube video
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
