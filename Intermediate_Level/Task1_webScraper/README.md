# Task 1: Web Scraper

This is a simple web scraper that extracts data from [http://quotes.toscrape.com/](http://quotes.toscrape.com/). It uses the `requests` library to fetch the HTML content of the page and `BeautifulSoup` to parse it and extract quotes, authors, and tags.

## Prerequisites
Make sure you have Python installed. You also need to install the required libraries:

```bash
pip install -r requirements.txt
```

## Running the Scraper
Run the Python script:

```bash
python web_scraper.py
```

The script will fetch the data and save it to a file named `scraped_quotes.csv` in the same directory.
