import requests
from bs4 import BeautifulSoup
import csv


# récupère les titres ou descriptions comme liste de strings
def extraire_donnees(elements):
	resultat = []
	for element in elements:
		resultat.append(element.string)
	return resultat


def get_in_soup(url):
        # lien de la page à scrapper
	reponse = requests.get(url)
	page = reponse.content

	# transforme (parse) le HTML en objet BeautifulSoup
	return BeautifulSoup(page, "html.parser")


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
    

def get_all_urls(url):
    page = url + "page-1.html"

    table_urls = []

    while (page):
        
        soup = get_in_soup(page)

        products = soup.find_all("h3")  
        for product in products:
            table_urls.append( url + product.find("a").get('href') )

        try:
            page = soup.find("li", class_="next").a.get('href')
        except:
            return table_urls
        else:
            page = url + page




table_urls = get_all_urls('http://books.toscrape.com/catalogue/')

extraire_donnees(table_urls)



# en_tetes = [ 
# "product_page_url",
# "universal_product_code (upc)",
# "title",
# "price_including_tax",
# "price_excluding_tax",
# "number_available",
# "product_description",
# "category",
# "review_rating",
# "image_url"
# ]