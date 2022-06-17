"""
Plugin créé par Luckyluka17
Version 0.1 (alpha)
Permet de créer une carte automap GUI à partir d'un fichier json.
"""
from tkinter import filedialog as fd
import tkinter as tk
import os
import folium
import json
from colorama import Fore, Back, Style, init

init(autoreset=True)

window = tk.Tk()
window.withdraw()
window.update()

fichier = None

while fichier is None:
    fichier = fd.askopenfile(mode='r', filetypes=[('Carte Automap GUI', '*.json')])

os.system("cls")

print(Fore.YELLOW + "Veuillez patienter, la carte est en cours de génération...")
fichier = os.path.abspath(fichier.name)

with open(fichier, 'r') as f:
    data = json.load(f)
    f.close()

if data["satellite"] == True:
    m = folium.Map()
    tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
    ).add_to(m)
else:
    m = folium.Map()

try:
    for point in data["points"]:
        folium.Marker(point.replace("\"", ""), folium.Icon(icon_color=data["marker_color"])).add_to(m)
except ValueError as e:
    print(Fore.RED + "Erreur: " + str(e))

m.save(data["name"] + ".html")