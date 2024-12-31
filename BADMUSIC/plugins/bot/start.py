# Copyright (C) 2024 by Badhacker98@Github, < https://github.com/Badhacker98 >.
# Owner https://t.me/ll_BAD_MUNDA_ll

import asyncio
import time
import random

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS, START_IMG_URL
from strings import get_string
from BADMUSIC import Platform, app
from BADMUSIC.misc import SUDOERS, _boot_
from BADMUSIC.plugins.play.playlist import del_plist_msg
from BADMUSIC.plugins.sudo.sudoers import sudoers_list
from BADMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    get_assistant,
    get_lang,
    get_userss,
    is_banned_user,
    is_on_off,
    is_served_private_chat,
)
from BADMUSIC.utils.decorators.language import LanguageStart
from BADMUSIC.utils.formatters import get_readable_time
from BADMUSIC.utils.functions import MARKDOWN, WELCOMEHELP
from BADMUSIC.utils.inline import alive_panel, music_start_panel, start_pannel

from .help import paginate_modules

loop = asyncio.get_running_loop()

STICKER = [
    "CAACAgUAAx0CepnpNQABATUjZypavrymDoERINkF-M3u9JDQ6K8AAhoDAAIOnnlVpyrYiDnVgWYeBA",
]

@app.on_message(group=-1)
async def ban_new(client, message):
    user_id = (
        message.from_user.id if message.from_user and message.from_user.id else 777000
    )
    chat_name = message.chat.title if message.chat.title else ""
    if await is_banned_user(user_id):
        try:
            alert_message = "😳"
            BAN = await message.chat.ban_member(user_id)
            if BAN:
                await message.reply_text(alert_message)
        except:
            pass


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_comm(client, message: Message, _):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)
    await message.react("❤️")
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help", close=True)
            )
            if config.START_IMG_URL:
                return await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["help_1"],
                    reply_markup=keyboard,
                )
            else:
                return await message.reply_text(
                    text=_["help_1"],
                    reply_markup=keyboard,
                )
        # Additional handlers go here...
    else:
        try:
            out = music_start_panel(_)
            bad = await message.reply_text(f"**'ʜᴇʏ 💌'**")
            await bad.delete()
            bad = await message.reply_text(f"**'ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ 💞'**")
            await asyncio.sleep(0.1)
            await bad.delete()
            umm = await bad.reply_sticker(sticker=random.choice(STICKER))
            if message.chat.photo:
                userss_photo = await app.download_media(
                    message.chat.photo.big_file_id,
                )
            else:
                userss_photo = "assets/nodp.png"
            if userss_photo:
                chat_photo = userss_photo
            chat_photo = userss_photo if userss_photo else START_IMG_URL
        except AttributeError:
            chat_photo = "assets/nodp.png"
        await bad.delete()
        await message.reply_photo(
            photo=chat_photo,
            caption=f"**'{_['start_2'].format(message.from_user.mention, app.mention)}'**",
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"**'{message.from_user.mention} ʜᴀs sᴛᴀʀᴛᴇᴅ ʙᴏᴛ. \n\nᴜsᴇʀ ɪᴅ : {sender_id}\nᴜsᴇʀ ɴᴀᴍᴇ: {sender_name}'**",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def testbot(client, message: Message, _):
    try:
        chat_id = message.chat.id
        try:
            # Try downloading the group's photo
            groups_photo = await client.download_media(
                message.chat.photo.big_file_id, file_name=f"chatpp{chat_id}.png"
            )
            chat_photo = groups_photo if groups_photo else START_IMG_URL
        except AttributeError:
            # If there's no chat photo, use the default image
            chat_photo = START_IMG_URL

        # Get the alive panel and uptime
        out = alive_panel(_)
        uptime = int(time.time() - _boot_)

        # Send the response with the group photo or fallback to START_IMG_URL
        if chat_photo:
            await message.reply_photo(
                photo=chat_photo,
                caption=_["start_7"].format(client.mention, get_readable_time(uptime)),
                reply_markup=InlineKeyboardMarkup(out),
            )
        else:
            await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["start_7"].format(client.mention, get_readable_time(uptime)),
                reply_markup=InlineKeyboardMarkup(out),
            )

        # Add the chat to the served chat list
        return await add_served_chat(chat_id)

    except Exception as e:
        print(f"Error: {e}")


@app.on_message(filters.new_chat_members, group=3)
async def welcome(client, message: Message):
    chat_id = message.chat.id

    # Private bot mode check
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(chat_id):
            await message.reply_text(
                "**ᴛʜɪs ʙᴏᴛ's ᴘʀɪᴠᴀᴛᴇ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ. ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs. ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ɪᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ, ᴀsᴋ ᴍʏ ᴏᴡɴᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇ ʏᴏᴜʀ ᴄʜᴀᴛ.**"
            )
            return await client.leave_chat(chat_id)
    else:
        await add_served_chat(chat_id)

    # Handle new chat members
    for member in message.new_chat_members:
        try:
            language = await get_lang(chat_id)
            _ = get_string(language)

            # If bot itself joins the chat
            if member.id == client.id:
                try:
                    groups_photo = await client.download_media(
                        message.chat.photo.big_file_id, file_name=f"chatpp{chat_id}.png"
                    )
                    chat_photo = groups_photo if groups_photo else START_IMG_URL
                except AttributeError:
                    chat_photo = START_IMG_URL

                userbot = await get_assistant(chat_id)
                out = start_pannel(_)
                await message.reply_photo(
                    photo=chat_photo,
                    caption=_["start_2"],
                    reply_markup=InlineKeyboardMarkup(out),
                )

            # Handle owner joining
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_3"].format(client.mention, member.mention)
                )

            # Handle SUDOERS joining
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_4"].format(client.mention, member.mention)
                )
            return

        except Exception as e:
            print(f"Error: {e}")
            return


@app.on_callback_query(filters.regex("go_to_start"))
@LanguageStart
async def go_to_home(client, callback_query: CallbackQuery, _):
    out = music_start_panel(_)
    await callback_query.message.edit_text(
        text=_["start_2"].format(callback_query.message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )
    
