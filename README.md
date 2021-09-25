#Créer un envrionnement virtuel
Pour créer un environnement :

1. Ouvrez l'invite de commande (touche Windows + R puis tappez "cmd")
2. Placez-vous dans le dossier du projet avec la commande :
```powershell
cd chemin_dossier
```
Pensez à remplacer chemin_dossier par votre vrai chemin
3. Initialisez l'environnement virtuel
```powershell
python -m venv env
```
4. Activez l'environnement
```powershell
call env/Scripts/activate.bat
```
5. Installez les paquets de **requirements.txt**
```powershell
pip install -r requirements.txt
```

#Lancer le Script

Il vous suffit de lancer le script en **double-cliquant sur main.py** ou en **tappant dans l'invite de commande**
```powershell
python main.py
```

Le résultat du script se trouvera dans le dossier Datas