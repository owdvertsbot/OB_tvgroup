import os
import math
import json
import time
import shutil
import urllib.request
import urllib.parse
import requests

from datetime import datetime
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from io import BytesIO
from tmdbv3api import TMDb, TV

from script import Script
from info import SAVE_USER, PICS
from database.filters_mdb import filter_stats
from database.users_mdb import add_user, find_user, all_users

@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        _id = ""
        _id += (
            "<b>➲ Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>➲ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
                "<b>➲ Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➲ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(
            _id,
            quote=True
        )


@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    with urllib.request.urlopen("https://i.ibb.co/t8LdJwf/PICS.jpg") as url:
        image_data = url.read()
    buffer = BytesIO(image_data)
    await message.reply_photo(
        photo=buffer,
        caption=Script.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴊᴏɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/OB_LINK")
                ],
                [
                    InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_data"),
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about_data")
                ],
                [
                    InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/OB_SERIESGROUP"),
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_data")
                ]
            ]
        ),
        parse_mode=enums.ParseMode.HTML,
        quote=True
    )

    if SAVE_USER == "yes":
        try:
            await add_user(
                str(message.from_user.id),
                str(message.from_user.username),
                str(message.from_user.first_name + " " + (message.from_user.last_name or "")),
                str(message.from_user.dc_id)
            )
        except:
            pass






