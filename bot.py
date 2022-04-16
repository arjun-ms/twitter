import tweepy
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from textblob import TextBlob
import re
from PIL import Image, ImageDraw, ImageFont

FILE_NAME = 'last_seen_id.txt'

print('Welcome to twitter bot')

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

auth = tweepy.OAuth1UserHandler(
   CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

last_seen_id = retrieve_last_seen_id(FILE_NAME)
mentions = api.mentions_timeline(since_id = last_seen_id,tweet_mode='extended')


for mention in reversed(mentions):
    print(str(mention.id)+' --- '+mention.full_text)
    last_seen_id = mention.id
    # store_last_seen_id(last_seen_id,FILE_NAME)
    if '#quoteit' in mention.full_text.lower():
        print('Quoted')
        original_tweet_id = mention.in_reply_to_status_id
        # fetching the status with extended tweet_mode
        status = api.get_status(original_tweet_id, tweet_mode = "extended")
        # fetching the full_text attribute
        full_text = status.full_text 
        quote = re.sub(r"http\S+", "", full_text)
        author = str("-" + status.author.name)
        
        print("Quote : " + quote +"\n"+"Author: "+author)
        
        bg_img = Image.open("bg.jpg")
        quote_image = ImageDraw.Draw(bg_img)
        
        quote_font = ImageFont.truetype('roboto-slab/RobotoSlab-Regular.ttf', 152)
        quote_text = str(quote)

        # offset = 0
        # for i in quote_text:
        #     i = i.split(".")
        #     for ix in i:
        #         quote_image.text((15,15+offset), ix, (216, 233, 237), font=quote_font)
        #         offset += 100
        
        # quote_image.text((15,15+offset), author, (216, 233, 237), font=quote_font)
        W, H = (6000,4000)
        quote_image.text((W/2,H/2),quote_text,font = quote_font,fill="#000000",anchor='ms')
        quote_image.text((W/2,3*H/4),author,font = quote_font,fill="#000000",anchor='ms')
        bg_img.save("quotedbybot.jpg")