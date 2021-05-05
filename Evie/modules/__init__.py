from Evie import tbot, MONGO_DB_URI, BOT_ID
from telethon import functions, types, events
from pymongo import MongoClient
import random, time, asyncio
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from Evie.modules.sql.elevated_sql import SUDO_USERS as su
from captcha.image import ImageCaptcha

#Setup SUDO
SUDO_USERS = []
ELITES = []
Elevated = su
for x in Elevated:
    SUDO_USERS.append(x)

#mongodb
client = MongoClient(MONGO_DB_URI)
db = client["evie"]

async def get_user(event):
    args = event.pattern_match.group(1).split(" ", 1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        extra = None
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return

    return user_obj, extra

async def can_promote_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.add_admins
    )

async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )

async def can_ban_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

async def is_admin(chat_id, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod

number_list = ['0','1','2','3','4','5','6','7','8','9']
alphabet_lowercase = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
alphabet_uppercase = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def gen_captcha(captcha_string_size=10):
    captcha_string_list = []
    base_char = alphabet_lowercase + alphabet_uppercase + number_list
    for i in range(captcha_string_size):
        char = random.choice(base_char)
        captcha_string_list.append(char)
    captcha_string = '' 
    for item in captcha_string_list:
        captcha_string += str(item)
    return captcha_string

def gen_img_captcha(captcha_string_size=6):
 image_captcha = ImageCaptcha(width = 1250, height = 800, font_sizes=[350, 210, 300])
 text = gen_captcha(captcha_string_size)
 image_file = "./"+ "captcha.png"
 image_captcha.write(text, image_file)
 
async def ban_user(chat_id, user_id):
 out = True
 try:
    await tbot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=None, view_messages=True)))
 except:
    pass
    out = False
 return out

async def unban_user(chat_id, user_id):
 out = True
 try:
    await tbot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=None, view_messages=False)))
 except:
    pass
    out = False
 return out


async def kick_user(chat_id, user_id):
 out = True
 try:
    await tbot.kick_participant(chat_id, user_id)
 except:
    pass
    out = False
 return out

async def mute_user(chat_id, user_id):
 out = True
 try:
    await tbot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=None, send_messages=True)))
 except Exception as e:
    print(e)
    out = False
 return out

async def unmute_user(chat_id, user_id):
 out = True
 try:
    await tbot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=None, send_messages=False)))
 except Exception as e:
    print(e)
    out = False
 return out

async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await message.reply(f"Invalid time type specified. Expected m,h, or d, got: {unit}")
            return ""

        if unit == "m" or unit == "minute":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h" or unit == "hour":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d" or unit == "day":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            return
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return

async def get_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await message.reply(f"Invalid time type specified. Expected m,h, or d, got: {unit}")
            return ""

        if unit == "m" or unit == "minute":
            bantime = int(time_num) * 60
        elif unit == "h" or unit == "hour":
            bantime = int(time_num) * 60 * 60
        elif unit == "d" or unit == "day":
            bantime = int(time_num) * 24 * 60 * 60
        else:
            return
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return    
    
async def tmute_user(chat_id, user_id, time=3600):
 out = True
 try:
    await tbot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=int(time), send_messages=True)))
 except:
    pass
    out = False
 return out

async def tban_user(chat_id, user_id, time=3600):
 out = True
 try:
    await tbot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=int(time), view_messages=True)))
 except:
    pass
    out = False
 return out


def Cquery(args):
    def decorator(func):
        tbot.add_event_handler(func, events.CallbackQuery(args))
        return func
    return decorator

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


async def kick_restricted_after_delay(delay, event, user_id):
    await asyncio.sleep(delay)
    k = await tbot.get_permissions(event.chat_id, user_id)
    if not k.is_banned:
      return
    await event.delete()
    await tbot.kick_participant(event.chat_id, user_id)

async def bot_ban(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=BOT_ID,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )
