"""
Plugin créé par Luckyluka17
Version 0.1 (alpha)
Permet d'obtenir une meilleure interface pour régler les paramètres d'automap
"""
from colorama import Fore, init
from tkinter import ttk
import tkinter as tk
import json
import os
from tkinter.messagebox import showinfo, showerror, showwarning

window = tk.Tk()

terminalcolor = "5"
colorpoints = "red"
path_ = os.path.abspath(os.getcwd())

os.chdir(path_.replace("\\plugins\\better_settings.py", ""))

def save():
    if cb1.get() == "" or cb2.get() == "":
        showwarning("Erreur", "Veuillez choisir une couleur pour chaque élément.")
    else:
        if cb2.get() == "Rouge":
            terminalcolor = "1"
        elif cb2.get() == "Vert":
            terminalcolor = "2"
        elif cb2.get() == "Bleu":
            terminalcolor = "3"
        elif cb2.get() == "Jaune":
            terminalcolor = "4"
        elif cb2.get() == "Blanc":
            terminalcolor = "5"
        else:
            terminalcolor = "5"

        if cb1.get() == "Rouge":
            colorpoints = "red"
        elif cb1.get() == "Vert":
            colorpoints = "green"
        elif cb1.get() == "Bleu":
            colorpoints = "blue"
        else:
            colorpoints = "red"

        with open("config.json", "w") as f:
            settingdata = {
                "colorterminal": terminalcolor,
                "colorpoints": colorpoints,
            }
            f.write(json.dumps(settingdata))
            f.close()
        print("""Les modifications ont été enregistrés dans le fichier de sauvegarde.
        Pour appliquer les modifications, redémarrez le logiciel.""")
        window.destroy()

window.title("Paramètres d'Automap")
window.geometry("300x160")
window.resizable(False, False)

ttk.Label(
    text="Couleur des points",
    font=("Arial", 15),
).pack()

cb1 = ttk.Combobox(
    values=["Rouge", "Vert", "Bleu"],
    font=("Arial", 10),
    state="readonly",
)
cb1.pack()

ttk.Label(
    text="Couleur de la console",
    font=("Arial", 15),
).pack()

cb2 = ttk.Combobox(
    values=["Rouge", "Vert", "Bleu", "Jaune", "Blanc"],
    font=("Arial", 10),
    state="readonly",
)
cb2.pack()

ttk.Label(
    text="",
    font=("Arial", 15),
).pack()

ttk.Button(
    text="Valider & quitter",
    command=save
).pack()

window.mainloop()