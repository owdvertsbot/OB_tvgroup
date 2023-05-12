import os
import re
import math
import json
import time
import shutil
import requests
import pyrogram
import urllib.request
import urllib.parse
import tvdb_api

from datetime import datetime
from pyrogram import filters
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait, BadRequest
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

from script import Script
from info import SAVE_USER, PICS, THETVDB_API_KEY
from plugins.helpers import humanbytes
from database.filters_mdb import filter_stats
from database.users_mdb import add_user, find_user, all_users
from dotenv import load_dotenv


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


import urllib.request
from io import BytesIO

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    with urllib.request.urlopen("https://i.ibb.co/t8LdJwf/PICS.jpg") as url:
        image_data = url.read()
    buffer = BytesIO(image_data)
    await message.reply_photo(
        photo=buffer,
        caption=Script.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("ᴊᴏɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/OB_LINK")
            ],[
                InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_data"),
                InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about_data")
            ],[
                InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/OB_SERIESGROUP"),
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_data")
            ]]
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
        
t = Tvdb(apikey="fe9c05b0-2099-4c03-b0dd-91ee77dfa192") # doctest:+SKIP   
        
        
# Function to retrieve TV show information and landscape poster
def get_tvshow_info(name):
    try:
        url = f'https://api.thetvdb.com/search/series?name={name}'
        headers = {'Content-Type': 'application/json'}
        data = {'apikey': 'fe9c05b0-2099-4c03-b0dd-91ee77dfa192'}
        response = requests.post(url, headers=headers, data=json.dumps(data)).json()
        if response['data']:
            tv_show = response['data'][0]
            title = tv_show['seriesName']
            overview = tv_show['overview']
            poster_path = tv_show['banner']
            if poster_path:
                poster_url = f'https://www.thetvdb.com/banners/{poster_path}'
                return title, overview, poster_url
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Function to check if message is a TV show name
def is_tvshow(message_text):
    print(f"Checking if '{message_text}' is a TV show name")
    # Use regular expression to match TV show names
    regex = r'\b([Tt][Vv]\s*[Ss]\d{2}([Ee]?\d{2})*)|([Tt][Vv]\s*[Ss]\d{1,2}\s*[Ee]\d{1,2})|([Tt][Vv]\s*series)\b'
    return re.search(regex, message_text)

# on_message function to handle incoming messages
@Client.on_message(filters.text & filters.group & filters.bot)
async def on_message(client, message):
    # Check if message is a TV show name
    if is_tvshow(message.text):
        # Get TV show information and landscape poster
        tvshow_info = get_tvshow_info(message.text)
        print(f"TV Show Info: {tvshow_info}")
        if tvshow_info:
            title, overview, poster_url = tvshow_info
            # Send TV show information and landscape poster
            try:
                await message.reply_text(f'{title}\n\n{overview}')
                await message.reply_photo(photo=poster_url)
            except pyrogram.errors.exceptions.bad_request_400.PhotoInvalidDimensions:
                await message.reply_text(f"{title}\n\n{overview}\n\nSorry, I could not send the poster because it's dimensions are invalid.")
            except pyrogram.errors.exceptions.bad_request_400.PhotoContentUrlEmpty:
                await message.reply_text(f"{title}\n\n{overview}\n\nSorry, I could not send the poster because the URL is empty.")
            except pyrogram.errors.exceptions.bad_request_400.PhotoIdInvalid:
                await message.reply_text(f"{title}\n\n{overview}\n\nSorry, I could not send the poster because the photo ID is invalid.")
            except pyrogram.errors.exceptions.bad_request_400.PhotoInvalid:
                await message.reply_text(f"{title}\n\n{overview}\n\nSorry, I could not send the poster because the photo is invalid.")
            except pyrogram.errors.exceptions.bad_request_400.PhotoContentUrlInvalid:
                await message.reply_text(f"{title}\n\n{overview}\n\nSorry, I could not send the poster because the URL is invalid.")
            except pyrogram.errors.exceptions.bad_request_400.PhotoRemoteFileInvalid:
                await message.reply_text('Error: Invalid photo file')

