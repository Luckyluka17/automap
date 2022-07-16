import json
import os
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning

import folium
import requests
from bs4 import BeautifulSoup
from pypresence import Presence

try:
    os.chdir(os.getcwd() + "/src/APP")
except:
    pass

data = {}
iconlist = []


window = tk.Tk()
version = "1.3"
len_markers = 0

check_updates1 = tk.BooleanVar()
open_file_directory1 = tk.BooleanVar()
portable_mode1 = tk.BooleanVar()
discord_rpc1 = tk.BooleanVar()

try:
    # Récupérer la liste des icones
    with requests.get("https://getbootstrap.com/docs/3.3/components/") as r:
        soup = BeautifulSoup(r.content, "html.parser")
        for i in soup.find_all(class_="bs-glyphicons-list"):
            iconlist.append(i.text.replace("glyphicon-", "").replace("glyphicon", "").replace("     ", "|").replace("    ", "").replace("  ", ""))
    iconlist = str(iconlist).replace("[", " ").replace("]", "").replace("'", "").split("|")

    # Récupération des informations du serveur
    with requests.get("https://raw.githubusercontent.com/automap-organization/automap/main/appinfo.json") as r:
        data = json.loads(r.text)
except requests.exceptions.ConnectionError as e:
    window.withdraw()
    showerror("Erreur de connexion au serveur", "Le client Automap n'a pas pu ce connecter au serveur.Merci de bien vouloir réessayer.\nErreur : " + str(e))
    window.destroy()

if os.path.exists("app_settings.json"):
    try:
        with open("app_settings.json", "r") as f:
            settings = json.loads(f.read())
            f.close()
    except json.decoder.JSONDecodeError:
        window.withdraw()
        showwarning("Fichier corrompu", "Le fichier où sont stockés vos paramètres est corrompu. En conséquent, vos paramètres vont être rénitialisés.")
        window.deiconify()
        with open("app_settings.json", "w") as f:
            settings = {
                "check_updates": True,
                "open_file_directory": False,
                "portable_mode": False,
                 "discord_rpc": True,
            }
            json.dump(settings, f)
            f.close()
        with open("app_settings.json", "r") as f:
            settings = json.loads(f.read())
            f.close()
    except Exception as e:
        window.withdraw()
        showerror("Erreur", "Une erreur inconnu c'est produite :\n"+ str(e))
        window.deiconify()
else:
    with open("app_settings.json", "a") as f:
        settings = {
            "check_updates": True,
            "open_file_directory": False,
            "portable_mode": False,
             "discord_rpc": True,
        }
        json.dump(settings, f)
        f.close()
    with open("app_settings.json", "r") as f:
        settings = json.loads(f.read())
        f.close()

def apply_settings():
    settings2apply = {
        "check_updates": check_updates1.get(),
        "open_file_directory": open_file_directory1.get(),
        "portable_mode": portable_mode1.get(),
        "discord_rpc": discord_rpc1.get(),
    }
    with open("app_settings.json", "w") as f:
        json.dump(settings2apply, f)
        f.close()

def reset_settings():
    settings2apply = {
        "check_updates": True,
        "open_file_directory": False,
        "portable_mode": False,
    }
    with open("app_settings.json", "w") as f:
        json.dump(settings2apply, f)
        f.close()
    portable_mode1.set(False)
    check_updates1.set(True)
    open_file_directory1.set(False)
    showinfo("Succès", "Les paramètres ont été rénitialisés.")


check_updates = settings["check_updates"]
check_updates1.set(settings["check_updates"])
open_file_directory1.set(settings["open_file_directory"])
portable_mode1.set(settings["portable_mode"])
discord_rpc1.set(settings["discord_rpc"])

if settings["discord_rpc"] == True:
    try:
        RPC = Presence(client_id=997483901406687302)
        RPC.connect()
        RPC.update(
            details="✏️ Édite une carte",
            state=f"🖥️ Automap v{version}",
            large_image="logo",
            large_text="Créé par Luckyluka17"
        )
    except:
        print("Discord n'est pas détecté ou n'est pas ouvert.")

if check_updates == True:
    if data["latest-version"] > version:
        window.withdraw()
        showinfo("Nouvelle version", "Une nouvelle version du logiciel est disponible sur le github.\nNous vous recommandons de l'installer afin de bénéficier des fonctionnalités les plus récentes.")
        window.deiconify()


def check_updates():
    if data["latest-version"] > version:
        showinfo("Mises à jour", "Une nouvelle version est disponible.")
    else:
        showinfo("Mises à jour", "Vous possèdez la dernière version.")

def startcmd():
    try:
        os.startfile(os.getcwd() + "\\cmd.exe")
    except FileNotFoundError as e:
        showerror("Erreur", str(e) + "\nVérifiez que vous avez tout les fichiers. Si le problème persiste, réinstallez automap.")



