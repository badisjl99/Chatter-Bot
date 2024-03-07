8import pymongo
import random
import time
from telegram import Bot, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from io import BytesIO
import requests
import pyshorteners

# MongoDB connection settings
MONGODB_URI = 'mongodb+srv://badisjl99:123321Sn99.@cluster0.gnyg3mm.mongodb.net/'
DB_NAME = 'moviesdb'
COLLECTION_NAME = 'movies'

# Telegram bot token
TELEGRAM_BOT_TOKEN = '7079642245:AAF_YS_QchnsBDuNj1z1NOuGIdguNPvHA0Q'

# Telegram channel ID
CHANNEL_ID = '@qtumairdropcommunity'

client = pymongo.MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def shorten_url(url):
    # Initialize a URL shortener
    s = pyshorteners.Shortener()
    # Shorten the URL
    return s.tinyurl.short(url)

def send_movie_to_channel():
    high_rated_movies = collection.aggregate([
        { '$match': { 'rating': { '$gt': "7.5" }, 'year': { '$gt': '2010' } } },
        { '$sample': { 'size': 1 } }
    ])
    
    
    for movie in high_rated_movies:
        title = movie.get('title', 'Unknown Title')
        year = movie.get('year', 'Unknown Year')
        summary = movie.get('summary', 'No summary available')
        image_url = movie.get('imageUrl')
        directors = ', '.join(movie.get('directors', ['Unknown Director']))
        genres = ', '.join(movie.get('genres', ['Unknown Genre']))
        rating = movie.get('rating', 'No rating available')
        downloads = movie.get('download', [])
        
        image_response = requests.get(image_url)
        image_data = BytesIO(image_response.content)
        
        message = "<b>Hot Torrent Movies</b>\n\n"\
                  f"Title: <b>{title}</b>\n\n"\
                  f"<b>Rating:</b> ⭐️ <b>{rating}</b>\n\n"\
                  f"<b>Year:</b> <b>{year}</b>\n\n"\
                  f"<b>Directors:</b> {directors}\n\n"\
                  f"<b>Genres:</b> {genres}\n\n"\
                  f"<b>Summary:</b> {summary}\n\n"\
                  "<b>Downloads:</b>\n\n"
        
        keyboard = []
        for download in downloads:
            link = download.get('link', 'Unknown Link')
            quality = download.get('quality', 'Unknown Quality')
            # Shorten the download link
            short_link = shorten_url(link)
            keyboard.append([InlineKeyboardButton(text=quality, url=short_link)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        bot.send_photo(chat_id=CHANNEL_ID, photo=image_data, caption=message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

if __name__ == "__main__":
    while True:
        print("Bot is Running...")
        send_movie_to_channel()
        time.sleep(90)
