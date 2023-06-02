import os
import math
import json
import time
import shutil
import urllib.request
import urllib.parse

from datetime import datetime
from pyrogram import filters
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

from script import Script
from info import SAVE_USER, PICS
from plugins.helpers import humanbytes
from database.filters_mdb import filter_stats
from database.users_mdb import add_user, find_user, all_users
from tmdbv3api import TMDb
from tmdbv3api import TV

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
        
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()


Code Conversion Requested


User
text to code

ChatGPT
Certainly! Please provide the specific task or problem you would like me to help you with, along with any relevant details or requirements.





User
a code for telegram bot which can send information about a tv show python, pyrogram, tmdb

ChatGPT
Certainly! Here's an example code for a Telegram bot that can send information about a TV show using Python, Pyrogram, and the TMDB (The Movie Database) API:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = os.environ.get("TMDB_API_KEY")
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
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

# Start the bot
app.run()
Make sure you have the required dependencies (pyrogram, tmdbv3api) installed, and you have registered a bot and obtained the necessary API keys from Telegram and TMDB. You'll need to replace the placeholders for API_ID, API_HASH, BOT_TOKEN, and TMDB_API_KEY with your own values.

This code sets up a Telegram bot using Pyrogram, and it responds to the /start command by providing a welcome message. Whenever a user sends a text message, the bot searches for the TV show using the TMDB API and sends back information about the show if found.

Remember to handle exceptions and add any additional functionality or features you may require.





User
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
 ﻿Invalid API key: You must be granted a valid key.
﻿Traceback (most recent call last):
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/dispatcher.py", line 242, in handler_worker
﻿await self.loop.run_in_executor(
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/thread.py", line 58, in run
﻿result = self.fn(*self.args, **self.kwargs)
﻿File "/app/plugins/commands.py", line 115, in tv_show_info
﻿search_results = tv.search(show_name)
﻿File "/opt/venv/lib/python3.9/site-packages/tmdbv3api/objs/tv.py", line 59, in search
﻿return self._get_obj(
﻿File "/opt/venv/lib/python3.9/site-packages/tmdbv3api/tmdb.py", line 115, in _get_obj
﻿raise TMDbException(result["status_message"])
﻿tmdbv3api.exceptions.TMDbException: Invalid API key: You must be granted a valid key.

ChatGPT
The error message suggests that the provided TMDB API key is invalid. Make sure you have a valid TMDB API key and replace the line tmdb.api_key = os.environ.get("9555335f868ed5bce03a57c35fa9da19") with the actual API key.

Here's an updated version of the code with the corrected TMDB API key assignment:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
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

# Start the bot
app.run()
Make sure to replace the API_ID, API_HASH, and BOT_TOKEN placeholders with your own values as well.





User
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

    client.send_message(chat_id=message.chat.id, text=response) this code works fine , thanks . i need some more help the bot is not replying to the users message and the bot is not sending the poster, seasons, total episodes, runtime etc add these to the code and send the corrected code

ChatGPT
Certainly! Here's the updated code that includes additional information such as the poster, seasons, total episodes, and runtime:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
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
        response += f"Seasons: {tv_show.number_of_seasons}\n"
        response += f"Total Episodes: {tv_show.number_of_episodes}\n"
        response += f"Runtime: {tv_show.episode_run_time[0]} minutes\n"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show.poster_path}"
        response += f"Poster: {poster_url}"

    client.send_message(chat_id=message.chat.id, text=response)

# Start the bot
app.run()
This code includes the poster URL, seasons, total episodes, and runtime for the TV show. It fetches the poster URL using the poster_path returned by the TMDB API and constructs a URL to the poster image.

Please note that the code assumes that the episode runtime is available for the first episode. It uses the episode_run_time attribute, which is a list, to retrieve the runtime of the first episode (in minutes).

Remember to replace the API_ID, API_HASH, and BOT_TOKEN placeholders with your own values.





User
i need the Title, Overview, First Air Date, ...etc  as caption of the poster

ChatGPT
Certainly! To set the title, overview, first air date, and other details as the caption of the poster, you can use the send_photo method instead of send_message to send the poster as a photo with a caption. Here's the updated code:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
        client.send_message(chat_id=message.chat.id, text=response)
    else:
        tv_show = search_results[0]
        caption = f"Title: {tv_show.name}\n"
        caption += f"Overview: {tv_show.overview}\n"
        caption += f"First Air Date: {tv_show.first_air_date}\n"
        caption += f"Vote Average: {tv_show.vote_average}\n"
        caption += f"Seasons: {tv_show.number_of_seasons}\n"
        caption += f"Total Episodes: {tv_show.number_of_episodes}\n"
        caption += f"Runtime: {tv_show.episode_run_time[0]} minutes"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show.poster_path}"

        # Send the photo with caption
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown"
        )

