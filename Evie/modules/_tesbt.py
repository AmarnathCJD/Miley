from Evie.events import register
from Evie.modules._dev import sudo

@register(pattern="^/py")
async def gay(event):
 k = event.sender_id
 if sudo(k):
   await event.reply("Sudo Spotted yEah")