def del_item():
    global len_markers
    try:
        selected = gestion_points.focus()
        gestion_points.delete(selected)
        len_markers = len_markers - 1
    except:
        showerror("Erreur de points", "Veuillez séléctionner un point à supprimer.")

def aj_point():
    global len_markers
    def create_point():
        global len_markers
        if entry2.get() == "" or entry2.get() == " " or not "," in entry2.get():
            showerror("Erreur", "Veuillez entrer des coordonnées valides.")
        else:
            len_markers = len_markers + 1
            if cb3.get() == "":
                gestion_points.insert(parent='', index=len_markers, iid=len_markers, text='', values=(entry2.get(),'Aucun',entry3.get()))
            else:
                gestion_points.insert(parent='', index=len_markers, iid=len_markers, text='', values=(entry2.get(),cb3.get(),entry3.get()))
            window1.destroy()

    window1 = tk.Tk()
    window1.title("Ajouter un point")
    window1.iconbitmap("icon.ico")
    window1.resizable(False, False)
    window1.geometry("300x200")

    ttk.Label(
        window1,
        text="Coordonnées",
        font=("Calibri", 14)
    ).pack()

    entry2 = ttk.Entry(
        window1,
        width=40
    )
    entry2.pack()

    ttk.Label(
        window1,
        text="Icone (facultatif)",
        font=("Calibri", 14)
    ).pack()

    cb3 = ttk.Combobox(
        window1,
        values=iconlist,
        state="readonly"
    )
    cb3.pack()

    ttk.Label(
        window1,
        text="Texte du popup (facultatif)",
        font=("Calibri", 14)
    ).pack()

    entry3 = ttk.Entry(
        window1,
        width=40
    )
    entry3.pack()

    bouton1 = ttk.Button(
        window1,
        text="Valider",
        command=create_point
    )
    bouton1.pack(pady=10)


    window1.mainloop()

def create_map():
    map = folium.Map()
    if not entry1.get() == "" or not entry1.get() == " ":
        if not cb1.get() == "":
            if not cb2.get() == "":
                if cb1.get() == "Rouge":
                    color = "red"
                elif cb2.get() == "Vert":
                    color = "green"
                else:
                    color = "blue"
                    
                if cb2.get() == "Satellite":
                    tile = folium.TileLayer(
                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                attr = 'Esri',
                                name = 'Esri Satellite',
                                overlay = False,
                                control = True
                    ).add_to(map)
                elif cb2.get() == "Normale (mode clair)":
                    folium.TileLayer('cartodbpositron').add_to(map)
                else:
                    folium.TileLayer('cartodbdark_matter').add_to(map)

                for child in gestion_points.get_children():
                    p = gestion_points.item(child)["values"][0].replace(" ", "").split(",")
                    if gestion_points.item(child)["values"][1] != "Aucun":
                        folium.Marker([float(p[0]), float(p[1])], popup=gestion_points.item(child)["values"][2], icon=folium.Icon(color=color, prefix='glyphicon', icon=gestion_points.item(child)["values"][1])).add_to(map)
                    else:
                        folium.Marker([float(p[0]), float(p[1])], icon=folium.Icon(color=color), popup=gestion_points.item(child)["values"][2]).add_to(map)
                try:
                    try:
                        os.mkdir("cartes")
                    except:
                        print("Le dossier cartes est déjà présent.")
                    map.save(f"{os.getcwd()}\\cartes\\{entry1.get()}.html")
                    showinfo("Succès", f"Votre carte a été enregistrée !")
                    if open_file_directory1.get() == False:
                        os.startfile(f"{os.getcwd()}\\cartes\\{entry1.get()}.html")
                    else:
                        os.system(f"explorer {os.getcwd()}\\cartes")
                except:
                    showerror("Erreur", "La carte n'a pas pu être créée.")
            else:
                showerror("Erreur", "Veuillez choisir le type de carte.")
        else:
            showerror("Erreur", "Veuillez choisir la couleur des points.")
    else:
        showerror("Erreur", "Veuillez choisir un nom pour la carte.")

style = ttk.Style()

window.title("Automap GUI - v" + version)
window.geometry("800x400")
if settings["portable_mode"] != True:
    window.iconbitmap("icon.ico")
window.resizable(False, False)

