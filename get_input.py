import os


# Ajoute à un message les occurences d'un tableau pour faire un choix
def add_table_to_string(string, table):
    # Donne le nombre d'éléments d'un tableau
    string += "[1-" + str(len(table)) + "]\n"
    for item in table.items():
        # loop dans un dictionnary pour récupérer tous les éléments
        string += str(item) + "\n"
    return string


# Affiche un message sur la console pour demander de choisir un élément
def choose_in_table(message, table):
    message = add_table_to_string(message, table)
    while True:
        try:
            mode = int(input(message))
        except ValueError:
            print("Veuillez taper un chiffre allant de 1 à " + str(len(table)))
            continue
        else:
            if 0 < mode <= len(table):
                break
            else:
                print("Veuillez taper un chiffre allant de 1 à " + str(len(table)))
                continue
    # print("Vous avez choisi : " + table[mode])
    return mode


tble_mode = {
    1: "Tous les produits",
    2: "Tous les produits d'une catégorie",
    3: "Tous les produits par catégorie"
}


def choose_mode():
    prompt_message_mode = "Choisi un mode d'extraction : "
    return choose_in_table(prompt_message_mode, tble_mode)
