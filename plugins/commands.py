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


tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

from pyrogram.types import InputMediaPhoto


# Handler for text messages
@Client.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
    else:
        tv_show = search_results[0]
        poster_url = f"https://image.tmdb.org/t/p/w1280{tv_show.backdrop_path}"
        response = f"Title: {tv_show.name}\n"
        response += f"Overview: {tv_show.overview}\n"
        response += f"First Air Date: {tv_show.first_air_date}\n"
        response += f"Vote Average: {tv_show.vote_average}\n"
        response += f"Poster: [Poster]({poster_url})\n"

        # Generate inline keyboard
        inline_keyboard = show_overview_inline_keyboard(tv_show.id)
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=response,
            reply_markup=inline_keyboard
        )

@Client.on_callback_query()
def callback_handler(client, callback_query):
    callback_data = callback_query.data
    if callback_data.startswith("cast:"):
        tv_show_id = callback_data.split(":")[1]
        cast = tv.credits(tv_show_id).cast
        cast_info = "\n".join([f"{actor.name} as {actor.character}" for actor in cast])
        client.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"Cast:\n{cast_info}"
        )
        pass
    elif callback_data.startswith("episodes:"):
        tv_show_id = callback_data.split(":")[1]
        episodes = tv.seasons(tv_show_id)
        episode_info = "\n".join([f"Season {episode.season_number}, Episode {episode.episode_number}: {episode.name}" for episode in episodes])
        client.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"Episodes:\n{episode_info}"
        )
        pass
    elif callback_data.startswith("similar:"):
        tv_show_id = callback_data.split(":")[1]
        similar_shows = tv.similar(tv_show_id)
        similar_info = "\n".join([show.name for show in similar_shows])
        client.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"Similar Shows:\n{similar_info}"
        )
        pass
    elif callback_data.startswith("info:"):
        tv_show_id = callback_data.split(":")[1]
        tv_show = tv.details(tv_show_id)
        info = f"Network: {tv_show.networks[0].name}\n" if tv_show.networks else ""
        info += f"Streaming Service: {tv_show.streaming_info.get('name', '')}\n" if tv_show.streaming_info else ""
        info += f"Website: {tv_show.homepage}\n" if tv_show.homepage else ""
        info += f"Quotes: {tv_show.quotes[0].quote}\n" if tv_show.quotes else ""
        info += f"Trivia: {tv_show.trivia[0].text}\n" if tv_show.trivia else ""
        info += f"Opinions: {tv_show.opinions[0].opinion}\n" if tv_show.opinions else ""
        client.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"Additional Information:\n{info}"
        )

def show_overview_inline_keyboard(tv_show_id):
    keyboard = [
        [
            InlineKeyboardButton("Cast", callback_data=f"cast:{tv_show_id}"),
            InlineKeyboardButton("Episodes", callback_data=f"episodes:{tv_show_id}")
        ],
        [
            InlineKeyboardButton("Similar Shows", callback_data=f"similar:{tv_show_id}"),
            InlineKeyboardButton("More Info", callback_data=f"info:{tv_show_id}")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)
