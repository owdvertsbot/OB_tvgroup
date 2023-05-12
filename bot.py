import requests
import re
import os
from dotenv import load_dotenv
import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import BOT_TOKEN, API_ID, API_HASH, THETVDB_API_KEY

load_dotenv()

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    app = pyrogram.Client(
        "filter bot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins,
        workers=300
    )


def get_tvshow_info(name):
    url = f'https://api.thetvdb.com/search/series?name={name}'
    headers = {'Authorization': f'Bearer {os.getenv("THETVDB_API_KEY")}'}
    response = requests.get(url, headers=headers).json()
    if response.get("data"):
        tv_show = response['data'][0]
        title = tv_show['seriesName']
        overview = tv_show['overview']
        poster_path = tv_show['poster']
        if poster_path:
            poster_url = f'https://www.thetvdb.com/banners/{poster_path}'
            return title, overview, poster_url
    return None


def is_tvshow(message_text):
    regex = r'\b([Tt][Vv]\s*[Ss]\d{2}([Ee]?\d{2})*)|([Tt][Vv]\s*[Ss]\d{1,2}\s*[Ee]\d{1,2})|([Tt][Vv]\s*series)\b'
    return re.search(regex, message_text)


@app.on_message(filters.text & ~filters.edited)
async def on_message(client, message):
    if is_tvshow(message.text):
        tvshow_info = get_tvshow_info(message.text)
        if tvshow_info:
            title, overview, poster_url = tvshow_info
            await message.reply_text(f'{title}\n\n{overview}')
            await message.reply_photo(photo=poster_url)


app.run()
