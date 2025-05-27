# Importation des bibliothèques nécessaires
import requests # Pour envoyer des requêtes HTTP
from bs4 import BeautifulSoup # Pour analyser le HTML
from urllib.parse import urljoin # Pour construire des URL complètes
import os # Pour gérer les fichiers et les dossiers
import csv # Pour écrire dans des fichiers CSV
import re # Pour utiliser des expressions régulières
# URL de base du site à scraper
base_url = "https://books.toscrape.com/"
# Fonction pour extraire un nombre (entier ou décimal) à partir d'un texte
def extract_number(text):
    match = re.search(r'\d+(\.\d+)?', text)
    return float(match.group()) if match else 0.0
# Fonction pour nettoyer un nom de fichier (supprimer les caractères interdits)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)
# Fonction pour télécharger une image et l’enregistrer dans un dossier
def download_image(img_url, save_folder, title):
    response = requests.get(img_url)
    if response.status_code == 200:
        filename = sanitize_filename(title)[:100] + ".jpg" #Sanitize + Truncate + Add Extension
        os.makedirs(save_folder, exist_ok=True)
        with open(os.path.join(save_folder, filename), 'wb') as f:
            f.write(response.content)
# Fonction pour extraire toutes les données d’un livre à partir de sa page
def extract_book_data(book_url, category_name):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
  # Titre du livre
    title = soup.h1.text.strip()
 # Description du livre
    description_tag = soup.find('div', id='product_description')
    description = description_tag.find_next_sibling('p').text.strip() if description_tag else "No description"
# Informations
    table = soup.find('table', class_='table table-striped')
    rows = {row.th.text.strip(): row.td.text.strip() for row in table.find_all('tr')}

    upc = rows.get('UPC', '')
    price_incl_tax = extract_number(rows.get('Price (incl. tax)', ''))
    price_excl_tax = extract_number(rows.get('Price (excl. tax)', ''))
    availability = extract_number(rows.get('Availability', ''))
    num_reviews = rows.get('Number of reviews', '')
 #rating
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag else "None"
# URL de l'image du livre
    img_tag = soup.find('img')
    img_url = urljoin(book_url, img_tag['src'])

   # Télécharger l’image
    download_image(img_url, f"images/{category_name}", title)
  # Retourne les données sous forme de liste
    return [
        book_url, upc, title, price_incl_tax, price_excl_tax,
        availability, description, category_name, rating, img_url
    ]
# Fonction pour récupérer les URLs de tous les livres d’une catégorie (avec gestion de la pagination)
def get_all_book_urls(category_url):
    book_urls = []

    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
     # Récupérer l’URL relative de chaque livre
        for book in books:
            relative_url = book.find('h3').find('a')['href']
            relative_url = relative_url.replace('../../../', 'catalogue/')
            full_url = urljoin(base_url, relative_url)
            book_urls.append(full_url)
 # Vérifie s’il y a une page suivante
        next_page = soup.find('li', class_='next')
        category_url = urljoin(category_url, next_page.find('a')['href']) if next_page else None

    return book_urls

# Fonction pour récupérer toutes les catégories de livres disponibles
def get_all_categories():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_tags = soup.find('ul', class_='nav-list').find_all('a')[1:]  # Skip "Books"
    categories = {
        tag.text.strip(): urljoin(base_url, tag['href'])
        for tag in category_tags
    }
    return categories
# Fonction principale qui gère tout le processus de scraping
def scrape_site():
    categories = get_all_categories()
  # Pour chaque livre, extraire les données
    for category_name, category_url in categories.items():
        print(f"\n Category: {category_name}")
        book_urls = get_all_book_urls(category_url)
        rows = []

        for url in book_urls:
            try:
                row = extract_book_data(url, category_name)
                rows.append(row)
                print(f"  {row[2]}")
            except Exception as e:
                print(f"Error: {e}")

        # Enregistrement des données dans un fichier CSV
        os.makedirs("csv", exist_ok=True)
        csv_filename = f"csv/{sanitize_filename(category_name)}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'product_page_url', 'universal_product_code', 'title',
                'price_including_tax', 'price_excluding_tax', 'number_available',
                'product_description', 'category', 'review_rating', 'image_url'
            ])
            writer.writerows(rows)

        print(f" CSV saved: {csv_filename}")
# Point d’entrée du script
if __name__ == "__main__":
    scrape_site()
