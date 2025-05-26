import requests # Pour envoyer des requêtes HTTP
from bs4 import BeautifulSoup # Pour analyser (parser) le contenu HTML
from urllib.parse import urljoin # Pour construire des URLs complètes
import csv  # Pour écrire les données dans un fichier CSV
import os #permet de travailler avec les dossiers et fichiers de ton ordinateur
import re #Extraire des chiffres dans une phrase

BASE_URL = "https://books.toscrape.com/"

# extraire un nombre depuis un texte (e.g., "In stock (20 available)")
def extract_number(text):
    match = re.search(r'\d+', text)
    return float(match.group()) if match else 0

# extraire les détails d’un livre
def extract_book_data(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.h1.text.strip()
    #Description du livre
    product_description = soup.find('div', id='product_description')
    description = product_description.find_next_sibling('p').text.strip() if product_description else "No description"
   #Catégorie
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    #Infos dans le tableau (UPC, prix, dispo, etc.)
    table = soup.find('table', class_='table table-striped')
    rows = {row.th.text.strip(): row.td.text.strip() for row in table.find_all('tr')}
   # Champs individuels
    upc = rows.get('UPC', '')
    price_incl_tax =extract_number (rows.get('Price (incl. tax)', ''))
    price_excl_tax = extract_number(rows.get('Price (excl. tax)', ''))
    availability = extract_number(rows.get('Availability', ''))
    num_reviews = rows.get('Number of reviews', '')
   #rating
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag else "None"
   #image
    img_tag = soup.find('img')
    img_url = urljoin(book_url, img_tag['src']) if img_tag else "No image"
   #Retour des données sous forme de liste
    return [
        book_url,
        upc,
        title,
        price_incl_tax,
        price_excl_tax,
        availability,
        description,
        category,
        rating,
        img_url
    ]

# Fonction : récupérer tous les livres d’une catégorie (avec pagination)
def get_books_in_category(category_url):
    book_urls = []

    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        books = soup.find_all('article', class_='product_pod')
        for book in books:
            rel_url = book.find('h3').find('a')['href'] #récupère le lien du livre tel qu’il est écrit dans le code HTML de la page.
            fixed_url = rel_url.replace('../../../', 'catalogue/')
            book_url = urljoin(BASE_URL, fixed_url)
            book_urls.append(book_url)
      #Passer à la page suivante s’il y a
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_page = next_btn.find('a')['href']
            category_url = urljoin(category_url, next_page)
        else:
            category_url = None

    return book_urls

# Fonction : récupérer toutes les catégories
def get_all_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Trouver tous les liens vers les catégories
    category_tags = soup.select('div.side_categories ul li ul li a')
    categories = {
        tag.text.strip(): urljoin(BASE_URL, tag['href'])
        for tag in category_tags
    }
    return categories

# Fonction : enregistrer les livres d’une catégorie dans un CSV
def save_category_to_csv(category_name, book_data_list):
    filename = f"{category_name.replace(' ', '_').lower()}.csv"
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)
#Écrire les données
    headers = ['product_page_url', 'universal_product_code (upc)', 'title',
               'price_including_tax', 'price_excluding_tax', 'number_available',
               'product_description', 'category', 'review_rating', 'image_url']

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as file: # 'utf-8-sig' CSV supports special characters like é, ñ, €, etc.
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(book_data_list)

    print(f" {category_name} → Saved {len(book_data_list)} books to '{filepath}'")

# === Main Flow ===
if __name__ == "__main__":
    print(" Starting Phase 3: Extracting all books in all categories...\n")
    #Obtenir toutes les catégories
    categories = get_all_categories()
#Pour chaque catégorie :
    for category_name, category_url in categories.items():
        print(f" Processing category: {category_name}")
        book_urls = get_books_in_category(category_url)

        book_data_list = []
        for book_url in book_urls:
            try:
                data = extract_book_data(book_url)
                book_data_list.append(data)
            except Exception as e:
                print(f" Error extracting {book_url}: {e}")
     # Sauvegarder dans un fichier CSV
        save_category_to_csv(category_name, book_data_list)

    print(" All categories have been processed.")