# Start the bot
app.run()
In this updated version, the caption includes all the desired details, and the send_photo method is used to send the poster image with the caption.

Please note that parse_mode="Markdown" is used in the send_photo method to enable markdown formatting in the caption. You can remove it if you don't need markdown formatting.

Remember to replace the API_ID, API_HASH, and BOT_TOKEN placeholders with your own values.





User
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
        client.send_message(chat_id=message.chat.id, text=response)
    else:
        tv_show = search_results[0]
        caption = f"Title: {tv_show.name}\n"
        caption += f"Overview: {tv_show.overview}\n"
        caption += f"First Air Date: {tv_show.first_air_date}\n"
        caption += f"Vote Average: {tv_show.vote_average}\n"
        caption += f"Seasons: {tv_show.number_of_seasons}\n"
        caption += f"Total Episodes: {tv_show.number_of_episodes}\n"
        caption += f"Runtime: {tv_show.episode_run_time[0]} minutes"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show.poster_path}"

        # Send the photo with caption
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown"
        ) insted of sending the 'Overview'  add an option to see the 'Overview' in bot pm

ChatGPT
To provide an option to see the TV show overview in a private message (PM) with the bot, you can modify the code as follows:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
        client.send_message(chat_id=message.chat.id, text=response)
    else:
        tv_show = search_results[0]
        caption = f"Title: {tv_show.name}\n"
        caption += f"First Air Date: {tv_show.first_air_date}\n"
        caption += f"Vote Average: {tv_show.vote_average}\n"
        caption += f"Seasons: {tv_show.number_of_seasons}\n"
        caption += f"Total Episodes: {tv_show.number_of_episodes}\n"
        caption += f"Runtime: {tv_show.episode_run_time[0]} minutes"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show.poster_path}"

        # Send the photo with caption
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=show_overview_inline_keyboard(tv_show.id)
        )

# Handler for 'overview' command
@app.on_callback_query(filters.regex('^overview_'))
def show_overview(client, callback_query):
    # Extract the TV show ID from the callback data
    tv_show_id = int(callback_query.data.split('_')[1])

    # Retrieve the TV show using the TMDB API
    tv_show = tv.details(tv_show_id)

    # Send the overview as a private message to the user
    client.send_message(chat_id=callback_query.from_user.id, text=tv_show.overview)

def show_overview_inline_keyboard(tv_show_id):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text="Show Overview",
                callback_data=f"overview_{tv_show_id}"
            )
        ]]
    )

# Start the bot
app.run()
In this updated code, a new handler show_overview is added to handle the callback from the "Show Overview" inline button. When the button is clicked, it sends the TV show's overview as a private message to the user who clicked the button.

The show_overview_inline_keyboard function creates an inline keyboard markup with a single button for showing the overview. This function is called when sending the photo with caption,





User
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response) remove these and start sending from ' # Handler for text messages' part

ChatGPT
Certainly! Here's the code starting from the "Handler for text messages" part:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for text messages
@app.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
        client.send_message(chat_id=message.chat.id, text=response)
    else:
        tv_show = search_results[0]
        caption = f"Title: {tv_show.name}\n"
        caption += f"First Air Date: {tv_show.first_air_date}\n"
        caption += f"Vote Average: {tv_show.vote_average}\n"
        caption += f"Seasons: {tv_show.number_of_seasons}\n"
        caption += f"Total Episodes: {tv_show.number_of_episodes}\n"
        caption += f"Runtime: {tv_show.episode_run_time[0]} minutes"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show.poster_path}"

        # Send the photo with caption
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=show_overview_inline_keyboard(tv_show.id)
        )

