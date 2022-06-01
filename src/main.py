"""
Développé par Luckyluka17.
Logiciel gratuit et open source.
"""

import os

print("Chargement des modules...")
try:
    import folium
    os.system("cls")
except ImportError:
    print("Le module folium n'est pas installé, installez le avec la commande :\npip install folium")
    print("\nAppuyez sur entrée pour quitter")
    os.system("pause >nul")
    exit()

version = "0.2"

if not os.name == "nt":
    os.system("clear")
    print("""Nous avons detecté que l'application s'éxécute sur un système non windows.
    Il est possible que certaines commandes ne fonctionnent pas comme prévu.
    (une version linux est en cours de développement)
""")

os.system(f"title Automap v{version}")
print(f"""Automap [Version {version}]
Created by Luckyluka17
Powered by Folium
""")

maplist = []
selectedmap = []
selectedmap1 = ""
listpoints = []
colorterminal = "5"
colorpoints = "blue"

if os.path.exists("config.txt"):
    with open("config.txt", "r") as f:
        data = f.read().replace(" ", "").split("-")
        colorterminal = str(data[0])
        colorpoints = str(data[1])
        f.close()
        del data
else:
    with open("config.txt", "w") as f:
        f.write(f"{colorterminal}-{colorpoints}")
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
    cmd = str(input("=>"))

    if cmd == "help":
        print("""help : Affiche l'aide
create : Crée une nouvelle carte
select : Sélectionne une carte
delete : Supprime une carte
save : Sauvegarde la carte
list maps : Affiche la liste des cartes créées
list markers : Affiche la liste des points sur la carte séléctionnée
list icons : Affiche la liste des icones pour les points
addmarker : Ajoute un marqueur
delmarker : Supprime un marqueur
credits : Affiche les crédits
settings : Affiche le menu des paramètres
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
                print(f"Erreur \"map\": une carte a ce nom existe déjà. Pour la supprimer, utilisez la commande \"delete {createdmap[1]}\"")
        else:
            print("Erreur \"args\": la commande 'create' doit être suivie uniquement d'un nom de carte.")
    elif cmd == "list maps":
        if len(maplist) != 0:
            for i in maplist:
                ind = int(maplist.index(i))
                ind = maplist[ind]
                if i == selectedmap1:
                    print(f"- {ind} (Selectionnée)")
                else:
                    print(f"- {ind}")
        else:
            print("Aucune carte n'a été créée.")
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
                print(f"Erreur \"map\": une carte a ce nom n'existe pas.")
        else:
            print("Erreur \"args\": la commande 'delete' doit être suivie uniquement d'un nom de carte.")
    elif cmd.startswith("select"):
        selectedmap = cmd.split(" ")
        if len(selectedmap) == 2:
            if selectedmap[1] in maplist:
                if selectedmap[1] != selectedmap1 and selectedmap1 != "":
                    print("ATTENTION : séléctionner une autre carte efface les données de la carte précédemment sélectionnée !\nVoulez-vous continuer ? (y/n)")
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
                print(f"Erreur \"map\": une carte à ce nom n'existe pas.")
        else:
            print("Erreur \"args\": la commande 'select' doit être suivie uniquement d'un nom de carte.")
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
                    print("Erreur \"save\": la carte n'a pas pu être sauvegardée.")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print("Erreur \"map\": aucune carte n'est sélectionnée.")
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
                    print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée.")
        else:
            print("Erreur \"args\": la commande 'addmarker' doit être suivie de coordonnées.")
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
                        print("Erreur \"marker\": les coordonnées entrées ne sont pas valides.")
                    else:
                        try:
                            folium.PolyLine(markersline, color=colorpoints, weight=2.5, opacity=0.8).add_to(carte)
                            print("Ligne créée.")
                        except RecursionError:
                            print("Erreur \"line\": la ligne doit avoir 5 points ou plus.")
                        except:
                            print("Erreur \"line\": la ligne n'a pas pu être créée.")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print("Erreur \"map\": aucune carte n'est sélectionnée.")
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
                        print("Aucun marqueur n'a été ajouté sur la carte séléctionnée.")
                else:
                    print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print("Erreur \"map\": aucune carte n'est sélectionnée.")
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
                        print("Erreur \"marker\": ce point n'existe pas.")
                else:
                    print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée.")
        else:
            print("Erreur \"args\": la commande 'delmarker' doit être suivie de coordonnées (et d'un nom de logo si vous en avez mis un).")
    elif cmd == "credits":
        print("""- Développeur : Luckyluka17
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

            with open("config.txt", "w") as f:
                f.write(f"{colorterminal}-{colorpoints}")
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

            with open("config.txt", "w") as f:
                f.write(f"{colorterminal}-{colorpoints}")
                f.close()
    elif cmd == "list icons":
        print("""La liste des icons pour les points est disponible à cette adresse :
https://getbootstrap.com/docs/3.3/components/""")
    else:
        errorcmd = cmd.split(" ")
        print(f"Erreur \"Cmd\": la commande {errorcmd[0]} n'existe pas ou est mal écrit.")
    