import tweepy

from generative_monster.settings import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    BEARER_TOKEN,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

class TwitterInterface:

    def __init__(self):
        # Twitter V2
        # Used to post tweets
        self._client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET)

        # Twitter V1
        # Required to upload media because V2 doesn't suppor it yet:
        # https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/integrate#media
        self._auth = tweepy.OAuth1UserHandler(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET)
        self._api = tweepy.API(self._auth)


    def upload_media(self, image_path, alt_text):
        media = self._api.media_upload(image_path)
        media_id = media.media_id
        self._api.create_media_metadata(media_id, alt_text)
        return media_id


    def search_tweets(self, query="from:aut0mata -is:retweet"):
        return self._client.search_recent_tweets(
            query=query,
            tweet_fields=['context_annotations', 'created_at'],
            max_results=100)


    def get_user(self, username="aut0mata"):
        return self._client.get_user(username=username)


    def tweet(self, text, media_ids=None):
        if media_ids:
            return self._client.create_tweet(text=text, media_ids=media_ids)
        return self._client.create_tweet(text=text)


    def tweet_with_images(self, text, prompt, image_paths):
        media_ids = []
        for image_path in image_paths:
            media_id = self.upload_media(image_path, prompt)
            media_ids.append(media_id)
        return self.tweet(text, media_ids)
