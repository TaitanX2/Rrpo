import logging
import re
import os
import sys
import asyncio
import time
import random
from telethon import TelegramClient, events
import telethon.utils
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from asyncio import sleep
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChatAdminRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime
from config import Var
from telethon import Button

from time import sleep
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)



RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

logging.basicConfig(level=logging.INFO)

print("Starting.....")

Dil = TelegramClient('Dil', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)

SUDO_USERS = []
for x in Var.SUDO:
    SUDO_USERS.append(x)



'''
start_time = time.time()

def get_uptime():
    uptime_seconds = round(time.time() - start_time)
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
    uptime_days, uptime_hours = divmod(uptime_hours, 24)
    return f"{uptime_days}d {uptime_hours}h {uptime_minutes}m {uptime_seconds}s"
'''


EMOJIS = ["🥰", "❤️", "😁", "💋", "😱", "🤣", "😘", "❤️‍🔥", "👌", "🫡", "😍"]

@Dil.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    bot_info = await event.client.get_me()
    bot_name = bot_info.first_name
    first_name = event.sender.first_name
    user_id = event.sender_id  # Define user ID

    random_emoji = random.choice(EMOJIS)

    buttons = [
        [Button.url("➕ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝘁 ➕", "https://t.me/mucissss_bot?startgroup=true&admin=ban_users")]
    ]

    if user_id in SUDO_USERS:
        buttons.append([Button.url("🧠 𝗛𝗲𝗹𝗽 & 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 🧠", data="not_sudo")])
    else:
        buttons.append([Button.inline("🧠 𝗛𝗲𝗹𝗽 & 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 🧠", data="not_sudo")])

    await event.respond(
        f"➻ 𝗛𝗲𝘆, {first_name} 💗\n\n"
        "🥀 𝗜 𝗮𝗺 𝗮𝗻 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 & 𝗛𝗶𝗴𝗵-𝗤𝘂𝗮𝗹𝗶𝘁𝘆 𝗥𝗼𝗯𝗼𝘁.\n"
        "🌿 𝗜 𝗰𝗮𝗻 𝗵𝗲𝗹𝗽 𝘆𝗼𝘂 𝗺𝗮𝗻𝗮𝗴𝗲 𝘆𝗼𝘂𝗿 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗼𝗿 𝗴𝗿𝗼𝘂𝗽𝘀.\n\n"
        "🐬 𝗧𝗮𝗽 𝗼𝗻 ❥ 𝗛𝗲𝗹𝗽 & 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻\n"
        "🦋 𝗧𝗼 𝗲𝘅𝗽𝗹𝗼𝗿𝗲 𝗺𝘆 𝗺𝗼𝗱𝘂𝗹𝗲𝘀 & 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀.\n\n"
        "💐 𝗙𝗲𝗲𝗹 𝗳𝗿𝗲𝗲 𝘁𝗼 𝘂𝘀𝗲 𝗺𝗲 𝗮𝗻𝗱 𝘀𝗵𝗮𝗿𝗲 𝘄𝗶𝘁𝗵 𝘆𝗼𝘂𝗿 𝗳𝗿𝗶𝗲𝗻𝗱𝘀!",
        buttons=buttons,
        file='https://graph.org/file/8363b1024b533cf062e65-06257ce831d003ddab.jpg'
    )

    await event.client.send_reaction(event.chat_id, event.message.id, [random_emoji])


@Dil.on(events.CallbackQuery(data=b"not_sudo"))
async def not_sudo_callback(event):
    await event.answer("⚠️ You have not permission To See This.", show_alert=True)

@Dil.on(events.NewMessage(pattern="^/ping"))
async def ping(e):
    start = datetime.now()
    text = "Pong!"
    event = await e.reply(text, parse_mode=None, link_preview=None)
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"**I'm On** \n\n __Pong__ !! `{ms}` ms")


@Dil.on(events.NewMessage(pattern="^/kickall"))
async def kickall(event):
    if not event.is_group:
        Reply = f"Noob !! Use This Cmd in Group."
        await event.reply(Reply)
    else:
        await event.delete()
        Ven = await event.get_chat()
        Venomop = await event.client.get_me()
        admin = Ven.admin_rights
        creator = Ven.creator
        if not admin and not creator:
            return await event.reply("I Don't have sufficient Rights !!")
        Sagar = await Dil.send_message(event.chat_id, "**Hello !! I'm Alive**")
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        all = 0
        kimk = 0
        async for user in event.client.iter_participants(event.chat_id):
            all += 1
            try:
                if user.id not in admins_id:
                    await event.client.kick_participant(event.chat_id, user.id)
                    kimk += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(str(e))
                await asyncio.sleep(0.1)
        await Sagar.edit(f"**Users Kicked Successfully ! \n\n Kicked:** `{kimk}` \n **Total:** `{all}`")


@Dil.on(events.NewMessage(pattern="^/banall"))
async def banall(event):
    if not event.is_group:
        Reply = f"Noob !! Use This Cmd in Group."
        await event.reply(Reply)
    else:
        await event.delete()
        Ven = await event.get_chat()
        Venomop = await event.client.get_me()
        admin = Ven.admin_rights
        creator = Ven.creator
        if not admin and not creator:
            return await event.reply("I Don't have sufficient Rights !!")
        Sagar = await Dil.send_message(event.chat_id, "**Hello !! I'm Alive**")
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        all = 0
        bann = 0
        async for user in event.client.iter_participants(event.chat_id):
            all += 1
            try:
                if user.id not in admins_id:
                    await event.client(EditBannedRequest(event.chat_id, user.id, RIGHTS))
                    bann += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(str(e))
                await asyncio.sleep(0.1)
        await Sagar.edit(f"**Users Banned Successfully ! \n\n Banned Users:** `{bann}` \n **Total Users:** `{all}`")


@Dil.on(events.NewMessage(pattern="^/unbanall"))
async def unban(event):
    if not event.is_group:
        Reply = f"Noob !! Use This Cmd in Group."
        await event.reply(Reply)
    else:
        msg = await event.reply("Searching Participant Lists.")
        p = 0
        async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await event.client(functions.channels.EditBannedRequest(event.chat_id, i, rights))
            except FloodWaitError as ex:
                print(f"sleeping for {ex.seconds} seconds")
                sleep(ex.seconds)
            except Exception as ex:
                await msg.edit(str(ex))
            else:
                p += 1
        await msg.edit("{}: {} unbanned".format(event.chat_id, p))


@Dil.on(events.NewMessage(pattern="^/leave"))
async def _(e):
    if e.sender_id in SUDO_USERS:
        dilxannu = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        if len(e.text) > 7:
            bc = dilxannu[0]
            bc = int(bc)
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None)
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("Successfully Left")
            except Exception as e:
                await event.edit(str(e))
        else:
            bc = e.chat_id
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None)
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("Successfully Left")
            except Exception as e:
                await event.edit(str(e))


@Dil.on(events.NewMessage(pattern="^/restart"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        text = "__Restarting__ !!!"
        await e.reply(text, parse_mode=None, link_preview=None)
        try:
            await Dil.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()

print("\n\n")
print("Your Ban All Bot Deployed Successfully ✅")

Dil.run_until_disconnected()
