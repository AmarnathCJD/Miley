from sys import argv, exit
from Evie import tbot, bot
from Evie import TOKEN

import Evie.events

try:
    tbot.start(bot_token=TOKEN)
    bot.start()
except Exception:
    print("Bot Token Invalid")
    exit(1)

if len(argv) not in (1, 3, 4):
    tbot.disconnect()
else:
    tbot.run_until_disconnected()

