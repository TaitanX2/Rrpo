import os
import sys
import asyncio
from telethon import events, functions
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsKicked, ChatBannedRights
from telethon.errors import FloodWaitError

# Replace 'Dil' with your actual bot client
@Dil.on(events.NewMessage(pattern="^/banall$"))
async def banall(event):
    if not event.is_group:
        return await event.reply("❌ This command only works in groups.")

    chat = await event.get_chat()
    me = await event.client.get_me()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await event.reply("❌ I don't have sufficient admin rights!")

    msg = await event.respond("🚀 **Mass banning users... Please wait!**")

    admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    admin_ids = {admin.id for admin in admins}

    RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

    async def ban_user(user_id):
        try:
            await event.client(functions.channels.EditBannedRequest(event.chat_id, user_id, RIGHTS))
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as ex:
            print(f"Error banning {user_id}: {ex}")

    ban_tasks = []
    count = 0

    async for user in event.client.iter_participants(event.chat_id, aggressive=True):
        if user.id not in admin_ids:
            ban_tasks.append(asyncio.create_task(ban_user(user.id)))
            count += 1

            if count % 500 == 0:
                await asyncio.gather(*ban_tasks)
                ban_tasks.clear()
                await asyncio.sleep(0.2)

    if ban_tasks:
        await asyncio.gather(*ban_tasks)

    await msg.edit(f"✅ **Banned {count} users successfully!**")


@Dil.on(events.NewMessage(pattern="^/unbanall$"))
async def unban(event):
    if not event.is_group:
        return await event.reply("❌ This command only works in groups.")

    msg = await event.reply("🔄 Searching for banned users...")

    p = 0
    RIGHTS = ChatBannedRights(until_date=0, view_messages=False)

    async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
        try:
            await event.client(functions.channels.EditBannedRequest(event.chat_id, i.id, RIGHTS))
        except FloodWaitError as ex:
            await asyncio.sleep(ex.seconds)
        except Exception as ex:
            print(f"Error unbanning {i.id}: {ex}")
        else:
            p += 1

    await msg.edit(f"✅ Unbanned {p} users successfully!")


@Dil.on(events.NewMessage(pattern="^/leave$"))
async def leave(e):
    if e.sender_id in SUDO_USERS:
        dilxannu = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        chat_id = int(dilxannu[0]) if len(e.text) > 7 else e.chat_id

        msg = await e.reply("🚪 Leaving group/channel...")
        try:
            await e.client(functions.channels.LeaveChannelRequest(chat_id))
            await msg.edit("✅ Successfully Left!")
        except Exception as ex:
            await msg.edit(f"❌ Error: {ex}")


@Dil.on(events.NewMessage(pattern="^/restart$"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        await e.reply("🔄 **Restarting bot...**")
        try:
            await Dil.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        sys.exit()


print("✅ Your Ban All Bot Deployed Successfully!")
Dil.run_until_disconnected()
