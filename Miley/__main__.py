import Miley.utils # pylint:disable=E0602
from Miley import TOKEN, bot

bot.start(bot_token=TOKEN)

bot.run_until_disconnected()
