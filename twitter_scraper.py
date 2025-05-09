from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import pandas as pd
from datetime import datetime

class TwitterScraper:
    def __init__(self, url):
        self.url = url
        self.tweets = []
        # Initialize Chrome options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Run in headless mode
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
    def setup_driver(self):
        """Initialize and return the webdriver"""
        return webdriver.Chrome(options=self.options)
        
    def scroll_page(self, driver):
        """Scroll the page to load more tweets"""
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # Wait for new tweets to load
            time.sleep(3)
            
            # Calculate new scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            # Break if no more new tweets
            if new_height == last_height:
                break
            last_height = new_height
            
    def extract_tweet_data(self, tweet_element):
        """Extract data from a tweet element"""
        try:
            username = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]').text
            timestamp = tweet_element.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
            tweet_text = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
            
            # Get engagement metrics if available
            try:
                replies = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="reply"]').text
                retweets = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]').text
                likes = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="like"]').text
            except NoSuchElementException:
                replies, retweets, likes = "N/A", "N/A", "N/A"
                
            return {
                'username': username,
                'timestamp': timestamp,
                'tweet_text': tweet_text,
                'replies': replies,
                'retweets': retweets,
                'likes': likes
            }
        except NoSuchElementException as e:
            print(f"Error extracting tweet data: {str(e)}")
            return None
            
    def scrape_tweets(self, max_tweets=100):
        """Main method to scrape tweets"""
        driver = self.setup_driver()
        try:
            # Load Twitter page
            driver.get(self.url)
            print(f"Scraping tweets from: {self.url}")
            
            while len(self.tweets) < max_tweets:
                # Find all tweet elements
                tweet_elements = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                
                # Extract data from new tweets
                for tweet_element in tweet_elements:
                    if len(self.tweets) >= max_tweets:
                        break
                        
                    tweet_data = self.extract_tweet_data(tweet_element)
                    if tweet_data and tweet_data not in self.tweets:
                        self.tweets.append(tweet_data)
                        print(f"Collected {len(self.tweets)} tweets")
                
                # Scroll to load more tweets
                self.scroll_page(driver)
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            driver.quit()
            
    def save_to_csv(self, filename=None):
        """Save scraped tweets to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'twitter_data_{timestamp}.csv'
            
        if self.tweets:
            df = pd.DataFrame(self.tweets)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Data saved to {filename}")
        else:
            print("No tweets to save")

def main():
    # Example usage
    url = input("Enter Twitter URL to scrape: ")
    max_tweets = int(input("Enter maximum number of tweets to scrape (default 100): ") or "100")
    
    scraper = TwitterScraper(url)
    scraper.scrape_tweets(max_tweets=max_tweets)
    scraper.save_to_csv()

if __name__ == "__main__":
    main()
