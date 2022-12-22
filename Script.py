import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil


def get_parameter(parameter):
    parameter_dic = {
        'home_page': 'http://books.toscrape.com/index.html',
        'output': './output/',
        'img': './output/img',
        'tmp': './tmp/',
        'book_root': 'http://books.toscrape.com/catalogue',
        'category_root': 'http://books.toscrape.com/catalogue/category/books/',
        'categories.csv': './tmp/categories.csv'
    }
    return parameter_dic[parameter]


def get_category_root(category_code_):
    category_root = get_parameter('category_root') + category_code_
    return category_root


def get_txt_book_url_list_path(category_code_):
    book_url_txt_list = get_parameter('tmp') + category_code_ + '.txt'
    return book_url_txt_list


def get_csv_book_url_list_path(category_code_):
    book_url_csv_list = get_parameter('output') + category_code_ + '.csv'
    return book_url_csv_list


def clean_dir(folder):
    if not os.path.exists(folder):
        print("Directory ", folder, " doesn't exist ")
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


# Nettoyer répertoires output et tmp s'il existe
clean_dir(get_parameter('output'))
clean_dir(get_parameter('tmp'))


def create_img_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Directory ", path, " Created ")
    else:
        print("Directory ", path, " already exists")


# Create output/img and tmp Directory tree if it doesn't exist
create_img_dir(get_parameter('img'))
create_img_dir(get_parameter('tmp'))


def url_to_soup(url_to_scrap):
    url_to_scrap = url_to_scrap.strip()
    scrap_page = requests.get(url_to_scrap)
    scrap_soup = BeautifulSoup(scrap_page.content, 'html.parser')
    # print(book_soup.title.string)
    return scrap_soup


def categories_to_csv(category_list_url, category_csv_file_path):
    # Create
    page = requests.get(category_list_url)
    if page.ok:
        soup = url_to_soup(category_list_url)
        category_bloc = soup.find(class_='nav nav-list').find('ul')
        nb_categories = len(category_bloc.find_all('a'))

        # Saves for each category : name, code, url -> temp
        with open(category_csv_file_path, 'w') as file:
            # Écrire en-tête du fichier csv
            file.write('category_name\tcategory_code\tcategory_url\n')

            # Parcourir liste des catégories et les écrire dans le fichier
            for i in range(nb_categories):
                category_name = category_bloc.find_all('li')[i].a.string.strip()
                category_href = category_bloc.find_all('a')[i].get('href')
                category_code = category_bloc.find_all('a')[i].get('href').replace('catalogue/category/books/',
                                                                                   '').replace(
                    '/index.html', '')
                category_url = category_list_url.replace('index.html', '') + category_href
                file.write(category_name + '\t' + category_code + '\t' + category_url + '\n')

    else:
        print(page)


categories_csv_file_path = get_parameter('categories.csv')
home_page = get_parameter('home_page')
categories_to_csv(home_page, categories_csv_file_path)


