from Miley.events import register
from Miley import StartTime, tbot, ubot
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



@register(pattern="^/(ping|ping@MissMiley_Robot)")
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

@register(pattern="^/bin (.*)")
async def alive(event):
      sender = await event.get_sender()
      fname = sender.first_name
      k = await event.reply("Wait for result")
      ok = event.pattern_match.group(1)
      async with ubot.conversation("@Carol5_bot") as bot_conv:
          await bot_conv.send_message(f"/bin {ok}")
          await asyncio.sleep(4)
          response = await bot_conv.get_response()
          res = response.text
          if "❌" in res:
               text = '🤬❌ INVALID BIN ❌🤬\n'
               text += f'Checked By **{fname}**'
               await k.edit(text)
          else:
               text = f'{res.splitlines()[0]}\n'
               text += f'{res.splitlines()[1]}\n'
               text += f'{res.splitlines()[2]}\n'
               text += f'{res.splitlines()[3]}\n'
               text += f'{res.splitlines()[4]}\n'
               text += f'{res.splitlines()[5]}\n'
               text += f'{res.splitlines()[6]}\n'
               text += f'Checked By **{fname}**'
               await k.edit(text)

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
      await (await inline_query(ubot, "@lybot", k))[0].click("@MissMiley_Robot")
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
      await (await inline_query(ubot, "@HowGayBot", k))[0].click("@MissMiley_Robot")
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
            await stt.edit("Error, Report at @Mileysupport")
            return
    namem = f"Song Name : {result.text.splitlines()[0]}\
        \n\nDetails : {result.text.splitlines()[2]}"
    await stt.edit(namem)
 except Exception as e:
      await event.reply(e)
