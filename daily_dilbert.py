import tweepy
import requests
import datetime
import time
from PIL import Image
from io import BytesIO

auth = tweepy.OAuthHandler(authKey, secretKey)
auth.set_access_token(AccessToken, secretAccessToken)

api = tweepy.API(auth)

tweet_check = False

def check_time(flag_check):
	current_time = datetime.datetime.now()
	if current_time.hour > 7 and flag_check == True:
		tweet_check = False
		print('Too early to tweet. Snoozing ...')
	elif current_time.hour == 7 and flag_check == False:
		print('Good morning! Time to tweet ...')
		tweet_comic()
		tweet_check = True
	else:
		print(current_time.strftime("%H:%M")+' Not time to tweet. Snoozing ...')

def tweet_comic():
	request = requests.get('https://dilbert-api.glitch.me/json').json()
	print(request['title'] + " - " + request['image'])

	comicURL = requests.get('http:'+request['image'])
	comicImage = Image.open(BytesIO(comicURL.content))
	comicImage.save(BytesIO(), 'PNG')

	comicUpload = api.media_upload('comic.png')
	api.update_status(status=request['title']+' #DailyDilbert', media_ids=[comicUpload.media_id])

while True:
	check_time(tweet_check)
	time.sleep(3600)