import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_quotes(url, output_file):
    """
    Scrapes quotes from quotes.toscrape.com and saves them to a CSV file.
    """
    print(f"Scraping {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_data = []

    # Find all quote containers
    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        # Extract the quote text
        text = quote.find('span', class_='text').get_text(strip=True)
        
        # Extract the author
        author = quote.find('small', class_='author').get_text(strip=True)
        
        # Extract the tags
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
        tags_str = ", ".join(tags)

        quotes_data.append({
            'Text': text,
            'Author': author,
            'Tags': tags_str
        })

    # Save to CSV
    if quotes_data:
        try:
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Text', 'Author', 'Tags'])
                writer.writeheader()
                writer.writerows(quotes_data)
            print(f"Successfully scraped {len(quotes_data)} quotes and saved to {output_file}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print("No quotes found on the page.")

if __name__ == "__main__":
    target_url = "http://quotes.toscrape.com/"
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(script_dir, "scraped_quotes.csv")
    
    scrape_quotes(target_url, output_csv)
