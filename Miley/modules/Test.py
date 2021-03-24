from Miley.events import register

@register(pattern="^/pin")
async def ok(event):
    await event.reply('test ok, bot alive')
