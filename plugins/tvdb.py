import re
from typing import Tuple, List
from tvdb_api import Tvdb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

# Initialize TVDB API with your API key
t = Tvdb(apikey="fe9c05b0-2099-4c03-b0dd-91ee77dfa192")


@Client.on_message(filters.command("tv"))
def tv_info(client, message):
    # Split the message to retrieve the TV show name
    command, *show_name = message.text.split(" ")
    show_name = " ".join(show_name)
    
    # Search TV show based on the provided name
    try:
        results = t.search(show_name)
    except:
        message.reply("An error occurred while searching for the TV show.")
        return
    
    # If there is no matching TV show, inform the user
    if not results:
        message.reply("No TV shows found with that name.")
        return
    
    # Retrieve the first search result
    result = results[0]
    
    # Retrieve the TV show ID and full series name
    show_id = result["id"]
    series_name = result["seriesName"]
    
    # Retrieve the TV show information based on the ID
    try:
        show_info = t[show_id]
    except:
        message.reply("An error occurred while retrieving TV show information.")
        return
    
    # Retrieve the TV show overview
    overview = show_info["overview"]
    
    # Retrieve the TV show banner image
    banner_url = show_info["banner"]
    
    # Retrieve the TV show genres
    genres = show_info["genre"]
    
    # Generate a list of clickable inline buttons for each season
    buttons = []
    for season_num in show_info:
        # If it's not a season dictionary, skip it
        if not isinstance(show_info[season_num], dict):
            continue
        
        # Extract the season number from the dictionary
        season = show_info[season_num]["seasonNumber"]
        
        # Append the season button to the list of buttons
        button = InlineKeyboardButton(
            text=f"Season {season}",
            callback_data=f"tv|{show_id}|{season}"
        )
        buttons.append(button)
    
    # Create a markup object for the inline keyboard
    markup = InlineKeyboardMarkup([buttons])
    
    # Construct the message to be sent
    msg = f"<b>{series_name}</b>\n\n"
    msg += f"<i>Genres:</i> {genres}\n\n"
    msg += f"{overview}"
    
    # Send the message with the inline keyboard markup and the banner image
    try:
        message.reply_photo(
            photo=banner_url,
            caption=msg,
            reply_markup=markup,
            parse_mode="html"
        )
    except BadRequest:
        # If the banner is not available, send the message without the image
        message.reply_text(
            text=msg,
            reply_markup=markup,
            parse_mode="html"
        )


@Client.on_callback_query(filters.regex("^tv\|\d+\|\d+$"))
def tv_season_info(client, callback_query):
    # Extract the TV show ID and season number from the callback data
    _, show_id, season_num = callback_query.data.split("|")
    
    # Retrieve the season information based on the provided TV show ID and season number
    try:
        season_info = t[int(show_id)][int(season_num)]
    except:
        callback_query.answer("An error occurred while retrieving season information.")
       
