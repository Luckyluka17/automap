"""
Développé par Luckyluka17.
Logiciel gratuit et open source.
"""
import os
import json
import webbrowser
import codecs

print("Chargement des modules...")
os.system("title Automap - Démarrage...")

try:
    import folium
    from bs4 import BeautifulSoup
    import requests
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    os.system("cls")
except ImportError:
    os.system("cls")
    print("Un ou plusieurs ne sont pas installés, installation automatique...")
    with requests.get("https://raw.githubusercontent.com/automap-organization/automap/main/appinfo.json") as r:
        data = json.loads(r.text)
        for i in data['dependencies']:
            os.system(f"pip install {i}")
        del data
    os.system("cls")
    print("Installation terminée.\nRedémarrez le programme pour appliquer les modifications.")
    os.system("pause")
    exit()
except:
    print("Une erreur inconnue est survenue.")
    os.system("pause")
    exit()

version = "0.6"

os.system("cls")
print(Fore.YELLOW + "Vérification des mises à jour...")
with requests.get("https://raw.githubusercontent.com/automap-organization/automap/main/appinfo.json") as r:
    data = json.loads(r.text)
    if data["latest-version"] != version and data["disable-update-check"] == False:
        os.system("cls")
        print(Fore.RED + "Mise à jour disponible !")
        print("Version actuelle : " + version)
        print("Version disponible : " + data["latest-version"])
        print("Voulez-vous télécharger la mise à jour ? (O/N)")
        if input(">").upper() == "O":
            webbrowser.open(f"https://github.com/automap-organization/automap/releases/download/{data['latest-version']}/automap.exe")
    
    os.system("cls")

if not os.name == "nt":
    os.system("clear")
    print("""Nous avons detecté que l'application s'éxécute sur un système non windows.
    Il est possible que certaines commandes ne fonctionnent pas comme prévu.
    (une version linux est en cours de développement)
""")

os.system(f"title Automap v{version}")
print(f"""Automap [Version {version}]
Créé par Luckyluka17
Fonctionne avec Folium, BeautifulSoup4 and Requests
""")

maplist = []
selectedmap = []
selectedmap1 = ""
listpoints = []
colorterminal = "5"
colorpoints = "blue"

if data["disable-app"] == True:
    os.system("cls")
    print(Fore.RED + "L'application est désactivée temporairement.")
    print(Fore.RED + "Raison :" + data["disable-app-reason"])
    os.system("pause")
    exit()


if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        data1 = json.loads(f.read())
        colorterminal = str(data1["colorterminal"])
        colorpoints = str(data1["colorpoints"])
        f.close()
        del data1
else:
    with open("config.json", "w") as f:
        settingdata = {
            "colorterminal": colorterminal,
            "colorpoints": colorpoints
        }
        f.write(json.dumps(settingdata))
        f.close()


if colorterminal == "1":
    os.system("color 4")
elif colorterminal == "2":
    os.system("color 2")
elif colorterminal == "3":
    os.system("color 1")
elif colorterminal == "4":
    os.system("color 6")
elif colorterminal == "5":
    os.system("color 7")
else:
    os.system("color 7")

