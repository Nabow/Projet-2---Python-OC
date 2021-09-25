import requests
from bs4 import BeautifulSoup
import csv
import nums_from_string
from urllib.parse import urlparse
import os
import re

# Crée la table de correspondance entre les ranking et une valeur numérique
Rating_Table = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Crée les tableaux qui contiendront les informations de chacune des pages produits
universal_product_code_UPC = []
title_product = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []
results = []


def get_in_soup(url):
    # lien de la page à scrapper
    reponse = requests.get(url)
    # On évite les erreurs d'encodage
    reponse.encoding = reponse.apparent_encoding
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    return BeautifulSoup(page, "html.parser")


# Vérifie si le dossier en question existe et sinon il le crée
def check_directory(dir_name):
    if not (os.path.exists(dir_name)):
        os.makedirs(dir_name)


# Télécharge les images et les stocke dans un dossier
def download_image(img_url, img_name, img_dir=""):
    img_data = requests.get(img_url).content
    if img_dir:
        check_directory(img_dir)
    image_path = os.path.join(img_dir, img_name)
    with open(image_path, 'wb') as handler:
        handler.write(img_data)


# récupère les informations des produits et les stocke dans les tableaux précédement crées
def extraire_donnees(elements):
    # Boucle dans chacune des url produit
    for element in elements:

        soup = get_in_soup(element)
        # Récupère l'UPC
        universal_product_code_UPC.append(soup.find("th", text="UPC").next_sibling.text)
        # Récupère le titre du livre
        title_product.append(soup.h1.string)
        # Récupère le prix TTC
        price_including_tax.append(
            nums_from_string.get_nums(soup.find("th", text="Price (incl. tax)").next_sibling.text)[0])
        # Récupère le prix HT
        price_excluding_tax.append(
            nums_from_string.get_nums(soup.find("th", text="Price (excl. tax)").next_sibling.text)[0])
        # Récupère la quantité en stock et si erreur alors on a pas de stock
        availability = soup.find("p", class_="instock availability").text
        try:
            number_available.append(nums_from_string.get_nums(availability)[0])
        except:
            number_available.append(0)
        # Récupère la description et
        try:
            product_description.append(soup.find(id="product_description").next_sibling.next_sibling.text)
        except:
            product_description.append("")
        # Récupère le nom de la catégorie
        cat = soup.find("ul", class_="breadcrumb")
        cat = cat.findAll("a")[2].text
        category.append(cat)
        # Récupère le rating
        rating = soup.find("p", class_="star-rating").attrs["class"][1]
        review_rating.append(Rating_Table[rating])
        # Récupère l'url de l'image
        img = soup.find("div", class_="item active").img.get_attribute_list("src")
        # On récrée l'url absolue à partir de l'url relative
        site_url = urlparse(element).netloc
        img_url = "https://" + img[0].replace("../..", site_url)
        image_url.append(img_url)

        # Si l'image a une balise alt alors on la récupère pour l'utiliser quand on l'enregistrera
        try:
            img_alt = soup.find("div", class_="item active").img.get_attribute_list("alt")[0]
            img_alt = re.sub('\W+', ' ', img_alt)
        except:
            img_alt = ""
        # On récupère le nom actuel de l'image
        image_name = os.path.basename(img_url)
        if img_alt:
            extension = os.path.splitext(image_name)[1]
            image_name = str(img_alt) + str(extension)
        # On enregistre l'image
        download_image(img_url, image_name, "datas/img")


# On récupère les urls de tous les livres du site
def get_all_urls(url, nb_page=100000000):
    page = url + "page-1.html"

    product_page_url = []
    i = 0
    while (i < nb_page):

        soup = get_in_soup(page)

        products = soup.find_all("h3")
        for product in products:
            product_page_url.append(url + product.find("a").get('href'))

        try:
            page = soup.find("li", class_="next").a.get('href')
        except:
            break
        else:
            page = url + page
            i += 1
    return product_page_url


# On met toutes les valeurs dans un fichier CSV
def put_datas_csv(product_page_url):
    dir_datas = "datas"
    check_directory(dir_datas)
    abs_file_path = os.path.join(dir_datas, "datas.csv")
    with open(abs_file_path, 'w', newline='', encoding="utf-8") as fichier_csv:
        en_tetes = [
            "product_page_url",
            "universal_product_code_UPC (upc)",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
        ]
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerow(en_tetes)
        for i in range(len(product_page_url)):
            ligne = [str(product_page_url[i]), universal_product_code_UPC[i], str(title_product[i]), price_including_tax[i],
                     price_excluding_tax[i], number_available[i], str(product_description[i]), category[i],
                     review_rating[i], str(image_url[i])]
            writer.writerow(ligne)
