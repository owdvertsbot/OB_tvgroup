import os
import urllib
from pyrogram import Client
from tmdbv3api import TMDb, TV


tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"

tv = TV()


def send_tv_show_details(bot, chat_id, tv_show_name):
    # Search for the TV show
    results = tv.search(tv_show_name)
    if not results:
        bot.send_message(chat_id, "TV show not found.")
        return

    tv_show = results[0]
    tv_show_id = tv_show.id

    # Get the details of the TV show
    tv_show_details = tv.get_tv_show_details(tv_show_id)

    # Download the poster image
    poster_path = tv_show_details.poster_path
    if poster_path:
        poster_url = tmdb.image_url + "w500" + poster_path
        poster_file_name = f"{tv_show_id}_poster.jpg"
        urllib.request.urlretrieve(poster_url, poster_file_name)

        # Send the TV show details and poster
        bot.send_photo(chat_id, photo=poster_file_name, caption=tv_show_details.overview)
    else:
        bot.send_message(chat_id, "Poster not available for this TV show.")
    
    # Clean up the downloaded poster file
    os.remove(poster_file_name)

    
def main():
    with app:
        @app.on_message()
        def handle_message(client, message):
            if message.text:
                # Extract the TV show name from the user's query
                tv_show_name = message.text

                # Send the TV show details to the user
                send_tv_show_details(client, message.chat.id, tv_show_name)
    
