from Miley import bot, TOKEN
import Miley.events  # pylint:disable=E0602

bot.start(bot_token=TOKEN)

bot.run_until_disconnected()
