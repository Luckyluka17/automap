from tkinter import ttk
import tkinter as tk
import os
from tkinter.messagebox import showinfo, showerror
import webbrowser
import folium
import requests
from bs4 import BeautifulSoup


# os.chdir(os.getcwd() + "/src/APP")
data = {}
iconlist = []

# Récupérer la liste des icones
with requests.get("https://getbootstrap.com/docs/3.3/components/") as r:
    soup = BeautifulSoup(r.content, "html.parser")
    for i in soup.find_all(class_="bs-glyphicons-list"):
        iconlist.append(i.text.replace("glyphicon-", "").replace("glyphicon", "").replace("     ", "|").replace("    ", "").replace("  ", ""))
iconlist = str(iconlist).replace("[", " ").replace("]", "").replace("'", "").split("|")


window = tk.Tk()
version = "1.0 alpha"
len_markers = 0

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
                gestion_points.insert(parent='', index=len_markers, iid=len_markers, text='', values=(entry2.get(),'Aucun',len_markers))
            else:
                gestion_points.insert(parent='', index=len_markers, iid=len_markers, text='', values=(entry2.get(),cb3.get(),len_markers))
            window1.destroy()

    window1 = tk.Tk()
    window1.title("Ajouter un point")
    window1.iconbitmap("icon.ico")
    window1.resizable(False, False)
    window1.geometry("300x150")

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
                    
                if cb2.get() != "Normale":
                    tile = folium.TileLayer(
                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                attr = 'Esri',
                                name = 'Esri Satellite',
                                overlay = False,
                                control = True
                    ).add_to(map)

                for child in gestion_points.get_children():
                    p = gestion_points.item(child)["values"][0].replace(" ", "").split(",")
                    if gestion_points.item(child)["values"][1] != "Aucun":
                        folium.Marker([float(p[0]), float(p[1])], icon=folium.Icon(color='red', prefix='glyphicon', icon=gestion_points.item(child)["values"][1])).add_to(map)
                    else:
                        folium.Marker([float(p[0]), float(p[1])], icon=folium.Icon(color='red')).add_to(map)
                try:
                    map.save(f"{entry1.get()}.html")
                    showinfo("Succès", "Votre carte a été enregistrée !")
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
window.iconbitmap("icon.ico")
window.resizable(False, False)

menubar = tk.Menu(window, tearoff=0)
menubar_file = tk.Menu(menubar, tearoff=0)
menubar_automap = tk.Menu(menubar, tearoff=0)
menubar_theme = tk.Menu(menubar, tearoff=0)
menubar_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Fichier", menu=menubar_file)
menubar.add_cascade(label="Automap", menu=menubar_automap)
menubar.add_cascade(label="Thèmes", menu=menubar_theme)
menubar.add_cascade(label="Aide", menu=menubar_help)
menubar_file.add_command(label="Sauvegarder la carte", command=create_map)
menubar_file.add_command(label="Rénitialiser", command=lambda:(
    gestion_points.delete(*gestion_points.get_children()),
    entry1.delete(0, 'end')
))
menubar_file.add_separator()
menubar_file.add_command(label="Quitter", command=window.quit)
menubar_automap.add_command(label="Ajouter un point", command=aj_point)
menubar_automap.add_command(label="Supprimer un point", command=del_item)
menubar_automap.add_separator()
menubar_automap.add_command(label="Revenir à la CMD", command=lambda:(os.startfile(os.getcwd() + "\\cmd.exe")))
menubar_help.add_command(label="Github", command=lambda: webbrowser.open("https://github.com/automap-organization/automap"))
menubar_help.add_command(label="Documentation", command=lambda: webbrowser.open("https://github.com/automap-organization/automap/wiki"))
menubar_help.add_command(label="Serveur Discord", command=lambda: webbrowser.open("https://discord.gg/wwPRdFe5Ua"))
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
    values=["Normale", "Satellite"],
    state="readonly"
)
cb2.place(x=25, y=175)

gestion_points = ttk.Treeview(
    window
)
gestion_points['columns']=('Coordonées', 'Icone', 'Numéro')
gestion_points.column('#0', width=0, stretch=False)
gestion_points.column('Coordonées', anchor='center', width=300)
gestion_points.column('Icone', anchor='center', width=100)
gestion_points.column('Numéro', anchor='center', width=100)

gestion_points.heading('#0', text='', anchor='center')
gestion_points.heading('Coordonées', text='Coordonées', anchor='center')
gestion_points.heading('Icone', text='Icone', anchor='center')
gestion_points.heading('Numéro', text='Numéro', anchor='center')

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