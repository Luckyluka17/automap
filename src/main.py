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

version = "0.1 alpha"

print(f"""Automap [Version {version}]
Created by Luckyluka17
Powered by Folium
""")

maplist = []
selectedmap = []
selectedmap1 = ""
listpoints = []

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
addmarker : Ajoute un marqueur
delmarker : Supprime un marqueur
credits : Affiche les crédits
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
                    folium.Marker(location=i).add_to(carte)
                carte.save(f"{selectedmap1}.html")
                print(f"Sauvegarde de {selectedmap1} terminée.")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print("Erreur \"map\": aucune carte n'est sélectionnée.")
    elif cmd == "clear":
        os.system("cls")
    elif cmd.startswith("addmarker"):
        addpin = cmd.replace(",", "").split(" ")
        if len(addpin) == 3:
            if selectedmap1 in maplist:
                if selectedmap1 != "":
                    listpoints.append([addpin[1], addpin[2]])
                    print("Marqueur ajouté.")
                else:
                    print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée.")
        else:
            print("Erreur \"args\": la commande 'addmarker' doit être suivie de coordonnées.")
    elif cmd == "list markers":
        if selectedmap1 in maplist:
                if selectedmap1 != "":
                    if len(listpoints) != 0:
                        for i in listpoints:
                            print(f"1 - {i[0]}, {i[1]}")
                    else:
                        print("Aucun marqueur n'a été ajouté sur la carte séléctionnée.")
                else:
                    print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
        else:
            print("Erreur \"map\": aucune carte n'est sélectionnée.")
    elif cmd.startswith("delmarker"):
        addpin = cmd.replace(",", "").split(" ")
        if len(addpin) == 3:
            if selectedmap1 in maplist:
                if selectedmap1 != "":
                    try:
                        print("Point supprimé.")
                        listpoints.remove([addpin[1], addpin[2]])
                    except:
                        print("Erreur \"marker\": ce point n'existe pas.")
                else:
                    print("Erreur \"map\": aucune carte n'est sélectionnée. Pour en sélectionner une, utilisez la commande \"select\"")
            else:
                print("Erreur \"map\": aucune carte n'est sélectionnée.")
        else:
            print("Erreur \"args\": la commande 'addmarker' doit être suivie de coordonnées.")
    elif cmd == "credits":
        print("""- Développeur : Luckyluka17
- Version : {version}
- Carte : Esri""")
    else:
        errorcmd = cmd.split(" ")
        print(f"Erreur \"Cmd\": la commande {errorcmd[0]} n'existe pas ou est mal écrit.")
    