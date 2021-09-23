import book_to_scrap as bts

if __name__ == '__main__':
    url = 'http://books.toscrape.com/catalogue/'
    product_page_url = bts.get_all_urls(url, 1)
    datas = bts.extraire_donnees(product_page_url)
    bts.put_datas_csv(product_page_url)
    print("Et voilà le travail !")