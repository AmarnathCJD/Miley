from Miley import ubot, tbot
from Miley.events import register


@register(pattern="^/nf")
async def acc(event):
 async with ubot.conversation("@UniqAccGenBot") as conv:
      await conv.send_message("/start")
      response = await conv.get_response()
      await response.click(0, 1)
      k = await conv.get_response()
      await event.reply(k)