menubar = tk.Menu(window, tearoff=0)
menubar_file = tk.Menu(menubar, tearoff=0)
menubar_automap = tk.Menu(menubar, tearoff=0)
menubar_settings = tk.Menu(menubar, tearoff=0)
menubar_theme = tk.Menu(menubar, tearoff=0)
menubar_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Fichier", menu=menubar_file)
menubar.add_cascade(label="Paramètres", menu=menubar_settings)
menubar.add_cascade(label="Automap", menu=menubar_automap)
menubar.add_cascade(label="Thèmes", menu=menubar_theme)
menubar.add_cascade(label="Aide", menu=menubar_help)
menubar_file.add_command(label="Sauvegarder la carte", command=create_map)
menubar_file.add_command(label="Réinitialiser", command=lambda:(
    gestion_points.delete(*gestion_points.get_children()),
    entry1.delete(0, 'end')
))
menubar_file.add_command(label="Vérifier les mises à jour", command=check_updates)
menubar_file.add_separator()
menubar_file.add_command(label="Quitter", command=window.quit)
menubar_automap.add_command(label="Ajouter un point", command=aj_point)
menubar_automap.add_command(label="Supprimer un point", command=del_item)
menubar_automap.add_command(label="Créer une ligne", state="disabled")
menubar_automap.add_separator()
if settings["portable_mode"]:
    menubar_automap.add_command(label="Revenir à la CMD", state="disabled")
else:
    menubar_automap.add_command(label="Revenir à la CMD", command=startcmd)
menubar_help.add_command(label="Documentation", command=lambda: webbrowser.open("https://docs.automap.tk"))
menubar_help.add_command(label="Github", command=lambda: webbrowser.open("https://github.com/automap-organization/automap"))
menubar_theme.add_command(label="Normal", command=lambda:(
    style.theme_use("vista"),
    style.map("Treeview")
))
menubar_theme.add_separator()
menubar_theme.add_command(label="Winnative", command=lambda:(
    style.theme_use("winnative"),
    style.map("Treeview")
))
menubar_theme.add_command(label="Xpnative", command=lambda:(
    style.theme_use("xpnative"),
    style.map("Treeview")
))
menubar_settings.add_checkbutton(label="Vérifier les mises à jour à chaque démarrage", variable=check_updates1, command=apply_settings)
menubar_settings.add_checkbutton(label="Ouvrir l'emplacement du fichier", variable=open_file_directory1, command=apply_settings)
menubar_settings.add_checkbutton(label="Mode portable (supression des fichiers facultatifs)", command=apply_settings, variable=portable_mode1)
menubar_settings.add_checkbutton(label="Discord Rich Presence", command=apply_settings, variable=discord_rpc1)
menubar_settings.add_checkbutton(label="Compatibilité Linux (bientôt disponible)", state="disabled")
menubar_settings.add_separator()
menubar_settings.add_command(label="Rénitialiser le fichier JSON des paramètres", command=reset_settings)

ttk.Label(
    window,
    text="Nom de la carte",
    font=("Calibri", 15)
).place(x=30, y=15)

ttk.Label(
    window,
    text="Couleur des points",
    font=("Calibri", 15)
).place(x=17, y=75)

ttk.Label(
    window,
    text="Type de carte",
    font=("Calibri", 15)
).place(x=35, y=140)

ttk.Label(
    window,
    text="Gestionnaire de points",
    font=("Calibri", 15)
).place(x=400, y=15)

entry1 = ttk.Entry(
    window,
    width=25
)

entry1.place(x=20, y=45)

cb1 = ttk.Combobox(
    window,
    values=["Rouge", "Vert", "Bleu"],
    state="readonly"
)
cb1.place(x=25, y=110)

cb2 = ttk.Combobox(
    window,
    values=["Satellite", "Normale (mode clair)", "Normale (mode sombre)"],
    state="readonly"
)
cb2.place(x=25, y=175)

gestion_points = ttk.Treeview(
    window
)
gestion_points['columns']=('Coordonées', 'Icone', 'Texte popup')
gestion_points.column('#0', width=0, stretch=False)
gestion_points.column('Coordonées', anchor='center', width=250)
gestion_points.column('Icone', anchor='center', width=100)
gestion_points.column('Texte popup', anchor='center', width=150)

gestion_points.heading('#0', text='', anchor='center')
gestion_points.heading('Coordonées', text='Coordonées', anchor='center')
gestion_points.heading('Icone', text='Icone', anchor='center')
gestion_points.heading('Texte popup', text='Texte popup', anchor='center')

gestion_points.place(x=275, y=50)

add_point = ttk.Button(
    window,
    text="Ajouter un point",
    command=aj_point
)
add_point.place(x=300, y=290)

del_point = ttk.Button(
    window,
    text="Supprimer un point",
    command=del_item
)
del_point.place(x=420, y=290)

create_map = ttk.Button(
    window,
    text="Créer la carte",
    command=create_map
)
create_map.place(x=50, y=220)

frame = ttk.Frame(
    window
)
frame.place(x=777, y=48)

sb = ttk.Scrollbar(frame, orient="vertical")
sb.pack(side="right", fill="y")

gestion_points.config(yscrollcommand=sb.set)
sb.config(command=gestion_points.yview)

window.config(menu=menubar)
window.mainloop()
