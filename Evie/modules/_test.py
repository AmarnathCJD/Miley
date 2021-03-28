from Evie.events import register

@register(pattern="^/surest")
async def surest(event):
  if SUDO == True:
   await event.reply("Test Success")
  else:
   await event.reply("test failed")
  
