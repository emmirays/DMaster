import tweepy
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterBot:
    def __init__(self, api_key, api_secret, access_token, access_token_secret, bearer_token):
        print("Initializing Twitter Bot...")
        print("\nVerifying credentials...")
        print(f"API Key length: {len(api_key)}")
        print(f"API Secret length: {len(api_secret)}")
        print(f"Access Token length: {len(access_token)}")
        print(f"Access Token Secret length: {len(access_token_secret)}")
        print(f"Bearer Token length: {len(bearer_token)}")
        
        try:
            # Create Client for v2 endpoints
            self.api = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Test authentication
            print("\nTesting API connection...")
            me = self.api.get_me()
            if not me:
                raise Exception("Could not get user information")
            
            print(f"✅ Successfully authenticated as @{me.data.username}")
            print(f"Account ID: {me.data.id}")
            
            # Test API access
            print("\nTesting API access levels...")
            try:
                # Try to get a tweet (basic v2 endpoint)
                tweet = self.api.get_tweet(1)
                print("✅ Basic v2 endpoint access confirmed")
            except Exception as e:
                print(f"❌ Basic v2 endpoint test failed: {str(e)}")
            
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")

    def send_dm(self, participant_id, message):
        """Send a DM to a specific user"""
        try:
            print(f"\nAttempting to send DM...")
            print(f"Participant ID: {participant_id}")
            print(f"Message length: {len(message)}")
            
            response = self.api.create_direct_message(
                participant_id=participant_id,
                text=message,
                user_auth=True
            )
            
            print("API Response:", response)
            print(f"✅ Successfully sent DM to user ID: {participant_id}")
            return True
            
        except Exception as e:
            print(f"\n❌ Error sending DM: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response Status Code: {e.response.status_code}")
                print(f"Response Text: {e.response.text}")
            return False

def test_dm():
    try:
        print("\n=== Testing DM Functionality ===\n")
        
        bot = TwitterBot(
            API_KEY,
            API_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET,
            BEARER_TOKEN
        )
        
        me = bot.api.get_me()
        my_id = me.data.id
        
        print(f"\nAttempting to send test DM to self (@{me.data.username})...")
        test_message = "🤖 This is a test message from your Twitter bot!"
        success = bot.send_dm(my_id, test_message)
        
        if success:
            print("\n✅ Test completed successfully!")
        else:
            print("\n❌ Test failed")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_dm()