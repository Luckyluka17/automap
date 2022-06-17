from tkinter import ttk
import tkinter as tk
import os
from tkinter.messagebox import showinfo, showerror
import webbrowser
import json


os.chdir(os.getcwd() + "/src")
data = {}


def create():
    if entry1.get() == "" or entry2.get() == "":
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        cb1.state(['!alternate'])
    else:
        showerror("Erreur", "Veuillez d'abord fermer la carte actuelle avant de créer une nouvelle carte.")

def fermer():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    cb1.state(['!alternate'])
    showinfo("Information", "La carte a été fermée.")

def save():
    if entry1.get() != "":
        data["name"] = entry1.get()
        if entry2.get() != "":
            data["points"] = str(entry2.get())

        else:
            data["points"] = []

        if str(cb1.state()).replace("'", "").replace(",", "") == "(selected)":
            data["satellite"] = True
        else:
            data["satellite"] = False

        if cp1.get() != "":
            data["marker_color"] = cp1.get()

        with open("carte.json", "w") as f:
            json.dump(data, f)
            f.close()

        showinfo("Information", "La carte a été sauvegardée. Pour la générer, veuillez ouvrir Automap CMD et entez la commande \"generate\".")
    else:
        showerror("Erreur", "Veuillez d'abord entrer un nom à la carte.")


def test():
    print(cb1.state())



window = tk.Tk()
version = "0.1 alpha"

window.title("Automap GUI - v" + version)
window.geometry("400x400")
window.iconbitmap("icon.ico")
window.resizable(False, False)

menubar = tk.Menu(window, tearoff=0)
menubar_file = tk.Menu(menubar, tearoff=0)
menubar_automap = tk.Menu(menubar, tearoff=0)
menubar_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Fichier", menu=menubar_file)
menubar.add_cascade(label="Outils d'automap", menu=menubar_automap)
menubar.add_cascade(label="Aide", menu=menubar_help)
menubar_file.add_command(label="Créer une carte", command=create)
menubar_file.add_command(label="Fermer une carte", command=fermer)
menubar_file.add_command(label="Sauvegarder la carte", command=save)
menubar_file.add_separator()
menubar_file.add_command(label="Quitter", command=window.quit)
menubar_automap.add_command(label="Créer une liste de points", command=window.quit)
menubar_help.add_command(label="Documentation", command=lambda: webbrowser.open("https://github.com/automap-organization/automap/wiki"))
menubar_help.add_command(label="Serveur Discord", command=lambda: webbrowser.open("https://discord.gg/wwPRdFe5Ua"))

texte1 = ttk.Label(
    window,
    text="\nNom de la carte",
    font=("Calibri", 15),
)
texte1.pack()

entry1 = ttk.Entry(
    window,
    width=30,
    font=("Calibri", 15),
)
entry1.pack()

texte2 = ttk.Label(
    window,
    text="\nPoints sur la carte",
    font=("Calibri", 15),
)
texte2.pack()

entry2 = ttk.Entry(
    window,
    width=30,
    font=("Calibri", 15),
)
entry2.pack()

texte3 = ttk.Label(
    window,
    text="\nCouleur des points",
    font=("Calibri", 15),
)
texte3.pack()

cp1 = ttk.Combobox(
    window,
    values=["Rouge", "Vert", "Bleu"],
    font=("Calibri", 15),
    state="readonly",
)
cp1.pack()

texte4 = ttk.Label(
    window,
    text="\nOptions supplémentaires",
    font=("Calibri", 15),
)
texte4.pack()

cb1 = ttk.Checkbutton(
    window,
    text="Mode satellite",
    variable=tk.BooleanVar(),
    onvalue=True,
    offvalue=False,
)
cb1.pack()
cb1.state(["!alternate"])

ttk.Label(
    window,
    text=" ",
    font=("Calibri", 15),
).pack()


bouton1 = ttk.Button(
    window,
    text="Sauvegarder la carte",
    command=save,
)
bouton1.pack()

window.config(menu=menubar)
window.mainloop()