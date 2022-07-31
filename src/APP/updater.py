import os
from tkinter import ttk
import tkinter as tk
from threading import Thread
import wget
from tkinter.messagebox import showinfo
import webbrowser

window = tk.Tk()

app_name = "Automap"

os.chdir(os.getcwd())
os.system("taskkill /f /im app_portable.exe")
wget.download('https://iconarchive.com/download/i43008/oxygen-icons.org/oxygen/Apps-system-software-update.ico', 'icon_updater.ico')

window.title("Automap Updater")
window.iconbitmap("icon_updater.ico")
window.geometry("300x150")
window.resizable(False, False)

menubar = tk.Menu(tearoff=0)
file_menu = tk.Menu(menubar, tearoff=0)
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Fichier", menu=file_menu)
menubar.add_cascade(label="Aide complémentaire", menu=help_menu)
file_menu.add_command(label="Télécharger manuellement", command=lambda: webbrowser.open("https://raw.githubusercontent.com/automap-organization/automap/main/src/exe/app_portable.exe"))
file_menu.add_command(label="À propos de ce logiciel", command=lambda: showinfo("À propos de ce logiciel", "Développé avec AutoUpdater Generator"))
file_menu.add_separator()
file_menu.add_command(label="Fermer l'Auto Updater", command=lambda: window.destroy())
help_menu.add_command(label="Signaler un problème", command=lambda: webbrowser.open("mailto:contact@automap.tk"))
help_menu.add_command(label="Voir la license", command=lambda: webbrowser.open("https://raw.githubusercontent.com/automap-organization/automap/main/LICENSE"))

def update():
    pb.pack()
    pb.start(15)
    text1.pack()
    bouton1.place(x=300, y=300)
    if os.path.exists("app_portable.exe"):
        os.remove("app_portable.exe")
    wget.download('https://raw.githubusercontent.com/automap-organization/automap/main/src/exe/app_portable.exe', 'app_portable.exe')
    window.withdraw()
    os.startfile("app_portable.exe")
    showinfo("Mise à jour", "La mise à jour a été installée.")
    window.destroy()
    

ttk.Label(
    text="Mise à jour disponible",
    font=("Calibri", 15)
).pack()

ttk.Label(
    text="Une nouvelle version est disponible.\n",
    font=("Calibri", 11)
).pack()

text1 = ttk.Label(
    text="Veuillez patienter (ne fermez pas cette fenêtre !).",
    font=("Calibri", 10)
)

pb = ttk.Progressbar(
    length=200,
    mode="indeterminate"
)

bouton1 = ttk.Button(
    text="Installer la mise à jour",
    cursor="hand2",
    command=Thread(target=update).start # Mise à jour avec un Thread
)
bouton1.place(x=170, y=100)

window.config(menu=menubar)
window.mainloop()