import requests
from bs4 import BeautifulSoup
import csv
import nums_from_string
from urllib.parse import urlparse
# import pandas as pd

Rating_Table = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
    }


def get_in_soup(url):
        # lien de la page à scrapper
	reponse = requests.get(url)
	page = reponse.content

	# transforme (parse) le HTML en objet BeautifulSoup
	return BeautifulSoup(page, "html.parser")


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

# récupère les titres ou descriptions comme liste de strings
def extraire_donnees(elements):
    global url

    for element in elements:

        soup = get_in_soup(element)

        universal_product_code_UPC.append(soup.find("th" , text="UPC" ).next_sibling.text)
        title_product.append(soup.h1.string)

        price_including_tax.append(nums_from_string.get_nums(soup.find("th" , text="Price (incl. tax)" ).next_sibling.text)[0])
        price_excluding_tax.append(nums_from_string.get_nums(soup.find("th" , text="Price (excl. tax)" ).next_sibling.text)[0])
        
        availability = soup.find("p" , class_="instock availability").text
        try:
            number_available.append(nums_from_string.get_nums(availability)[0])
        except:
            number_available.append(0)

        try:
            product_description.append(soup.find( id="product_description" ).next_sibling.next_sibling.text)
        except:
            product_description.append("")

        test = soup.find("ul" , class_="breadcrumb" )
        cat = test.findAll("a")[2].text
        category.append(cat)


        rating = soup.find("p" , class_="star-rating").attrs["class"][1]
        review_rating.append(Rating_Table[rating])

        img = soup.find("div" , class_="item active").img.get_attribute_list("src")
        site_url = urlparse(element).netloc
        img_url = img[0].replace("../..", site_url)
        image_url.append(img_url)



# charger la donnée dans un fichier csv
def charger_donnees(nom_fichier, en_tete, titres, descriptions):
	with open(nom_fichier, 'w') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(en_tete)
		# zip permet d'itérer sur deux listes à la fois
		for titre, description in zip(titres, descriptions):
			writer.writerow([titre, description])


def scroll_page():
    print()
    

def get_all_urls(url, nb_page = 100000000):
    page = url + "page-1.html"

    product_page_url = []
    i=0
    while (i<nb_page):
        
        soup = get_in_soup(page)

        products = soup.find_all("h3")  
        for product in products:
            product_page_url.append( url + product.find("a").get('href') )

        try:
            page = soup.find("li", class_="next").a.get('href')
        except:
            break
        else:
            page = url + page
            i += 1
    return product_page_url


url='http://books.toscrape.com/catalogue/'

product_page_url = get_all_urls(url)

datas = extraire_donnees(product_page_url)


# print(datas)

with open('datas.csv', 'w', newline='') as fichier_csv:
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
        ligne = [str(product_page_url[i]), universal_product_code_UPC[i], str(title_product[i]), price_including_tax[i], price_excluding_tax[i], number_available[i], str(product_description[i]), category[i], review_rating[i], str(image_url[i])]
        # ligne = ligne.text.encode('utf8').decode('ascii', 'ignore')
        # ligne = str(ligne)
        writer.writerow(ligne)
        