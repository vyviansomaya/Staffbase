import feedparser
import json
import requests
from datetime import datetime
from setup_logger import logger

class NewsFeed():

    def __init__(self,authkey,feedUrl,newsUrl):
        self.authKey= authkey
        self.feedUrl= feedUrl
        self.newsUrl= newsUrl

    def get_feeds(self):
        logger.info('Reading rss feeds from the {}'.format(self.feedUrl))
        return feedparser.parse(self.feedUrl)

    def make_payload(self,entry):
        post = {}
        contents = {}
        enContent = {}
        enContent['content'] = entry.description
        enContent['image'] = entry.enclosures[0].href
        enContent['title'] = entry.title
        contents['en_US'] = enContent
        post['contents'] = contents
        post['published'] =  datetime.strftime(datetime.strptime(entry.published, "%a, %d %b %Y %X +0000"),"%Y-%m-%dT%H:%M:%S.%fZ")
        return json.dumps(post)

    def post_news(self):
        rssURL = self.feedUrl
        NewsAPI = self.newsUrl

        feeds = self.get_feeds()
        logger.info('{} items in the feed'.format(len(feeds.entries)))
        for idx,entry in enumerate(feeds.entries):
            payload = self.make_payload(entry)
            body = payload
            headers = {'Authorization': 'Basic ' + self.authKey,
                   'Content-Type': 'application/json; charset=UTF-8'}
            entry
            logger.info('posting news with title "{}"'.format(entry.title))
            try:
                response = requests.post(NewsAPI,body,headers=headers)
                response.raise_for_status
            except requests.exceptions.RequestException as e:
                logger.error('error in making a news post: ' + str(e))
                raise SystemExit(e)
            if idx==3:
              break