while True:
    cmd = str(input("=>")).lower()

    if cmd == "help":
        print("""help : Affiche l'aide
create : Crée une nouvelle carte
select : Sélectionne une carte
delete : Supprime une carte
save : Sauvegarde la carte
list maps : Affiche la liste des cartes créées
list markers : Affiche la liste des points sur la carte séléctionnée
list icons : Affiche la liste des icones pour les points
list plugins : Affiche la liste des plugins installés
addmarker : Ajoute un marqueur
delmarker : Supprime un marqueur
credits : Affiche les crédits
settings : Affiche le menu des paramètres
plugin install : Télécharge et installe un plugin
plugin uninstall : Supprime un plugin
plugin start : Démarre un plugin
plugin info : Affiche les informations d'un plugin
check update : Vérifie les mises à jour
clear : Efface le contenu de la console
exit : Quitte l'application""")
    elif cmd == "exit":
        exit()
    elif cmd.startswith("create"):
        createdmap = cmd.split(" ")
        if len(createdmap) == 2:
            if not createdmap[1] in maplist:
                createdmap = createdmap[1]
                maplist.append(createdmap)
                print(f"La carte {createdmap} a été créée.")
            else:
                print(Fore.RED + f"Erreur \"map\": une carte a ce nom existe déjà. Pour la supprimer, utilisez la commande \"delete {createdmap[1]}\"")
        else:
            print(Fore.RED + "Erreur \"args\": la commande 'create' doit être suivie uniquement d'un nom de carte.")
    elif cmd == "list maps":
        if len(maplist) != 0:
            for i in maplist:
                ind = int(maplist.index(i))
                ind = maplist[ind]
                if i == selectedmap1:
                    print(Fore.CYAN + f"- {ind} (Selectionnée)")
                else:
                    print(f"- {ind}")
        else:
            print(Fore.YELLOW + "Aucune carte n'a été créée.")
    elif cmd.startswith("delete"):
        deletedmap = cmd.split(" ")
        if len(deletedmap) == 2:
            if deletedmap[1] in maplist:
                deletedmap = deletedmap[1]
                maplist.remove(deletedmap)

                if selectedmap1 == deletedmap:
                    selectedmap1 = ""
                
                print(f"La carte {deletedmap} a été supprimée.")
            else:
                print(Fore.RED + f"Erreur \"map\": une carte a ce nom n'existe pas.")
        else:
            print(Fore.RED + "Erreur \"args\": la commande 'delete' doit être suivie uniquement d'un nom de carte.")
    elif cmd.startswith("select"):
        selectedmap = cmd.split(" ")
        if len(selectedmap) == 2:
            if selectedmap[1] in maplist:
                if selectedmap[1] != selectedmap1 and selectedmap1 != "":
                    print(Fore.YELLOW + "ATTENTION : séléctionner une autre carte efface les données de la carte précédemment sélectionnée !\nVoulez-vous continuer ? (y/n)")
                    if str(input("=>")) == "y":
                        selectedmap1 = str(selectedmap[1])
                        listpoints = []
                        carte = folium.Map()
                        tile = folium.TileLayer(
                            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                            attr = 'Esri',
                            name = 'Esri Satellite',
                            overlay = False,
                            control = True
                        ).add_to(carte)
                        print(f"La carte {selectedmap1} est actuellement sélectionnée.")
                else:
                    selectedmap1 = str(selectedmap[1])
                    listpoints = []
                    carte = folium.Map()
                    tile = folium.TileLayer(
                            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                            attr = 'Esri',
                            name = 'Esri Satellite',
                            overlay = False,
                            control = True
                        ).add_to(carte)
                    print(f"La carte {selectedmap1} est actuellement sélectionnée.")
            else:
                print(Fore.RED + f"Erreur \"map\": une carte à ce nom n'existe pas.")
        else:
            print(Fore.RED + "Erreur \"args\": la commande 'select' doit être suivie uniquement d'un nom de carte.")
    elif cmd == "save":
        if selectedmap1 in maplist:
            if selectedmap1 != "":
                print(f"Sauvegarde de {selectedmap1} en cours...")
                for i in listpoints:
                    try:
                        if len(i) == 3:
                            folium.Marker(location=[i[0], i[1]], icon=folium.Icon(color=colorpoints, prefix='glyphicon', icon=i[2])).add_to(carte)
                        else:
                            folium.Marker(location=[i[0], i[1]], icon=folium.Icon(color=colorpoints)).add_to(carte)
                    except:
                        print("Erreur \"marker\": un marqueur n'a pas pu être ajouté à la carte.")
                try:
                    carte.save(f"{selectedmap1}.html")
                    print(f"Sauvegarde de {selectedmap1} terminée.")
                except:
                    print(Fore.RED + "Erreur \"save\": la carte n'a pas pu être sauvegardée.")
            else:
                print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée.")
    elif cmd == "clear":
        os.system("cls")
    elif cmd.startswith("addmarker"):
        addpin = cmd.replace(",", "").split(" ")
        if len(addpin) == 3 or len(addpin) == 4:
            if selectedmap1 in maplist:
                if selectedmap1 != "":
                    if len(addpin) == 4:
                        listpoints.append([addpin[1], addpin[2], addpin[3]])
                    else:
                        listpoints.append([addpin[1], addpin[2]])
                    print("Marqueur ajouté.")
                else:
                    print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
            else:
                print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée.")
        else:
            print(Fore.RED + "Erreur \"args\": la commande 'addmarker' doit être suivie de coordonnées.")
    elif cmd == "addline":
        if selectedmap1 in maplist:
            if selectedmap1 != "":
                markersline = []
                ch = "a"
                print("Pour créer une ligne, vous devez entrer plusieurs coordonnées. Pour terminer la ligne, appuyez sur entrer.")
                while ch != "":
                    ch = input("addline=>")
                    if len(ch.replace(",", "").split(" ")) == 2:
                        if ch != "":
                            memory = ch.replace(",", "").split(" ")
                            markersline.append((memory[0], memory[1]))
                    elif ch != "":
                        print(Fore.RED + "Erreur \"marker\": les coordonnées entrées ne sont pas valides.")
                    else:
                        try:
                            folium.PolyLine(markersline, color=colorpoints, weight=2.5, opacity=0.8).add_to(carte)
                            print("Ligne créée.")
                        except RecursionError:
                            print(Fore.RED + "Erreur \"line\": la ligne doit avoir 5 points ou plus.")
                        except:
                            print(Fore.RED + "Erreur \"line\": la ligne n'a pas pu être créée.")
            else:
                print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée.")
    elif cmd == "list markers":
        if selectedmap1 in maplist:
                if selectedmap1 != "":
                    if len(listpoints) != 0:
                        for i in listpoints:
                            try:
                                print(f"- {i[0]}, {i[1]} | Icone : {i[2]}")
                            except IndexError:
                                print(f"- {i[0]}, {i[1]}")
                    else:
                        print(Fore.YELLOW + "Aucun marqueur n'a été ajouté sur la carte séléctionnée.")
                else:
                    print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée.")
    elif cmd.startswith("delmarker"):
        addpin = cmd.replace(",", "").split(" ")
        if len(addpin) == 3 or len(addpin) == 4:
            if selectedmap1 in maplist:
                if selectedmap1 != "":
                    try:
                        if len(addpin) == 3:
                            listpoints.remove([addpin[1], addpin[2]])
                        else:
                            listpoints.remove([addpin[1], addpin[2], addpin[3]])

                        print("Point supprimé.")
                    except:
                        print(Fore.RED + "Erreur \"marker\": ce point n'existe pas.")
                else:
                    print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
            else:
                print(Fore.RED + "Erreur \"map\": aucune carte n'est sélectionnée.")
        else:
            print(Fore.RED + "Erreur \"args\": la commande 'delmarker' doit être suivie de coordonnées (et d'un nom de logo si vous en avez mis un).")
    elif cmd == "credits":
        print(f"""- Développeur : Luckyluka17
- Version : {version}
- Carte : Esri""")
    elif cmd == "settings":
        print("""Paramètres d'automap (pour séléctionner le paramètre, entrez le numéro du menu, et pour quitter, appuyez juste sur entrer.) :
1 - Couleur de la console
2 - Couleur des marqueurs""")
        setting=str(input("=>"))
        if setting == "1":
            print("""Couleurs disponibles :
1 - Rouge
2 - Vert
3 - Bleu
4 - Jaune
5 - Blanc""")
            colorterminal=str(input("=>"))
            if colorterminal == "1":
                os.system("color 4")
            elif colorterminal == "2":
                os.system("color 2")
            elif colorterminal == "3":
                os.system("color 1")
            elif colorterminal == "4":
                os.system("color 6")
            elif colorterminal == "5":
                os.system("color 7")

            with open("config.json", "w") as f:
                settingdata = {
                    "colorterminal": colorterminal,
                    "colorpoints": colorpoints
                }
                f.write(json.dumps(settingdata))
                f.close()
        elif setting == "2":
            print("""Couleurs disponibles :
1 - Rouge
2 - Vert
3 - Bleu""")
            colorpoints=str(input("=>"))
            if colorpoints == "1":
                colorpoints = "red"
            elif colorpoints == "2":
                colorpoints = "green"
            elif colorpoints == "3":
                colorpoints = "blue"

            with open("config.json", "w") as f:
                settingdata = {
                    "colorterminal": colorterminal,
                    "colorpoints": colorpoints
                }
                f.write(json.dumps(settingdata))
                f.close()
    elif cmd == "list icons":
        print("Icones disponibles :\n")
        with requests.get("https://getbootstrap.com/docs/3.3/components/") as r:
            soup = BeautifulSoup(r.content, "html.parser")
            for i in soup.find_all(class_="bs-glyphicons-list"):
                print(i.text.replace("glyphicon-", "").replace("glyphicon", "").replace("     ", "\n").replace("    ", ""))
    elif cmd.startswith("plugin install"):
        plugin = cmd.split(" ")
        if len(plugin) == 3:
            with requests.get("https://raw.githubusercontent.com/automap-organization/automap/main/appinfo.json") as r:
                plugins = json.loads(r.text)["plugins_availables"]
                if plugin[2] in plugins:
                    print(Fore.RED + "Avertissement : ne téléchargez pas des plugins qui ne proviennent pas de cette commande.\n")
                    try:
                        os.mkdir("Plugins")
                    except FileExistsError:
                        pass
                    print(Fore.YELLOW + "Téléchargement du plugin en cours...")
                    os.system(f"curl https://raw.githubusercontent.com/automap-organization/automap/main/src/plugins/{plugin[2]}.py -o \"%cd%\Plugins\{plugin[2]}.py\" >nul")
                    print(Fore.GREEN + "Plugin téléchargé.")
                else:
                    print(Fore.RED + "Erreur \"plugin\": ce plugin n'existe pas.")
        else:
            print(Fore.RED + "Erreur \"plugin\": la commande \"plugin install\" doit être suivie du nom du plugin.")
    elif cmd.startswith("plugin start"):
        plugin = cmd.split(" ")
        if len(plugin) == 3:
            if os.path.exists(f"Plugins\\{plugin[2]}.py"):
                print(Fore.YELLOW + "Démarrage du plugin en cours...")
                os.system(f"python \"%cd%\Plugins\\{plugin[2]}.py\"")
                print(Fore.YELLOW + "Le plugin a fini son exécution.")
            else:
                print(Fore.RED + "Erreur \"plugin\": ce plugin n'existe pas ou n'est pas installé.")
        else:
            print(Fore.RED + "Erreur \"plugin\": la commande \"plugin start\" doit être suivie du nom du plugin.")
    elif cmd.startswith("plugin info"):
        plugin = cmd.split(" ")
        if len(plugin) == 3:
            if os.path.exists(f"Plugins\\{plugin[2]}.py"):
                with codecs.open(f"Plugins\\{plugin[2]}.py", "r", "utf-8") as f:
                    info = f.read().split("\"\"\"")
                    print(info[1])
            else:
                print(Fore.RED + "Erreur \"plugin\": ce plugin n'existe pas ou n'est pas installé.")
        else:
            print(Fore.RED + "Erreur \"plugin\": la commande \"plugin info\" doit être suivie du nom du plugin.") 
    elif cmd == "list plugins":
        try:
            os.mkdir("Plugins")
        except FileExistsError:
            pass

        with requests.get("https://raw.githubusercontent.com/automap-organization/automap/main/appinfo.json") as r:
            plugins_availables = json.loads(r.text)["plugins_availables"]

        if os.listdir("Plugins") != []:
            try:
                for i in os.listdir("Plugins"):
                    if i.endswith(".py"):
                        if i.replace('.py', '') in plugins_availables:
                            print(Fore.GREEN + i.replace('.py', '') + " | Vérifié")
                        else:
                            print(Fore.YELLOW + i.replace('.py', '') + " | Non vérifié")
            except FileNotFoundError as e:
                print(Fore.RED + "Une erreur inconnue est survenue.\nCode d'erreur : " + str(e))
        else:
            print("Aucun plugin installé.")
    elif cmd.startswith("plugin uninstall"):
        plugin = cmd.split(" ")
        if len(plugin) == 3:
            if os.path.exists(f"Plugins\\{plugin[2]}.py"):
                os.remove(f"Plugins\\{plugin[2]}.py")
                print(Fore.GREEN + "Plugin supprimé.")
            else:
                print(Fore.RED + "Erreur \"plugin\": ce plugin n'existe pas ou n'est pas installé.")
        else:
            print(Fore.RED + "Erreur \"plugin\": la commande \"plugin uninstall\" doit être suivie du nom du plugin.")
    elif cmd == "check update":
        print(Fore.YELLOW + "Vérification des mises à jour...")
        with requests.get("https://raw.githubusercontent.com/automap-organization/automap/main/appinfo.json") as r:
            data = json.loads(r.text)
            if data["latest-version"] != version:
                os.system("cls")
                print(Fore.RED + "Mise à jour disponible !")
                print("Version actuelle : " + version)
                print("Version disponible : " + data["latest-version"])
                print("Voulez-vous télécharger la mise à jour ? (O/N)")
                if input(">").upper() == "O":
                    webbrowser.open(f"https://github.com/automap-organization/automap/releases/download/{data['latest-version']}/automap.exe")
            else:
                print(Fore.GREEN + "Aucune mise à jour disponible.")
    else:
        print(f"Erreur \"Cmd\": la commande {cmd} n'existe pas ou est mal écrite.")
    