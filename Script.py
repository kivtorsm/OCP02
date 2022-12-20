import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil

# Nettoyer répertoire output
folder = './output/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Create target Directory if don't exist
dir_img = './output/img'
if not os.path.exists(dir_img):
    os.mkdir(dir_img)
    print("Directory ", dir_img, " Created ")
else:
    print("Directory ", dir_img, " already exists")

url = 'http://books.toscrape.com/index.html'
page = requests.get(url)

if page.ok:
    soup = BeautifulSoup(page.text, 'html.parser')
    category_bloc = soup.find(class_='nav nav-list').find('ul')
    nb_categories = len(category_bloc.find_all('a'))

    # Enregistrer la liste des catégories et des urls dans un fichier csv
    with open('./output/categories.csv', 'w') as file:
        file.write('category_name,category_code,category_url\n')  # Écrire en-tête du fichier csv

        # Parcourir liste des catégories et les écrire dans le fichier
        for i in range(nb_categories):
            category_name = category_bloc.find_all('li')[i].a.string.strip()
            category_href = category_bloc.find_all('a')[i].get('href')
            category_code = category_bloc.find_all('a')[i].get('href').replace('catalogue/category/books/', '').replace(
                '/index.html', '')
            category_url = url.replace('index.html', '') + category_href
            file.write(category_name + ',' + category_code + ',' + category_url + '\n')

else:
    print(page)

with open('./output/categories.csv', newline='') as file:
    reader = csv.DictReader(file)
    n = 0  # Compteur de livres finis
    k = 0  # compteur de catégories finies
    for row in reader:
        j = 0  # Remise à 0 du compteur de livres enregistrés par catégorie
        category_url = row['category_url']
        category_page = requests.get(category_url)
        category_code = row['category_code']
        category_name = row['category_name']
        # print(category_code)
        # print(category_url)
        # print(category_name)

        if category_page.ok:  # vérifie si la réponse est ok (code 200)
            category_soup = BeautifulSoup(category_page.text, 'html.parser')

            # Initialiser liste de pages de la catégorie à scraper
            books_root = 'http://books.toscrape.com/catalogue/category/books/'
            category_root = books_root + row['category_code']
            urls_catalogue = [row['category_url']]
            books_root = 'http://books.toscrape.com/catalogue/category/books/'

            # Vérifier si la catégorie contient une seule page
            current_field_response = category_soup.find(class_='current')
            # print(current_field_response)

            if current_field_response is not None:

                # Identifier nombre de pages à parcourir
                current_field = category_soup.find(class_='current').string
                nb_pages = int(current_field.replace('Page 1 of ', ''))
                print(category_name + ': ' + str(nb_pages) + ' pages')

                # Ajouter pages du catalogue à scraper à la liste
                for i in range(nb_pages):
                    if i > 0:
                        url_page = str(category_root + '/page-' + str(i + 1) + '.html')
                        urls_catalogue.append(url_page)
            else:
                print(category_name + ': 1 page')

            # Ouvrir fichier pour lister les urls des livres
            category_file_name = './output/' + category_code + '.txt'
            with open(category_file_name, 'w') as url_file:

                # Parcourir chaque page de catalogue
                for catalogue in urls_catalogue:
                    catalogue_page = requests.get(catalogue)
                    catalogue_soup = BeautifulSoup(catalogue_page.text, 'html.parser')

                    # Récupérer tous les liens d'une page
                    h3_list = catalogue_soup.find('section').find_all('h3')

                    # Parcourir chaque titre de livre pour récupérer l'url et l'écrire dans un fichier .txt
                    for h3 in h3_list:
                        book_url = 'http://books.toscrape.com/catalogue' + h3.a['href'].replace('../../..', '')
                        url_file.write(book_url + '\n')

            with open(category_file_name, 'r') as url_list:
                # Ouvrir fichier csv pour écrire les noms des livres
                with open('output/livres.csv', 'w', encoding="utf-8") as output_file:
                    # Écrire en-tête
                    output_file.write('product_page_url,universal_product_code (upc),title,price_including_tax,'
                                      'price_excluding_tax,number_available,product_description,category,review_rating,'
                                      'image_url\n')
                    for book_url in url_list:
                        book_page = requests.get(book_url.strip())  # Response -> code 200 = ok

                        if book_page.ok:  # vérifie si la réponse est ok (code 200)
                            # print(book_page)
                            book_soup = BeautifulSoup(book_page.text, 'html.parser')  # Récupération de la page
                            # print(book_soup.title.string)

                            table = book_soup.find('table')  # Chercher table
                            liste_td = table.find_all('td')  # Liste des valeurs de td

                            # Test de récupération de valeurs d'un tableau en parcourant chaque ligne. ça renvoie des
                            # valeurs -1 TODO : demander pourquoi ça fonctionne comme ça.
                            for tr in table:
                                td = tr.find('td')
                                # print(td)

                            # Liste toutes les variables à récupérer sur le fichier csv
                            upc = liste_td[0].string
                            title = book_soup.find('h1').string
                            price_inc_tax = liste_td[3].string.replace('Â', '')
                            # print(liste_td[3].string)  # TODO : pourquoi le string renvoi le caractère Â ?
                            price_exc_tax = liste_td[2].string.replace('Â', '')
                            text_number_available = liste_td[5].string
                            number_available = ''
                            # Récupérer les valeurs numériques du str → valeur de stock
                            for string in text_number_available:
                                if string.isdigit():
                                    number_available = number_available + string
                            product_description = 'tbd'
                            category_url = '../category/books/' + category_code + '/index.html'
                            # print(category_url)
                            category_field = book_soup.find('ul',
                                                            {'class': 'breadcrumb'}).find('a',
                                                                                          {'href': category_url}).string
                            review_rating_list = book_soup.find('p',
                                                                {
                                                                    'class': 'instock availability'}).find_next_sibling().get_attribute_list(
                                'class')
                            review_rating_list.remove('star-rating')
                            review_rating = review_rating_list[0]
                            image_url = 'http://books.toscrape.com' + book_soup.img['src'].replace('../..', '')

                            # Écriture ligne csv sous forme de str
                            ligne_csv = url + ',' + upc + ',' + title + ',' + price_inc_tax + ',' + \
                            price_exc_tax + ',' + number_available + ',' + 'product_description' + ',' + \
                            category_code + ',' + review_rating + ',' + image_url + '\n'

                            # Écrire contenu page
                            output_file.write(ligne_csv)
                            n += 1
                            j += 1
                            print(str(n) + ' livres enregistrés au total et ' + str(j) + ' dans ' + category_name)

                            # Enregistrer image livre

                            image_url_code = book_soup.find('img')['src']
                            image_url = 'http://books.toscrape.com' + image_url_code.replace('../..', '')
                            filename = './output/img/' + upc + '.jpg'
                            # print(filename)

                            # Open the url image, set stream to True, this will return the stream content.
                            r = requests.get(image_url, stream=True)

                            # Check if the image was retrieved successfully
                            if r.status_code == 200:
                                # Set decode_content value to True, otherwise the downloaded image file's size will
                                # be zero.
                                r.raw.decode_content = True

                                # Open a local file with wb ( write binary ) permission.
                                with open(filename, 'wb') as f:
                                    shutil.copyfileobj(r.raw, f)

                                print('Image sucessfully Downloaded: ', filename)
                            else:
                                print('Image Couldn\'t be retreived')

                        else:
                            print(book_page)

            k += 1
            print(str(k) + ' / ' + str(nb_categories) + ' catégories complétées')

        else:
            print(page)
