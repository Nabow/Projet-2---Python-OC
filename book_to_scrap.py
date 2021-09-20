import requests
from bs4 import BeautifulSoup
import csv
import nums_from_string


def get_in_soup(url):
        # lien de la page à scrapper
	reponse = requests.get(url)
	page = reponse.content

	# transforme (parse) le HTML en objet BeautifulSoup
	return BeautifulSoup(page, "html.parser")


# récupère les titres ou descriptions comme liste de strings
def extraire_donnees(elements):
	universal_product_code = []
    title_product = []
    price_including_tax = []
    price_excluding_tax = []
    number_available = []
    product_description = []
    category = []
    review_rating = []
    image_url = []
    results = []

	for element in elements:

        soup = get_in_soup(element)

        universal_product_code.append(soup.find("th" , text="UPC" ).next_sibling)
        title_product.append(soup.h1.string)
        price_including_tax.append(soup.find("th" , text="Price (incl. tax)" ).next_sibling)
        price_excluding_tax.append(soup.find("th" , text="Price (excl. tax)" ).next_sibling)
        
        availability = soup.find("p" , class_="instock availability").text
        number_available.append(nums_from_string.get_nums(availability))

        product_description.append(soup.find( id="product_description" ).next_sibling.next_sibling)  #Ne marche pas

        test = soup.find("ul" , class_="breadcrumb" )
        cat = test.select("li:nth-child(3) > a") #Ne marche pas
        category.append(cat.string)


        review_rating_score = soup.find("p" , class_="star-rating *")
    
        image_url

    return results = [elements, universal_product_code, title_product, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ]


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

    product_page_url = []

    while (page):
        
        soup = get_in_soup(page)

        products = soup.find_all("h3")  
        for product in products:
            product_page_url.append( url + product.find("a").get('href') )

        try:
            page = soup.find("li", class_="next").a.get('href')
        except:
            return product_page_url
        else:
            page = url + page




product_page_url = get_all_urls('http://books.toscrape.com/catalogue/')

extraire_donnees(product_page_url)



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