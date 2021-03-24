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
