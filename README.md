
Books to Scrape
Description
Ce projet permet de collecter des données sur les livres depuis le site Books to Scrape afin de surveiller les prix et autres informations par catégorie.
Le script télécharge les informations détaillées de chaque livre ainsi que les images, puis sauvegarde les données sous forme de fichiers CSV organisés par catégorie.
Fonctionnalités
•	Extraction des détails des livres (titre, prix, disponibilité, description,  etc.)
•	Téléchargement des images des couvertures des livres
•	Gestion de la pagination et des multiples catégories
•	Enregistrement des données dans des fichiers CSV structurés par catégorie
Prérequis
•	Python 3.x
•	Principales bibliothèques utilisées :
o	requests(pip install requests)
o	BeautifulSoup4(pip install BeautifulSoup4)
Création et activation de l'environnement virtuel
sous windows :
python -m venv venv
venv\Scripts\activate
Sous macOS/Linux :
python3 -m venv venv
source venv/bin/activate
Si vous exécutez ce projet dans un environnement virtuel, vous pouvez installer les dépendances :
pip install -r requirements.txt
Utilisation
Pour lancer le script, exécutez :
python Phase_4.py
Les données et images extraites seront sauvegardées automatiquement dans les dossiers /csv (pour les fichiers CSV) et /images (pour les images classées par catégorie).
Résultats attendus
•	Dossiers /csv/ contenant un fichier CSV par catégorie avec les informations des livres
•	Dossiers /images/<nom_de_catégorie>/ contenant les images des livres correspondants
Organisation du projet
/csv/               # Données extraites au format CSV  
/images/            # Images téléchargées, triées par catégorie  
Phase_4.py          # Script principal du scraper  
Read_me.txt          # Ce fichier
Remarques
•	Le script gère les erreurs d’extraction et continue le traitement même si certains livres posent problème
•	Les noms de fichiers sont nettoyés pour éviter les caractères invalides
•	Il est possible d’adapter ou d’étendre le script pour supporter d’autres sites ou fonctionnalités
Contact
Pour toute question ou remarque, vous pouvez me contacter [abirami1488@gmail.com]