# Open liste des catégories à scraper
with open(categories_csv_file_path, newline='') as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in reader:
        category_url = row['category_url']
        category_code = row['category_code']
        category_name = row['category_name']
        # print(category_code)
        # print(category_url)
        print(category_name)

        def category_url_to_book_url_txt_list(category_url_, category_code_):
            category_page = requests.get(category_url_)
            if category_page.ok:  # vérifie si la réponse est ok (code 200)
                print(category_code_)
                category_soup = url_to_soup(category_url_)

                # Initialiser liste de pages de la catégorie à scraper
                category_root = get_category_root(category_code_)  # category root path

                # Initializing category catalogue url list (category pages)
                category_catalogue_url_list = [category_url_]

                def get_category_catalogue_number_of_pages(soup):
                    current_field_response = soup.find(class_='current')
                    # print(current_field_response)
                    if current_field_response is not None:

                        # Identifier nombre de pages à parcourir
                        current_field = category_soup.find(class_='current').string
                        nb_pages = int(current_field.replace('Page 1 of ', ''))
                        # print(str(nb_pages) + ' pages')
                        return nb_pages

                    else:
                        # print('1 page')
                        return 1

                # Get number of catalogue pages in the category
                category_nb_pages = get_category_catalogue_number_of_pages(category_soup)

                def add_catalogue_pages_to_catalogue_url_list(catalogue_url_list, category_nb_of_pages):
                    # Ajouter pages du catalogue à scraper à la liste
                    for i in range(category_nb_of_pages):
                        if i > 0:
                            url_page = str(category_root + '/page-' + str(i + 1) + '.html')
                            catalogue_url_list.append(url_page)
                    # print(catalogue_url_list)
                    return catalogue_url_list

                # List all catalogue pages to parse
                category_catalogue_url_list = add_catalogue_pages_to_catalogue_url_list(category_catalogue_url_list,
                                                                                        category_nb_pages)
                # Get book url txt list path -> tmp
                book_url_txt_list = get_txt_book_url_list_path(category_code_)

                def category_list_to_book_url_txt_file(book_url_list_txt_file_path, catalogue_url_list):
                    # Creates text file with all book urls
                    with open(book_url_list_txt_file_path, 'w') as book_url_list_file:

                        # Parse every page in the category catalogue
                        for category_catalogue_page_url in catalogue_url_list:
                            print(category_catalogue_page_url)
                            category_catalogue_soup = url_to_soup(category_catalogue_page_url)

                            # Récupérer tous les liens d'une page
                            h3_list = category_catalogue_soup.find('section').find_all('h3')

                            # Parcourir chaque titre de livre pour récupérer l'url et l'écrire dans un fichier .txt
                            for h3 in h3_list:
                                book_url_to_txt = get_parameter('book_root') + h3.a['href'].replace('../../..', '')
                                book_url_list_file.write(book_url_to_txt + '\n')

                # Save all book urls in a category to a category.txt file
                category_list_to_book_url_txt_file(book_url_txt_list, category_catalogue_url_list)
            else:
                print(category_page)

        # Scrapping all categories and saving book-urls to .txt files
        category_url_to_book_url_txt_list(category_url, category_code)

        def book_url_txt_list_to_book_data_csv_list(category_code_):
            book_url_txt_list = get_txt_book_url_list_path(category_code_)
            book_data_csv_file = get_csv_book_url_list_path(category_code_)
            print(book_data_csv_file)

            # Open category.txt and category.csv file with all book page urls for that category
            with open(book_data_csv_file, 'w', encoding='utf-8-sig') as output_file:
                # Write header
                output_file.write(
                    'product_page_url\tuniversal_product_code (upc)\ttitle\tprice_including_tax\t'
                    'price_excluding_tax\tnumber_available\tproduct_description\tcategory\treview_rating\t'
                    'image_url\timage_local_path\n')
                with open(book_url_txt_list, 'r') as book_url_list:

                    for book_url in book_url_list:
                        book_url = book_url.strip()

                        def book_info_to_csv(book_url_, category_code__):  # TODO : call function
                            # Save book data to csv and save book file
                            book_page = requests.get(book_url_.strip())

                            # Récupérer données de la page du livre et les écrire dans fichier .csv
                            if book_page.ok:  # vérifie si la réponse est ok (code 200)
                                # print(book_page)
                                book_soup = url_to_soup(book_url_)

                                def book_data_to_str(book_soup_, book_url__, category_code___):
                                    # Scrap book content
                                    td_list = book_soup_.find('table').find_all(
                                        'td')  # Liste avec toutes les valeurs de td

                                    # Liste toutes les variables à récupérer sur le fichier csv
                                    print(book_url__)
                                    upc = td_list[0].string
                                    title = book_soup_.find('h1').string
                                    price_inc_tax = td_list[3].string
                                    price_exc_tax = td_list[2].string

                                    def get_stocks(td_list_):
                                        # Récupérer valeur des stocks disponibles
                                        text_number_available = td_list_[5].string
                                        stocks = ''
                                        for string in text_number_available:
                                            if string.isdigit():
                                                stocks = stocks + string
                                        return stocks

                                    number_available = get_stocks(td_list)

                                    def get_product_description(book_soup__):
                                        product_description_title = book_soup__.find(id='product_description')
                                        if product_description_title is not None:
                                            product_description_string = product_description_title.find_next_sibling().string
                                            return product_description_string
                                        else:
                                            return ''

                                    product_description = get_product_description(book_soup_)
                                    category_page_url = get_category_root(
                                        category_code___) + category_code___ + '/index.html'
                                    category_path = '../category/books/' + category_code___ + '/index.html'
                                    # print(category_url)
                                    category_field = book_soup_.find('ul',
                                                                     {'class': 'breadcrumb'}).find('a',
                                                                                                   {'href': category_path}).string

                                    def get_rating(book_soup__):
                                        review_rating_list = book_soup__.find('p',
                                                                              {
                                                                                  'class':
                                                                                      "instock availability"}).find_next_sibling().get_attribute_list(
                                            'class')
                                        review_rating_list.remove('star-rating')
                                        review_rating_str = review_rating_list[0]
                                        rating_dic = {
                                            'One': 1,
                                            'Two': 2,
                                            'Three': 3,
                                            'Four': 4,
                                            'Five': 5
                                        }
                                        review_rating_ = str(rating_dic[review_rating_str])
                                        return review_rating_

                                    review_rating = get_rating(book_soup_)

                                    def download_book_covers(img_url):
                                        filename = './output/img/' + upc + '.jpg'
                                        # print(filename)

                                        # Open the url image, set stream to True, this will return the stream content.
                                        r = requests.get(img_url, stream=True)

                                        # Check if the image was retrieved successfully
                                        if r.status_code == 200:
                                            # Set decode_content value to True, otherwise the downloaded image file's size will
                                            # be zero.
                                            r.raw.decode_content = True

                                            # Open a local file with wb ( write binary ) permission.
                                            with open(filename, 'wb') as f:
                                                shutil.copyfileobj(r.raw, f)

                                            print('Image sucessfully Downloaded: ', filename)
                                            filename_path = os.getcwd() + filename.replace('.', '')
                                            return filename_path
                                        else:
                                            print('Image Couldn\'t be retreived')
                                            return "No img found"

                                    # Enregistrer image livre
                                    image_url = 'http://books.toscrape.com' + book_soup_.img['src'].replace('../..', '')
                                    image_url_code = book_soup.find('img')['src']
                                    image_local_url = download_book_covers(image_url)

                                    # Écriture ligne csv sous forme de str
                                    ligne_csv = book_url__ + '\t' + upc + '\t' + title + '\t' + price_inc_tax + '\t' + \
                                                price_exc_tax + '\t' + number_available + '\t' + product_description + '\t' + \
                                                category_field + '\t' + review_rating + '\t' + image_url + '\t' + image_local_url + '\n'

                                    return ligne_csv

                                book_data = book_data_to_str(book_soup, book_url_, category_code__)
                                output_file.write(book_data)
                            else:
                                print(book_page)

                        book_info_to_csv(book_url, category_code_)

        # Scraping all book urls and saving data to csv and images locally
        book_url_txt_list_to_book_data_csv_list(category_code)
