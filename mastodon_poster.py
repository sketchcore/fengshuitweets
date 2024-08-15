from mastodon import Mastodon
import json
import time
import random

# Mastodon API credentials
mastodon = Mastodon(
    access_token = 'your_access_token',
    api_base_url = 'https://mastodon.social'  # or your chosen instance
)

def load_tips():
    with open('feng_shui_tips.json', 'r') as f:
        return json.load(f)

def post_toot(tip):
    try:
        mastodon.status_post(tip)
        print(f"Toot posted: {tip}")
    except Exception as e:
        print(f"Error posting toot: {e}")

def main():
    tips = load_tips()
    while True:
        tip = random.choice(tips)
        post_toot(tip)
        # Wait for 4 hours before next toot (14400 seconds)
        time.sleep(14400)

if __name__ == "__main__":
    main()