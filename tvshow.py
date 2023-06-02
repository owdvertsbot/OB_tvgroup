import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = os.environ.get("9555335f868ed5bce03a57c35fa9da19")
tv = TV()

# Handler for the '/start' command
@Client.on_message(filters.command("start1"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

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
        response = f"Title: {tv_show.name}\n"
        response += f"Overview: {tv_show.overview}\n"
        response += f"First Air Date: {tv_show.first_air_date}\n"
        response += f"Vote Average: {tv_show.vote_average}\n"

    client.send_message(chat_id=message.chat.id, text=response)