# Handler for 'overview' command
@app.on_callback_query(filters.regex('^overview_'))
def show_overview(client, callback_query):
    # Extract the TV show ID from the callback data
    tv_show_id = int(callback_query.data.split('_')[1])

    # Retrieve the TV show using the TMDB API
    tv_show = tv.details(tv_show_id)

    # Send the overview as a private message to the user
    client.send_message(chat_id=callback_query.from_user.id, text=tv_show.overview)

def show_overview_inline_keyboard(tv_show_id):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text="Show Overview",
                callback_data=f"overview_{tv_show_id}"
            )
        ]]
    )

# Start the bot
app.run()




User

﻿'AsObj' object has no attribute 'number_of_seasons'
﻿Traceback (most recent call last):
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/dispatcher.py", line 242, in handler_worker
﻿await self.loop.run_in_executor(
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/thread.py", line 58, in run
﻿result = self.fn(*self.args, **self.kwargs)
﻿File "/app/plugins/commands.py", line 124, in tv_show_info
﻿caption += f"<b>Seasons:</b> {tv_show.number_of_seasons}\n"
﻿AttributeError: 'AsObj' object has no attribute 'number_of_seasons'

ChatGPT
It seems that the AsObj object returned by the TMDB API does not have the attribute number_of_seasons. This might be due to a recent change in the API response structure. To resolve this issue, you can modify the code to access the number_of_seasons attribute from the tv_show object directly. Here's the updated code:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()

# Handler for the '/start' command
@app.on_message(filters.command("start"))
def start_command(client, message):
    response = "Welcome to the TV Show Bot! Please enter the name of a TV show to get information about it."
    client.send_message(chat_id=message.chat.id, text=response)

# Handler for text messages
@app.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
        client.send_message(chat_id=message.chat.id, text=response)
    else:
        tv_show = search_results[0]
        tv_show_details = tv.details(tv_show.id)
        caption = f"Title: {tv_show_details.name}\n"
        caption += f"First Air Date: {tv_show_details.first_air_date}\n"
        caption += f"Vote Average: {tv_show_details.vote_average}\n"
        caption += f"Seasons: {tv_show_details.number_of_seasons}\n"
        caption += f"Total Episodes: {tv_show_details.number_of_episodes}\n"
        caption += f"Runtime: {tv_show_details.episode_run_time[0]} minutes"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show_details.poster_path}"

        # Send the photo with caption
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=show_overview_inline_keyboard(tv_show.id)
        )

# Handler for 'overview' command
@app.on_callback_query(filters.regex('^overview_'))
def show_overview(client, callback_query):
    # Extract the TV show ID from the callback data
    tv_show_id = int(callback_query.data.split('_')[1])

    # Retrieve the TV show using the TMDB API
    tv_show = tv.details(tv_show_id)

    # Send the overview as a private message to the user
    client.send_message(chat_id=callback_query.from_user.id, text=tv_show.overview)

def show_overview_inline_keyboard(tv_show_id):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text="Show Overview",
                callback_data=f"overview_{tv_show_id}"
            )
        ]]
    )

# Start the bot
app.run()
This code retrieves the TV show details again using the details method from the tv object to get the accurate information such as number_of_seasons.





