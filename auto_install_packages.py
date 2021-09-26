import os
import subprocess


def check_env():
    env = "env"
    if not (os.path.exists(env)):
        print("Création d'un environnement virtuel\n")
        subprocess.Popen('python -m venv env', shell=True).wait()


def check_requirements():
    file = "requirements.txt"
    if not (os.path.exists(file)):
        print("Le fichier requirements.txt est manquant, cela va prendre plus de temps\n")
        subprocess.Popen('pip install pipreqs', shell=True).wait()
        print("Récupération de la liste des paquets nécessaires\n")
        subprocess.Popen('pipreqs ' + os.getcwd(), shell=True).wait()


def auto_install_packages():
    #     subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    check_env()
    check_requirements()
    subprocess.Popen('."\\"env"\\"Scripts"\\"activate', shell=True).wait()
    subprocess.Popen('pip install -r requirements.txt', shell=True).wait()
    print("Paquets installés avec succès")
    os.system('pause')


auto_install_packages()
