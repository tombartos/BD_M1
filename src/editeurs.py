import tkinter as tk
from datetime import date
from query import *
import accueil

import tkinter.font as tkfont
import tkinter.ttk as ttk

class Editeurs:
    """Ecran de la table editeurs avec toutes les operations qui lui correspondent"""
    def __init__(self, window):
        self.window = window

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=10)

        # Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM EDITEURS")
        
        # Bouton retour
        font1 = tkfont.Font(family="Times New Roman", size=18)
        btnretour = tk.Button(self.window, text="Retour", font=font1, command=self.commandback)
        btnretour.grid(column=0, row=0, sticky="nw")

        # Label en haut de l'ecran nom de la table
        font0 = tkfont.Font(family="Times New Roman", size=30, weight="bold")
        lbl1 = tk.Label(self.window, text="Editeurs", font=font0)
        lbl1.grid(column=1, row=0)

        # Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Times New Roman', 17))
        style.configure("Treeview", font=('Calibri', 15))

        # Creation tableau
        self.table = ttk.Treeview(self.window, height=22)
        self.table.grid(column=0, row=1, columnspan=3)
        self.table['columns'] = ['NomEdit', 'Patron', 'Pays']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('NomEdit', width=200)
        self.table.column('Patron', width=200)
        self.table.column('Pays', width=140)

        for e in self.table['columns']:
            self.table.heading(e, text=e)

        self.table.heading('NomEdit', text='NomEdit')
        self.table.heading('Patron', text='Patron')
        self.table.heading('Pays', text='Pays')

        # Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

        # bind de la table
        self.table.bind('<ButtonRelease-1>', self.commandSelection)
        
        # Variable pour recuperer un NomEditeur
        self.nomediteur = None

        # Boutons nouvelle entree, supprimer et recherche
        self.ButNew = tk.Button(self.window, text='Nouveau Editeur', font=font1, command=self.commandNew)
        self.ButNew.grid(row=2, column=0, sticky='e')
        
        self.ButDel = tk.Button(self.window, text='Supprimer Editeur', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.grid(row=2, column=1)

        self.ButSearch = tk.Button(self.window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.grid(row=2, column=2)

        # Label Nouvelle entree
        self.lblnew = tk.Label(self.window, text="Nouveau Editeur", font=font0)

        # Frame pour les entrees des nouveaux attributs qu'on cache au debut
        self.newframe = tk.Frame(self.window)

        # Attributs pour nouvelle entree
        font2 = tkfont.Font(family="Calibri", size=25)
        self.lblnewNomEdit = tk.Label(self.newframe, text="Nom", font=font2)
        self.lblnewNomEdit.grid(row=0, sticky='nsew')
        self.entnewNomEdit = tk.Entry(self.newframe)
        self.entnewNomEdit.grid(row=1)

        self.lblnewPatron = tk.Label(self.newframe, text="Patron", font=font2)
        self.lblnewPatron.grid(row=2, column=0)
        self.entnewPatron = tk.Entry(self.newframe)
        self.entnewPatron.grid(row=3)

        self.lblnewPays = tk.Label(self.newframe, text="Pays", font=font2)
        self.lblnewPays.grid(row=4)
        self.entnewPays = tk.Entry(self.newframe)
        self.entnewPays.grid(row=5)

        self.btnconfEditeur = tk.Button(self.newframe, text='Confirmer', font=font1, command=self.commandConfNew)
        self.btnconfEditeur.grid(row=6)

        # Creation du label indiquant par la suite si l'operation a reussie ou non
        self.lblnewstate = tk.Label(self.newframe, text="")
        self.lblnewstate.grid(row=7)

        # Label Rechercher
        self.lblsearch = tk.Label(self.window, text="Rechercher", font=font0)

        # Frame pour les entrees de la recherche
        self.searchframe = tk.Frame(self.window)

        # Attributs Recherche
        # Nom Entry
        self.lblsearchNomEdit = tk.Label(self.searchframe, text="Nom", font=font2)
        self.lblsearchNomEdit.grid(row=0)
        self.entsearchNomEdit = tk.Entry(self.searchframe)
        self.entsearchNomEdit.grid(row=1)

        # Patron Entry
        self.lblsearchPatron = tk.Label(self.searchframe, text="Patron", font=font2)
        self.lblsearchPatron.grid(row=2)
        self.entsearchPatron = tk.Entry(self.searchframe)
        self.entsearchPatron.grid(row=3)

        # Pays Entry
        self.lblsearchPays = tk.Label(self.searchframe, text="Pays", font=font2)
        self.lblsearchPays.grid(row=4)
        self.entsearchPays = tk.Entry(self.searchframe)
        self.entsearchPays.grid(row=5)

        # Bouton Confirmer Recherche
        self.btnconfSearch = tk.Button(self.searchframe, text="Rechercher", font=font1, command=self.commandConfSearch)
        self.btnconfSearch.grid(row=6)

        # Label Erreur recherche vide
        self.lblconfSearch = tk.Label(self.searchframe, text="Veuillez remplir au moins un champ", fg='red')
        
    def updatetable(self):
        """Met à jour l'affichage du tableau"""
        # Suppression des elements
        for line in self.table.get_children():
            self.table.delete(line)

        # Remplissage avec les nouveaux elements
        req = doQuery(self.conn, "SELECT * FROM EDITEURS")
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

    def commandNew(self):
        """Affiche l'interface pour ajouter une nouvelle entree a la table"""
        self.updatetable()  # On fait une update au cas ou on etait dans recherche pour reafficher toute la table
        self.ButSearch.configure(state="active")
        self.ButNew.configure(state="disabled")
        self.searchframe.grid_forget()
        self.newframe.grid(column=3, row=1, sticky="nsew")
        self.lblsearch.grid_forget()
        self.lblnew.grid(column=3, row=0)
    
    def commandSearch(self):
        """Affiche l'interface pour effectuer une recherche"""
        self.ButNew.configure(state="active")
        self.ButSearch.configure(state="disabled")
        self.newframe.grid_forget()
        self.searchframe.grid(column=3, row=1, sticky="nsew")
        self.lblnew.grid_forget()
        self.lblsearch.grid(column=3, row=0)

    def commandDel(self):
        """Supprime l'entree selectionnee"""
        # Vérification qu'il y ait une ligne sélectionnée
        if self.nomediteur is not None:
            try:
                doNoReturnQuery(self.conn, f"DELETE FROM Editeurs WHERE NomEdit = '{self.nomediteur}';")
                self.lblnewstate.config(text="Opération Réussie", fg="green")
                self.updatetable()
                self.ButDel.configure(state="disabled")
            except:
                self.lblnewstate.config(text="Opétation échouée, revoyez les entrées", fg="red")
                doNoReturnQuery(self.conn, "ROLLBACK;")
    
    def commandSelection(self, event):
        """récupère le NomEdit de la ligne sélectionnée."""
        # récupération de la ligne
        value = self.table.item(self.table.selection())['values']
        
        # Vérification si la ligne est vide ou non
        if value:
            # Récupération de la valeur de NomEdit
            if value[0] != self.nomediteur:
                self.nomediteur = value[0]
                self.ButDel.configure(state="normal")
            # Déselectionne si la ligne est resélectionnée
            else:
                self.table.selection_toggle(self.table.selection())
                self.nomediteur = None
                self.ButDel.configure(state="disabled")
        else:
            self.nomediteur = None
            self.ButDel.configure(state="disabled")

    def commandConfNew(self):
        """Confirme un nouveau editeur (envoie la requete SQL a la BDD pour ajouter une entree a la table Editeurs)"""
        # Recuperation des valeurs de la nouvelle entree
        nom = self.entnewNomEdit.get()
        patron = self.entnewPatron.get()
        pays = self.entnewPays.get()
        
        try:
            doNoReturnQuery(self.conn, f"INSERT INTO Editeurs (NomEdit, Patron, Pays) VALUES('{nom}', '{patron}', '{pays}');")
            self.lblnewstate.config(text="Opération Réussie", fg="green")
            self.updatetable()
        except:
            self.lblnewstate.config(text="Opétation échouée, revoyez les entrées", fg="red")
            doNoReturnQuery(self.conn, "ROLLBACK;")
        
    def commandConfSearch(self):
        """Confirme une recherche (envoie la requete SQL et affiche la reponse dans le tableau)"""
        # Construction de la requete
        req = "SELECT * FROM Editeurs WHERE "
        nomedit = self.entsearchNomEdit.get()
        patron = self.entsearchPatron.get()
        pays = self.entsearchPays.get()

        if nomedit == patron == pays == "":
            self.lblconfSearch.grid(row=9)
            return

        if nomedit != "":
            req += "NomEdit = '" + nomedit + "' AND "
        if patron != "":
            req += "Patron = '" + patron + "' AND "
        if pays != "":
            req += "Pays = '" + pays + "' AND "
        
        if req[-5:] == " AND ":
            req = req[:-5]
        req += ";"
        self.lblconfSearch.grid_forget()  # On supprime le label d'erreur au cas ou il etait present
        
        res = doQuery(self.conn, req)  # Envoie de la requete et recuperation du resultat
        
        for line in self.table.get_children():  # Suppression des elements du tableau pour afficher le resultat de la requete
            self.table.delete(line)
        
        for i in range(len(res)):
            self.table.insert(parent='', index=i, values=res[i])
    
    def commandback(self):
        """Retourne a l'ecran d'accueil"""
        for widget in self.window.winfo_children():  # Suppression de tous les elements de la fenetre
            widget.destroy()
        accueil.Accueil(self.window)

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1400x720")
    e = Editeurs(window)
    tk.mainloop()