from Evie.events import register

@register(pattern="^/sutest")
async def surest(event):
  if True:
   await event.reply("Test Success")
  else:
   await event.reply("test failed")
  
