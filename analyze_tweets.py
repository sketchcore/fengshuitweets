from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pandas as pd

def login_to_twitter(driver, username, password):
    driver.get("https://twitter.com/login")
    
    # Wait for and enter username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
    )
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    
    # Wait for and enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

def scrape_tweets(driver, username):
    driver.get(f"https://twitter.com/{username}")
    
    tweets = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while len(tweets) < 100:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(2)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        # Find tweet elements
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
        
        for tweet in tweet_elements:
            if tweet not in tweets:
                tweets.append(tweet)
    
    return tweets[:100]  # Return only the first 100 tweets

def analyze_tweets(driver, username):
    tweets = scrape_tweets(driver, username)
    
    tweet_data = []
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    for tweet in tweets:
        # Extract tweet data (you may need to adjust these selectors based on Twitter's current HTML structure)
        text = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
        date_string = tweet.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        retweets = int(tweet.find_element(By.CSS_SELECTOR, "div[data-testid='retweet']").text or 0)
        likes = int(tweet.find_element(By.CSS_SELECTOR, "div[data-testid='like']").text or 0)
        
        if date > seven_days_ago:
            tweet_data.append({
                'text': text,
                'created_at': date,
                'retweets': retweets,
                'likes': likes,
                'engagement': retweets + likes
            })
    
    df = pd.DataFrame(tweet_data)
    df = df.sort_values('engagement', ascending=False)
    
    print("Top 5 most engaging tweets:")
    print(df.head()[['text', 'engagement']])
    
    print("\nAverage engagement:", df['engagement'].mean())

def main():
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.
    login_to_twitter(driver, "your_username", "your_password")
    analyze_tweets(driver, "your_username")
    driver.quit()

if __name__ == "__main__":
    main()