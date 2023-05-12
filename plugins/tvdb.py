import os
import re
import json
import requests
import pyrogram
import tvdb_api

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import BadRequest
from dotenv import load_dotenv
from tvdb_api import Tvdb, tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound, tvdb_episodenotfound, tvdb_attributenotfound

tvdb = Tvdb(apikey="fe9c05b0-2099-4c03-b0dd-91ee77dfa192")


# Function to retrieve TV show information and landscape poster
@Client.on_message(filters.command("tv") & filters.private)
async def tv(client, message):
    try:
        show_name = message.text.split(" ", 1)[1]
        show = tvdb[show_name]
        msg = f"**{show['seriesname']}**\n\n"
        for season in show:
            msg += f"<b>Season {season}: </b>\n"
            for episode in show[season]:
                msg += f"<code>{episode}: </code>{show[season][episode]['episodename']}\n"
            msg += "\n"
        await message.reply_text(msg)
    except tvdb_shownotfound:
        await message.reply_text(f"TV Show not found!")
    except tvdb_seasonnotfound:
        await message.reply_text(f"Season not found!")
    except tvdb_episodenotfound:
        await message.reply_text(f"Episode not found!")
    except tvdb_attributenotfound:
        await message.reply_text(f"Attribute not found!")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Function to check if message is a TV show name
def is_tvshow(message_text):
    print(f"Checking if '{message_text}' is a TV show name")
    # Use regular expression to match TV show names
    regex = r'\b([Tt][Vv]\s*[Ss]\d{2}([Ee]?\d{2})*)|([Tt][Vv]\s*[Ss]\d{1,2}\s*[Ee]\d{1,2})|([Tt][Vv]\s*series)\b'
    return re.search(regex, message_text)

# on_message function to handle incoming messages
@Client.on_message(filters.command('series'))
async def showid(client, message):
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
               

