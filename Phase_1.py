import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# URL setup
url = "https://books.toscrape.com/catalogue/set-me-free_988/index.html"
base_url = "https://books.toscrape.com/"

# Request and parse
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Function to extract numbers
def extract_number(text):
    match = re.search(r'\d+(\.\d+)?', text)
    return float(match.group()) if match else None

# Product details
title = soup.h1.text.strip()
product_description = soup.find('div', id='product_description').find_next_sibling('p').text.strip()
table = soup.find('table', class_='table table-striped')
rows = {row.th.text.strip(): row.td.text.strip() for row in table.find_all('tr')}

# Data collection
product_data = {
    "Title": title,
    "Product Description": product_description,
    "UPC": rows.get('UPC'),
    "Product Type": rows.get('Product Type'),
    "Price (excl. tax)": extract_number(rows.get('Price (excl. tax)', '')),
    "Price (incl. tax)": extract_number(rows.get('Price (incl. tax)', '')),
    "Tax": extract_number(rows.get('Tax', '')),
    "Availability": extract_number(rows.get('Availability', '')),
    "Number of Reviews": rows.get('Number of reviews'),
    "Rating": soup.find('p', class_='star-rating')['class'][1],
    "Category": soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
    "Image URL": urljoin(base_url, soup.find('img')['src']),
    "Product Page URL": url
}
# Print everything 
for key, value in product_data.items(): #.items() is a method of a dictionary that returns a view of all its key-value pairs as tuples.
    print(f"{key}: {value}")
# Writing to CSV
csv_file = 'product_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=product_data.keys())
    writer.writeheader()
    writer.writerow(product_data)

print(f"Data has been written to {csv_file}")