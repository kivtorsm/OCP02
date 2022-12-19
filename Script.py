import requests
from bs4 import BeautifulSoup

# import time # pour utiliser des méthodes de temporisation et simuler un utilisateur réel

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
page = requests.get(url)  # Response -> code 200 = ok

if page.ok:  # vérifie si la réponse est ok (code 200)
    soup = BeautifulSoup(page.text, 'html.parser')  # Récupération de la page

    table = soup.find('table')  # Chercher table
    liste_td = table.find_all('td')  # Liste des valeurs de td

    # Test de récupération de valeurs d'un tableau en parcourant chaque ligne. ça renvoie des valeurs -1
    # TODO : demander pourquoi ça fonctionne comme ça.
    print('Comportement à comprendre')
    for tr in table:
        td = tr.find('td')
        print(td)

    # Liste toutes les variables à récupérer sur le fichier csv
    upc = liste_td[0].string
    title = soup.find('h1').string
    price_inc_tax = liste_td[3].string.replace('Â', '')
    print(liste_td[3].string)  # TODO : pourquoi le string renvoi le caractère Â ?
    price_exc_tax = liste_td[2].string.replace('Â', '')
    text_number_available = liste_td[5].string
    number_available = ''
    # Récupérer les valeurs numériques du str --> valeur de stock
    for str in text_number_available:
        if str.isdigit():
            number_available = number_available + str
    product_description = 'tbd'
    category = soup.find('ul',
                         {'class': 'breadcrumb'}).find('a',
                                                       {'href': "../category/books/poetry_23/index.html"}).get_text()
    review_rating_list = soup.find('p', {'class': 'instock availability'}).find_next_sibling().get_attribute_list(
        'class')
    review_rating_list.remove('star-rating')
    review_rating = review_rating_list[0]
    image_url = 'http://books.toscrape.com' + soup.img['src'].replace('../..', '')

    # Écriture ligne csv sous forme de str
    ligne_csv = url + ',' + upc + ',' + title + ',' + price_inc_tax + ',' + price_exc_tax + ',' \
                + number_available + ',' + 'product_description' + ',' + category + ',' \
                + review_rating + ',' + image_url + '\n'

    # Écrire fichier csv
    with open('output/livres.csv', 'w') as output_file:
        # Écrire en-tête
        output_file.write('product_page_url,universal_product_code (upc),title,price_including_tax,'
                          'price_excluding_tax,number_available,product_description,category,review_rating,'
                          'image_url\n')
        # Écrire contenu page
        output_file.write(ligne_csv)
else:
    print(page)

'''
with open('urls.txt', 'r') as inf:  # 'with' ferme tout seul le fichier à la fin de l'indentation
    with open('pays.csv', 'w') as output_file:
        output_file.write('pays,population\n')
            for row in inf:
                url = row.strip()  # pour supprimer le retour à la ligne
                response = requests.get(url)
                if response.ok:
                soup = BeautifulSoup(response.text)  # stocker contenu de la page
                country = soup.find('tr', {'id': 'places_country__row'}).find('td',{'class': 'w2p_fw'})  # Enregistrer le nom du pays
                pop = soup.find('tr', {'id': 'places_population__row'}).find('td', {'class': 'w2p_fw'})  # Enregistrer la valeur de population
                print('Pays: ' + country + ', Pop: ' + pop)  # Affichage des résultats
                outf.write(country.text. + ',' + pop.text.replace(',','') + '\n')  # remplacer les virgules dans les valeurs numériques par
                time.sleep(3)
'''
'''
links = []  # Liste de liens

# Parcourir toute la pagination
for i in range(26):
    url = 'http://example.webscraping.com/'
    response = requests.get(url)  # Response -> code 200 = ok
    print(response)  # Vérifier que la réponse est bonne au fur et à mesure de u parsing

    # Récupérer les liens de chacune des cellules du tableau
    if response.ok:  # vérifie si la réponse est ok (code 200)
        print('Page: ' + str(i))  # imprimer numéro de page
    soup = BeautifulSoup(response.text, 'lxml')  # 2e argument = parser à utiliser : lxml
    title = soup.find('title')  # Obtention du titre sans les balises
    tds = soup.findAll('td')  # récupérer toutes les cellules du tableau (balises td)

    # Dans chaque cellule récupérer le lien et le stocker dans la liste
    for td in tds:
        a = td.find('a')
    link = a['href']  # Récupérer un attribut à l'intérieur d'une balise
    links.append('http://example.webscrapping.com' + link)  # concaténation du lien
    time.sleep(3)  # Temporisation avant de renvoyer la boucle et éviter de se faire bloquer par le site
    print(len(links))  # Afficher liste des liens

    # Stocker la liste des liens dans un fichier .txt
    with open('urls.txt', 'w') as file:  # 'with' ferme tout seul le fichier à la fin de l'indentation
        for
    link in links:  # Pour chaque lien dans la liste
    file.write(link + '\n')  # Écrire le lien dans le fichier

    # Stocker les valeurs dans un fichier .csv
    with open('urls.txt', 'r') as inf:  # 'with' ferme tout seul le fichier à la fin de l'indentation
        with
    open('pays.csv', 'w') as outf:
    outf.write('pays,population\n')
    for row in inf:
        url = row.strip()  # pour supprimer le retour à la ligne
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text)  # stocker contenu de la page
    country = soup.find('tr', {'id': 'places_country__row'}).find('td',
                                                                  {'class': 'w2p_fw'})  # Enregistrer le nom du pays
    pop = soup.find('tr', {'id': 'places_population__row'}).find('td', {
        'class': 'w2p_fw'})  # Enregistrer la valeur de population
    print('Pays: ' + country + ', Pop: ' + pop)  # Affichage des résultats
    outf.write(country.text. + ',' + pop.text.replace(',',
                                                      '') + '\n')  # remplacer les virgules dans les valeurs numériques par 
    time.sleep(3)
'''
