from googleapiclient.discovery import build
from youtubesearchpython import VideosSearch
from Evie import *
from html import unescape
import os
from telethon import types
from telethon.tl import functions
from Evie.events import register

from telethon import events


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


async def youtube_search(
    query, order="relevance", token=None, location=None, location_radius=None
):
    """ Do a YouTube search. """
    youtube = build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY, cache_discovery=False
    )
    search_response = (
        youtube.search()
        .list(
            q=query,
            type="video",
            pageToken=token,
            order=order,
            part="id,snippet",
            maxResults=10,
            location=location,
            locationRadius=location_radius,
        )
        .execute()
    )

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "KeyError, try again."
        return (nexttok, videos)


@register(pattern="^/yts (.*)")
async def yts_search(video_q):

    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if video_q.is_group:
        if await is_register_admin(video_q.input_chat, video_q.message.sender_id):
            pass
        elif video_q.chat_id == iid and video_q.sender_id == userss:
            pass
        else:
            return

    # For /yts command, do a YouTube search from Telegram.
    query = video_q.pattern_match.group(1)
    result = ""

    if not YOUTUBE_API_KEY:
        await video_q.reply(
            "`Error: YouTube API key missing! Add it to environment vars or config.env.`"
        )
        return

    c = await video_q.reply("```Processing...```")

    full_response = await youtube_search(query)
    videos_json = full_response[1]

    for video in videos_json:
        title = f"{unescape(video['snippet']['title'])}"
        link = f"https://youtu.be/{video['id']['videoId']}"
        result += f"{title}\n{link}\n\n"

    await c.edit(result)


@register(pattern="^/ytinfo (.*)")
async def yts_search(video_q):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if video_q.is_group:
        if await is_register_admin(video_q.input_chat, video_q.message.sender_id):
            pass
        elif video_q.chat_id == iid and video_q.sender_id == userss:
            pass
        else:
            return
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
    final = """**Extracted information from youtube**:
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
 - /yts <query>: Searches your query in youtube and returns results
 - /ytinfo <video link>: Returns information about the youtube video
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
