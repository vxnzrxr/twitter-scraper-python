# Twitter Scraper

A Python script to scrape tweets from Twitter pages with infinite scroll functionality.

## Features

- Automatically scrolls through Twitter pages to load more tweets
- Extracts tweet data including:
  - Username
  - Timestamp
  - Tweet text
  - Engagement metrics (replies, retweets, likes)
- Saves data to CSV file with timestamp
- Configurable maximum number of tweets to scrape

## Requirements

- Python 3.6+
- Chrome/Chromium browser
- ChromeDriver matching your Chrome version

## Installation

1. Install required Python packages:
```bash
pip install -r requirements.txt
```

2. Install ChromeDriver:
   - Download ChromeDriver that matches your Chrome version from: https://sites.google.com/chromium.org/driver/
   - Add ChromeDriver to your system PATH

## Usage

1. Run the script:
```bash
python twitter_scraper.py
```

2. Enter the Twitter URL when prompted
3. Enter the maximum number of tweets to scrape (default: 100)
4. The script will create a CSV file with the scraped data in the current directory

## Output

The script creates a CSV file named `twitter_data_YYYYMMDD_HHMMSS.csv` containing:
- Username
- Timestamp
- Tweet text
- Number of replies
- Number of retweets
- Number of likes

## Notes

- The script runs Chrome in headless mode
- Twitter's layout may change, which could affect the scraping selectors
- Respect Twitter's terms of service and rate limits