User
Invalid parse mode "Markdown"
﻿Traceback (most recent call last):
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/dispatcher.py", line 242, in handler_worker
﻿await self.loop.run_in_executor(
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/thread.py", line 58, in run
﻿result = self.fn(*self.args, **self.kwargs)
﻿File "/app/plugins/commands.py", line 133, in tv_show_info
﻿client.send_photo(
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/sync.py", line 78, in async_to_sync_wrap
﻿return asyncio.run_coroutine_threadsafe(coroutine, main_loop).result()
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/_base.py", line 446, in result
﻿return self.__get_result()
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/_base.py", line 391, in __get_result
﻿raise self._exception
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/methods/messages/send_photo.py", line 187, in send_photo
﻿**await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/utils.py", line 354, in parse_text_entities
﻿text, entities = (await client.parser.parse(text, parse_mode)).values()
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/parser/parser.py", line 54, in parse
﻿raise ValueError(f'Invalid parse mode "{mode}"')
﻿ValueError: Invalid parse mode "Markdown"
﻿Invalid parse mode "Markdown"
﻿Traceback (most recent call last):
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/dispatcher.py", line 242, in handler_worker
﻿await self.loop.run_in_executor(
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/thread.py", line 58, in run
﻿result = self.fn(*self.args, **self.kwargs)
﻿File "/app/plugins/commands.py", line 133, in tv_show_info
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/sync.py", line 78, in async_to_sync_wrap
﻿return asyncio.run_coroutine_threadsafe(coroutine, main_loop).result()
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/_base.py", line 446, in result
﻿return self.__get_result()
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/_base.py", line 391, in __get_result
﻿client.send_photo(
﻿raise self._exception
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/methods/messages/send_photo.py", line 187, in send_photo
﻿**await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/utils.py", line 354, in parse_text_entities
﻿text, entities = (await client.parser.parse(text, parse_mode)).values()
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/parser/parser.py", line 54, in parse
﻿raise ValueError(f'Invalid parse mode "{mode}"')
﻿ValueError: Invalid parse mode "Markdown"
﻿list index out of range
﻿Traceback (most recent call last):
﻿File "/opt/venv/lib/python3.9/site-packages/pyrogram/dispatcher.py", line 242, in handler_worker
﻿await self.loop.run_in_executor(
﻿File "/root/.nix-profile/lib/python3.9/concurrent/futures/thread.py", line 58, in run
﻿result = self.fn(*self.args, **self.kwargs)
﻿File "/app/plugins/commands.py", line 127, in tv_show_info
﻿caption += f"Runtime: {tv_show_details.episode_run_time[0]} minutes"
﻿IndexError: list index out of range

ChatGPT
I apologize for the confusion. It appears that the Pyrogram library does not support the "Markdown" parse mode for captions when sending photos. To resolve this issue, you can remove the parse_mode="Markdown" argument from the send_photo method. Here's the updated code:

python
Copy code
import os
from pyrogram import Client, filters
from tmdbv3api import TMDb
from tmdbv3api import TV

# Set up the Pyrogram client
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("tv_show_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the TMDB API client
tmdb = TMDb()
tmdb.api_key = "9555335f868ed5bce03a57c35fa9da19"
tv = TV()


# Handler for text messages
@Client.on_message(filters.text)
def tv_show_info(client, message):
    show_name = message.text

    # Search for the TV show using the TMDB API
    search_results = tv.search(show_name)
    if len(search_results) == 0:
        response = "Sorry, I couldn't find any information about that TV show."
        client.send_message(chat_id=message.chat.id, text=response)
    else:
        tv_show = search_results[0]
        tv_show_details = tv.details(tv_show.id)
        caption = f"Title: {tv_show_details.name}\n"
        caption += f"First Air Date: {tv_show_details.first_air_date}\n"
        caption += f"Vote Average: {tv_show_details.vote_average}\n"
        caption += f"Seasons: {tv_show_details.number_of_seasons}\n"
        caption += f"Total Episodes: {tv_show_details.number_of_episodes}\n"
        caption += f"Runtime: {tv_show_details.episode_run_time[0]} minutes"

        # Get the TV show poster
        poster_url = tmdb.base_url + f"w342{tv_show_details.poster_path}"

        # Send the photo with caption
        client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            reply_markup=show_overview_inline_keyboard(tv_show.id)
        )

# Handler for 'overview' command
@Client.on_callback_query(filters.regex('^overview_'))
def show_overview(client, callback_query):
    # Extract the TV show ID from the callback data
    tv_show_id = int(callback_query.data.split('_')[1])

    # Retrieve the TV show using the TMDB API
    tv_show = tv.details(tv_show_id)

    # Send the overview as a private message to the user
    client.send_message(chat_id=callback_query.from_user.id, text=tv_show.overview)

def show_overview_inline_keyboard(tv_show_id):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text="Show Overview",
                callback_data=f"overview_{tv_show_id}"
            )
        ]]
    )

