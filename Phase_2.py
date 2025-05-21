import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/category/books/art_25/index.html"
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text,'html.parser')
print(soup)
ol = soup.find('ol')
articles = ol.find_all('article', class_="product_pod")
cat_titles = []
for article in articles:
    image = article.find('img')
    title = image.attrs['alt']
    print(title)
    cat_titles.append({'Category_Titles':title})
    #creating CSV file
with open ("category.csv","w",newline='',encoding='utf-8')as f:
 writer=csv.DictWriter(f, fieldnames=['Category_Titles'])
 writer.writeheader()
 writer.writerows(cat_titles)