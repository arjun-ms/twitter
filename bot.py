import tweepy
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from textblob import TextBlob
import re
from PIL import Image, ImageDraw, ImageFont
import textwrap
from string import ascii_letters
import time

FILE_NAME = 'last_seen_id.txt'

print('Welcome to Quote It! bot.')

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

auth = tweepy.OAuthHandler(
   CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

while(True):
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(since_id = last_seen_id,tweet_mode='extended')

    for mention in reversed(mentions):

        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,FILE_NAME)
        if '#quoteit' in mention.full_text.lower():
            print('#quoteit verified')
            original_tweet_id = mention.in_reply_to_status_id
            
            # fetching the status
            status = api.get_status(original_tweet_id, tweet_mode = "extended")
            # fetching the full_text attribute
            full_text = status.full_text 
            quote = re.sub(r"http\S+", "", full_text)
            author = str("-" + status.author.name)
            
            print("Quote : " + quote +"\n"+"Author: "+author)
            
            bg_img = Image.open("bg.jpg")
            quote_image = ImageDraw.Draw(bg_img)
            quote_font = ImageFont.truetype('roboto-slab/RobotoSlab-Bold.ttf', 192)
            quote_text = str(quote)

            # Calculate the average length of a single character of our font.
            # Note: this takes into account the specific font and font size.
            avg_char_width = sum(quote_font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            # Translate this average length into a character count
            max_char_count = int(bg_img.size[0] * .618 / avg_char_width)
            quote_text = textwrap.fill(text=quote_text, width=35)

            W, H = (6000,4000)
            quote_image.text((W/2,H/2),quote_text,font = quote_font,fill="#000000",anchor='mm')
            quote_image.text((13*W/20,3*H/4),author,font = quote_font,fill="#000000",anchor='ms')
            bg_img.save("quotedbybot.jpg")

            #  generate tweet with image
            api.update_status_with_media(status = f"@{mention.user.screen_name}",filename='./quotedbybot.jpg',in_reply_to_status_id = mention.id)
            print("quote image sent")
            time.sleep(20)