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
tmdb.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NTU1MzM1Zjg2OGVkNWJjZTAzYTU3YzM1ZmE5ZGExOSIsInN1YiI6IjYxNzkwYWM2NzBiNDQ0MDAyYmFiZmMxNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.R4Pa-9YfC1sGlc2FEy1J2AvAgiCDJ3YBmxADCp-LjF8"
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

        # Print debug information
        print(f"TV Show Name: {show_name}")
        print(f"TMDB Search Results: {search_results}")
        print(f"Poster URL: {poster_url}")
        print(f"Response: {response}")


@Client.on_callback_query()
def callback_handler(client: Client, callback_query: CallbackQuery):
    callback_data = callback_query.data

    if callback_data.startswith("cast:"):
        tv_show_id = callback_data.split(":")[1]
        try:
            # Retrieve the TV show cast using the TMDB API
            cast = tmdb.get_tv_show_cast(tv_show_id)
            cast_info = "\n".join([f"{actor['name']} as {actor['character']}" for actor in cast])
            # Send the cast information as a message
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=f"Cast:\n{cast_info}"
            )

            # Print debug information
            print(f"TV Show ID (Cast): {tv_show_id}")
            print(f"TMDB Cast: {cast}")
            print(f"Cast Info: {cast_info}")

        except Exception as e:
            # Handle the TMDB API error
            error_message = f"Failed to retrieve cast information: {str(e)}"
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=error_message
            )

            # Print debug information
            print(f"Cast Error: {str(e)}")


    elif callback_data.startswith("episodes:"):
        tv_show_id = callback_data.split(":")[1]
        try:
            # Retrieve the TV show episodes using the TMDB API
            episodes = tmdb.get_tv_show_episodes(tv_show_id)
            episode_info = "\n".join([f"Season {episode['season_number']}, Episode {episode['episode_number']}: {episode['name']}" for episode in episodes])
            # Send the episode information as a message
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=f"Episodes:\n{episode_info}"
            )

            # Print debug information
            print(f"TV Show ID (Episodes): {tv_show_id}")
            print(f"TMDB Episodes: {episodes}")
            print(f"Episode Info: {episode_info}")

        except Exception as e:
            # Handle the TMDB API error
            error_message = f"Failed to retrieve episode information: {str(e)}"
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=error_message
            )

            # Print debug information
            print(f"Episode Error: {str(e)}")


    elif callback_data.startswith("similar:"):
        tv_show_id = callback_data.split(":")[1]
        try:
            # Retrieve similar TV shows using the TMDB API
            similar_shows = tmdb.get_similar_tv_shows(tv_show_id)
            similar_info = "\n".join([show['name'] for show in similar_shows])
            # Send the similar shows information as a message
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=f"Similar Shows:\n{similar_info}"
            )

            # Print debug information
            print(f"TV Show ID (Similar): {tv_show_id}")
            print(f"TMDB Similar Shows: {similar_shows}")
            print(f"Similar Info: {similar_info}")

        except Exception as e:
            # Handle the TMDB API error
            error_message = f"Failed to retrieve similar shows information: {str(e)}"
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=error_message
            )

            # Print debug information
            print(f"Similar Error: {str(e)}")


    elif callback_data.startswith("info:"):
        tv_show_id = callback_data.split(":")[1]
        try:
            # Retrieve additional information about the TV show using the TMDB API
            tv_show = tmdb.get_tv_show_details(tv_show_id)
            info = f"Network: {tv_show['networks'][0]['name']}\n" if tv_show['networks'] else ""
            info += f"Streaming Service: {tv_show['streaming_info']['name']}\n" if tv_show['streaming_info'] else ""
            info += f"Website: {tv_show['homepage']}\n" if tv_show['homepage'] else ""
            # Send the additional information as a message
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=f"Additional Information:\n{info}"
            )

            # Print debug information
            print(f"TV Show ID (Info): {tv_show_id}")
            print(f"TMDB TV Show: {tv_show}")
            print(f"Additional Info: {info}")

        except Exception as e:
            # Handle the TMDB API error
            error_message = f"Failed to retrieve additional information: {str(e)}"
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text=error_message
            )

            # Print debug information
            print(f"Info Error: {str(e)}")

def show_overview_inline_keyboard(tv_show_id):
    keyboard = [
        [
            InlineKeyboardButton("Cast", callback_data="cast:{tv_show_id"),
            InlineKeyboardButton("Episodes", callback_data=f"episodes:{tv_show_id}")
        ],
        [
            InlineKeyboardButton("Similar Shows", callback_data=f"similar:{tv_show_id}"),
            InlineKeyboardButton("More Info", callback_data=f"info:{tv_show_id}")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)
