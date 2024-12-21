import tweepy
from time import sleep
from typing import List, Dict, Optional


class TwitterBot:

    def __init__(self, api_key: str, api_secret: str, access_token: str,
                 access_token_secret: str, bearer_token: str):
        """Initialize Twitter bot with credentials"""
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        # self.api = tweepy.API(auth)

        self.client = client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=False)

    def post_tweet(self, content: str) -> str:
        """
        Post a tweet
        
        Args:
            content (str): The content of the tweet
            
        Returns:
            str: Status message about the tweet
        """
        try:
            tweet = self.client.create_tweet(text=content)
            return f"Successfully posted tweet with ID: {tweet.data['id']}"
        except tweepy.TweepError as e:
            return f"Error posting tweet: {str(e)}"

    def read_mentions(self, count: int = 10) -> List[Dict]:
        """
        Read recent mentions
        
        Args:
            count (int): Number of recent mentions to retrieve
            
        Returns:
            List[Dict]: List of mention objects containing relevant information
        """
        try:
            mentions = self.api.mentions_timeline(count=count)
            return [{
                'id': mention.id,
                'text': mention.text,
                'user': mention.user.screen_name,
                'created_at': mention.created_at
            } for mention in mentions]
        except tweepy.TweepError as e:
            return [{'error': str(e)}]

    def reply_to_tweet(self, tweet_id: str, content: str) -> str:
        """
        Reply to a specific tweet
        
        Args:
            tweet_id (str): ID of the tweet to reply to
            content (str): Content of the reply
            
        Returns:
            str: Status message about the reply
        """
        try:
            tweet = self.api.get_status(tweet_id)
            username = tweet.user.screen_name
            reply_content = f"@{username} {content}"

            reply = self.api.update_status(status=reply_content,
                                           in_reply_to_status_id=tweet_id,
                                           auto_populate_reply_metadata=True)
            return f"Successfully replied to tweet {tweet_id}"
        except tweepy.TweepError as e:
            return f"Error replying to tweet: {str(e)}"

    def get_tweets(self, count: int = 10) -> List[Dict]:
        """
        Get tweets
        
        Args:
            count (int): Number of tweets to retrieve
            
        Returns:
            List[Dict]: List of matching tweets
        """
        try:
            userId = self.client.get_user(username="PumpFunUpdates").data.id  #

            response = self.client.get_users_tweets(userId, max_results=10)

            return [{
                'id': tweet.id,
                'text': tweet.text
            } for tweet in response.data]
        except tweepy.TweepError as e:
            return [{'error': str(e)}]
