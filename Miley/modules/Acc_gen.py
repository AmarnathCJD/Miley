from Miley import ubot, tbot
from Miley.events import register


@register(pattern="^/nf")
async def acc(event):
 async with ubot.conversation("@UniqAccGenBot") as conv:
   try:
      await conv.send_message("/start")
      pro = await conv.get_response()
      await event.reply(pro.text)
      s = await pro.click(1)
      j = await s.get_response()
      await j.click(1)
   except Exception as e:
      await event.reply(e)
