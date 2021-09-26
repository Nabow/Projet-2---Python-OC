import extract_mode
import get_input


if __name__ == '__main__':
    url = 'http://books.toscrape.com/catalogue/'
    mode = get_input.choose_mode()
    extract_mode.extract_mode(mode, url)

    print("Et voilà le travail !")

