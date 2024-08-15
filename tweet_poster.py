import json
import random
from datetime import datetime

def load_tips():
    with open('feng_shui_tips.json', 'r') as f:
        return json.load(f)

def save_tweets(tweets):
    today = datetime.now().strftime('%Y-%m-%d')
    data = {
        'date': today,
        'tweets': tweets
    }
    with open('tweets.json', 'w') as f:
        json.dump(data, f, indent=2)

def main():
    tips = load_tips()
    daily_tweets = random.sample(tips, 6)
    save_tweets(daily_tweets)

if __name__ == "__main__":
    main()