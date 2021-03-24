from Miley import CMD_LIST, CMD_HELP, tbot
FUN_LIST = None
import io
import re
from math import ceil

from telethon import custom, events, Button

from Miley.events import register

from telethon import types
from telethon.tl import functions

from pymongo import MongoClient
from Miley import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
pagenumber = db.pagenumber



about = "**About Me**\n\nMy name is Miley, A group management bot who can take care of your groups with automated regular admin actions!\n\n**My Software Version:** 2.0.1\n**Telethon Version:** 1.21.1\n\n**My Developers:**\n• @RoseLoverX\n• @LegendX22\n• @Proboyx\n\nUpdates Channel: [Click Here](t.me/lunabotnews)\nSupport Chat: [Click Here](t.me/lunabotsupport)\n\nAnd finally thanks for Supporting me😘"
ad_caption = "Hey! I am Miley, here to help you manage your groups! I perform most of the admin functions and make your group automated!\n\nJoin @Lunabotnews for updates.\n@Lunabotsupport for help and support\n\nYou can checkout more about me via following buttons."
pm_caption = "Hey there! My name is Miley - I'm a Telethon based Bot Made to help you manage your groups!\n\nHit /help to find out more about me and unleash my full potential.\n\n"
pmt = "Hello there! I'm Miley\nI'm a Telethon Based group management bot\n with a Much More! Have a look\nat the following for an idea of some of \nthe things I can help you with.\n\nMain commands available:\n/start : Starts me, can be used to check i'm alive or not.\n/help : PM's you this message.\nExplore My Commands🙃."
@register(pattern="^/start$")
async def start(event):

    if not event.is_group:
        await tbot.send_message(
            event.chat_id,
            pm_caption,
            buttons=[
                [
                    Button.inline("Advanced", data="soon"),
                    Button.inline("Commands", data="help_menu"),
                ],
                  [
                    Button.url(
                        "Add Me To Your Group!", "t.me/missmiley_robot?startgroup=true"
                    ),
                ],
            ],
        )
    else:
        await event.reply("Heya Luna Here!,\nHow Can I Help Ya.")

@tbot.on(events.CallbackQuery(pattern=r"reopen_again"))
async def reopen_again(event):
    if not event.is_group:
        await event.edit(
            pm_caption,
            buttons=[
                [
                    Button.inline("Advanced", data="soon"),
                    Button.inline("Commands", data="help_menu"),
                ],
                  [
                    Button.url(
                        "Add Me To Your Group!", "t.me/missmiley_robot?startgroup=true"
                    ),
                ],
            ],
        )
    else:
        pass


@register(pattern="^/help$")
async def help(event):
    if not event.is_group:
        buttons = paginate_help(event, 0, CMD_LIST, "helpme")
        await event.reply(pmt, buttons=buttons)
    else:
        await event.reply(
            "Contact me in PM for help!",
            buttons=[[Button.url("Click me for help!", "t.me/missmiley_robot?start=help")]],
        )

@tbot.on(events.CallbackQuery(pattern=r"help_menu"))
async def help_menu(event):
    buttons = paginate_help(event, 0, CMD_LIST, "helpme")
    await event.edit(pmt, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"soon"))
async def soon(event):
    buttons=[[Button.inline("About Me", data="about_me"), Button.inline("Commands", data="help_menu"),],[Button.inline("Go Back", data="reopen_again"),],]
    await event.edit(ad_caption, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"about_me"))
async def soon(event):
    buttons=[Button.inline("Go Back", data="soon"),]
    await event.edit(about, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern=r"fun_help"))
async def fun_help(event):
    buttons = nood_page(event, 0, FUN_LIST, "helpme")
    await event.edit(pmt, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(rb"helpme_next\((.+?)\)")))
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = paginate_help(event, current_page_number + 1, CMD_LIST, "helpme")
    await event.edit(buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(rb"helpme_prev\((.+?)\)")))
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = paginate_help(event, current_page_number - 1, CMD_LIST, "helpme")
    await event.edit(buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"us_plugin_(.*)")))
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = ""
    # By @RoseLoverX

    for i in CMD_LIST[plugin_name]:
        plugin = plugin_name.replace("_", " ")
        emoji = plugin_name.split("_")[0]
        output = str(CMD_HELP[plugin][1])
        help_string = f"Here is the help for **{emoji}**:\n" + output

    if help_string is None:
        pass  # stuck on click
    else:
        reply_pop_up_alert = help_string
    try:
        await event.edit(
            reply_pop_up_alert, buttons=[
                [Button.inline("Back", data="go_back")]]
        )
    except BaseException:
        pass

@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(rb"helpme_lel\((.+?)\)")))
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = paginate_help(event, current_page_number + 1, FUN_LIST, "helpme")
    await event.edit(buttons=buttons)

@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(rb"helpme_ull\((.+?)\)")))
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = paginate_help(event, current_page_number - 1, FUN_LIST, "helpme")
    await event.edit(buttons=buttons)

@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"help_plugin_(.*)")))
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = ""
    # By @RoseLoverX

    for i in FUN_LIST[plugin_name]:
        plugin = plugin_name.replace("_", " ")
        emoji = plugin_name.split("_")[0]
        output = str(CMD_HELP[plugin][1])
        help_string = f"Here is the help for **{emoji}**:\n" + output

    if help_string is None:
        pass  # stuck on click
    else:
        reply_pop_up_alert = help_string
    try:
        await event.edit(
            reply_pop_up_alert, buttons=[
                [Button.inline("Back", data="fun_back")]]
        )
    except BaseException:
        pass

@tbot.on(events.CallbackQuery(pattern=r"go_back"))
async def go_back(event):
    c = pagenumber.find_one({"id": event.sender_id})
    number = c["page"]
    # print (number)
    buttons = paginate_help(event, number, CMD_LIST, "helpme")
    await event.edit(pm_caption, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"fun_back"))
async def go_back(event):
    c = pagenumber.find_one({"id": event.sender_id})
    number = c["page"]
    # print (number)
    buttons = nood_page(event, number, FUN_LIST, "helpme")
    await event.edit(pmt, buttons=buttons)

def get_page(id):
    return pagenumber.find_one({"id": id})


def paginate_help(event, page_number, loaded_plugins, prefix):
    number_of_rows = 15
    number_of_cols = 3

    to_check = get_page(id=event.sender_id)

    if not to_check:
        pagenumber.insert_one({"id": event.sender_id, "page": page_number})

    else:
        pagenumber.update_one(
            {
                "_id": to_check["_id"],
                "id": to_check["id"],
                "page": to_check["page"],
            },
            {"$set": {"page": page_number}},
        )

    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{}".format(x.replace("_", " ")), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols], modules[2::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "Go Back", data="reopen_again"
                ),
                custom.Button.inline(
                    "Advanced Commands", data="fun_help"
                ),
            )
        ]
    return pairs

def nood_page(event, page_number, loaded_plugins, prefix):
    number_of_rows = 15
    number_of_cols = 3

    to_check = get_page(id=event.sender_id)

    if not to_check:
        pagenumber.insert_one({"id": event.sender_id, "page": page_number})

    else:
        pagenumber.update_one(
            {
                "_id": to_check["_id"],
                "id": to_check["id"],
                "page": to_check["page"],
            },
            {"$set": {"page": page_number}},
        )

    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{}".format(x.replace("_", " ")), data="help_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols], modules[2::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "Go Back", data="help_menu"
                ),
            )
        ]
    return pairs
