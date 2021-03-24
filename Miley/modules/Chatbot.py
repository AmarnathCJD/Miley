
from Miley.events import register
@register(pattern="hi")
async def _(event):
   await event.reply('hi')
