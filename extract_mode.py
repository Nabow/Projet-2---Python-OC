import extract_datas
import re
import get_input
from urllib.parse import urlparse


# On récupère les urls de tous les livres du site
def get_all_urls(url, nb_page=100000):
    page = url + "page-1.html"

    product_page_url = []
    i = 0
    while i < nb_page:

        soup = extract_datas.get_in_soup(page)

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


def get_all_categories(url):
    soup = extract_datas.get_in_soup(url)
    cat_temp = soup.find("ul", class_="nav nav-list")
    cat_temp = cat_temp.find_all("a")
    cat_list = {}
    i = 0
    for cat in cat_temp:
        i += 1
        cat_title = " ".join(cat.text.split())
        cat_list.update({i: [cat_title, cat.get('href').rsplit('/', 1)[0] + '/']})

    return cat_list


def extract_mode(mode, url):
    main_url = "https://" + urlparse(url).netloc
    if mode == 1:
        product_page_url = get_all_urls(url)
        datas = extract_datas.extraire_donnees(product_page_url)
        extract_datas.put_datas_csv(product_page_url)
    elif mode == 2:
        cat_list = get_all_categories(main_url)
        input_cat = get_input.choose_in_table("Choisissez une catégorie : ", cat_list)
        url = cat_list.get(input_cat)[1]
        url = main_url + "/" + url
        product_page_url = get_all_urls(url)
        datas = extract_datas.extraire_donnees(product_page_url)
        extract_datas.put_datas_csv(product_page_url, cat_list.get(input_cat)[0] + " - datas.csv")
    elif mode == 3:
        cat_list = get_all_categories(main_url)
        for cat, values in cat_list.items():
            url = values[1]
            url = main_url + "/" + url
            product_page_url = get_all_urls(url)
            datas = extract_datas.extraire_donnees(product_page_url)
            extract_datas.put_datas_csv(product_page_url, values[0] + " - datas.csv")
