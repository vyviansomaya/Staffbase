from post_news import NewsFeed
from upload_images import ImageUploader
import json
import logging

class Main():     
 def begin(self):
    config = self.get_config()
    authKey = config['authKey'] 
    feedUrl = config['rssFeedUrl']
    newsUrl = config['newsChannelUrlForFeedPost']
    usersListUrl = config['usersListUrl']
    folderPath = config['profilePicturesFolder']
    imageFormat = config['imageFormat']

    newsfeed = NewsFeed(authKey,feedUrl,newsUrl)  
    newsfeed.post_news()

    imageuploader = ImageUploader(authKey,usersListUrl,folderPath,imageFormat)
    imageuploader.upload_images()


 def get_config(self):
    with open('config.json', 'r') as f:
        config = json.load(f)
        f.close()
    return config


Main().begin()
