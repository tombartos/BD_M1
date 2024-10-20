import tkinter as tk
from datetime import date
from query import *
import accueil

import tkinter.font as tkfont
import tkinter.ttk as ttk

class Auteurs:
    """Ecran de la table auteurs avec toutes les operations qui lui correspondent"""
    def __init__(self, window):
        self.window = window

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=10)

        # Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM AUTEURS")
        
        # Bouton retour
        font1 = tkfont.Font(family="Times New Roman", size=18)
        btnretour = tk.Button(self.window, text="Retour", font=font1, command=self.commandback)
        btnretour.grid(column=0, row=0, sticky="nw")

        # Label en haut de l'ecran nom de la table
        font0 = tkfont.Font(family="Times New Roman", size=30, weight="bold")
        lbl1 = tk.Label(self.window, text="Auteurs", font=font0)
        lbl1.grid(column=1, row=0)

        # Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Times New Roman', 17))
        style.configure("Treeview", font=('Calibri', 15))

        # Creation tableau
        self.table = ttk.Treeview(self.window, height=22)
        self.table.grid(column=0, row=1, columnspan=3)
        self.table['columns'] = ['IDAuteur', 'NomAut', 'PrenomAut', 'NaissanceAut', 'Mort', 'Nationalite']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('IDAuteur', width=120)
        self.table.column('NomAut', width=200)
        self.table.column('PrenomAut', width=200)
        self.table.column('NaissanceAut', width=140)
        self.table.column('Mort', width=140)
        self.table.column('Nationalite', width=160)

        for e in self.table['columns']:
            self.table.heading(e, text=e)

        # Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

        # bind de la table
        self.table.bind('<ButtonRelease-1>', self.commandSelection)
        
        # Variable pour recuperer un IDAuteur
        self.na = None

        # Boutons nouvelle entree, supprimer et recherche
        self.ButNew = tk.Button(self.window, text='Nouvel Auteur', font=font1, command=self.commandNew)
        self.ButNew.grid(row=2, column=0, sticky='e')
        
        self.ButDel = tk.Button(self.window, text='Supprimer Auteur', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.grid(row=2, column=1)

        self.ButSearch = tk.Button(self.window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.grid(row=2, column=2)

        # Label Nouvelle entree
        self.lblnew = tk.Label(self.window, text="Nouvel Auteur", font=font0)

        # Frame pour les entrees des nouveaux attributs qu'on cache au debut
        self.newframe = tk.Frame(self.window)

        # Attributs pour nouvelle entree
        font2 = tkfont.Font(family="Calibri", size=25)
        self.lblnewNomAut = tk.Label(self.newframe, text="NomAut", font=font2)
        self.lblnewNomAut.grid(row=0, sticky='nsew')
        self.entnewNomAut = tk.Entry(self.newframe)
        self.entnewNomAut.grid(row=1)

        self.lblnewPrenomAut = tk.Label(self.newframe, text="PrenomAut", font=font2)
        self.lblnewPrenomAut.grid(row=2, column=0)
        self.entnewPrenomAut = tk.Entry(self.newframe)
        self.entnewPrenomAut.grid(row=3)

        self.lblnewNaissanceAut = tk.Label(self.newframe, text="NaissanceAut", font=font2)
        self.lblnewNaissanceAut.grid(row=4)
        self.entnewNaissanceAut = tk.Entry(self.newframe)
        self.entnewNaissanceAut.grid(row=5)

        self.lblnewMort = tk.Label(self.newframe, text="Mort", font=font2)
        self.lblnewMort.grid(row=6)
        self.entnewMort = tk.Entry(self.newframe)
        self.entnewMort.grid(row=7)

        self.lblnewNationalite = tk.Label(self.newframe, text="Nationalite", font=font2)
        self.lblnewNationalite.grid(row=8)
        self.entnewNationalite = tk.Entry(self.newframe)
        self.entnewNationalite.grid(row=9)

        self.btnconfAuteur = tk.Button(self.newframe, text='Confirmer', font=font1, command=self.commandConfNew)
        self.btnconfAuteur.grid(row=10)

        # Creation du label indiquant par la suite si l'operation a reussie ou non
        self.lblnewstate = tk.Label(self.newframe, text="")
        self.lblnewstate.grid(row=11)

        # Label Rechercher
        self.lblsearch = tk.Label(self.window, text="Rechercher", font=font0)

        # Frame pour les entrees de la recherche
        self.searchframe = tk.Frame(self.window)

        # Attributs Recherche
        # IDAuteur Entry
        self.lblsearchIDAuteur = tk.Label(self.searchframe, text="IDAuteur", font=font2)
        self.lblsearchIDAuteur.grid(row=0)
        self.entsearchIDAuteur = tk.Entry(self.searchframe)
        self.entsearchIDAuteur.grid(row=1)

        # NomAut Entry
        self.lblsearchNomAut = tk.Label(self.searchframe, text="NomAut", font=font2)
        self.lblsearchNomAut.grid(row=2)
        self.entsearchNomAut = tk.Entry(self.searchframe)
        self.entsearchNomAut.grid(row=3)

        # PrenomAut Entry
        self.lblsearchPrenomAut = tk.Label(self.searchframe, text="PrenomAut", font=font2)
        self.lblsearchPrenomAut.grid(row=4)
        self.entsearchPrenomAut = tk.Entry(self.searchframe)
        self.entsearchPrenomAut.grid(row=5)

        # NaissanceAut Entry
        self.lblsearchNaissanceAut = tk.Label(self.searchframe, text="NaissanceAut", font=font2)
        self.lblsearchNaissanceAut.grid(row=6)
        self.entsearchNaissanceAut = tk.Entry(self.searchframe)
        self.entsearchNaissanceAut.grid(row=7)

        # Mort Entry
        self.lblsearchMort = tk.Label(self.searchframe, text="Mort", font=font2)
        self.lblsearchMort.grid(row=8)
        self.entsearchMort = tk.Entry(self.searchframe)
        self.entsearchMort.grid(row=9)

        # Nationalite Entry
        self.lblsearchNationalite = tk.Label(self.searchframe, text="Nationalite", font=font2)
        self.lblsearchNationalite.grid(row=10)
        self.entsearchNationalite = tk.Entry(self.searchframe)
        self.entsearchNationalite.grid(row=11)

        # Bouton Confirmer Recherche
        self.btnconfSearch = tk.Button(self.searchframe, text="Rechercher", font=font1, command=self.commandConfSearch)
        self.btnconfSearch.grid(row=12)

        # Label Erreur recherche vide
        self.lblconfSearch = tk.Label(self.searchframe, text="Veuillez remplir au moins un champ", fg='red')
        
    def updatetable(self):
        """Met à jour l'affichage du tableau"""
        # Suppression des elements
        for line in self.table.get_children():
            self.table.delete(line)

        # Remplissage avec les nouveaux elements
        req = doQuery(self.conn, "SELECT * FROM AUTEURS")
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
        if self.na is not None:
            try:
                doNoReturnQuery(self.conn, f"DELETE FROM Auteurs WHERE IDAuteur = '{self.na}';")
                self.lblnewstate.config(text="Opération Réussie", fg="green")
                self.updatetable()
                self.ButDel.configure(state="disabled")
            except:
                self.lblnewstate.config(text="Opétation échouée, revoyez les entrées", fg="red")
                doNoReturnQuery(self.conn, "ROLLBACK;")      
    
    def commandSelection(self, event):
        """Récupère le IDAuteur de la ligne sélectionnée."""
        # récupération de la ligne
        value = self.table.item(self.table.selection())['values']
        
        # Vérification si la ligne est vide ou non
        if value:
            # Récupération de la valeur de IDAuteur
            if value[0] != self.na:
                self.na = value[0]
                self.ButDel.configure(state="normal")
            # Déselectionne si la ligne est resélectionnée
            else:
                self.table.selection_toggle(self.table.selection())
                self.na = None
                self.ButDel.configure(state="disabled")
        else:
            self.na = None
            self.ButDel.configure(state="disabled")

    def commandConfNew(self):
        """Confirme un nouvel auteur (envoie la requete SQL a la BDD pour ajouter une entree a la table Auteurs)"""
        # Recuperation des valeurs de la nouvelle entree
        nomaut = self.entnewNomAut.get()
        prenomaut = self.entnewPrenomAut.get()
        naisanceaut = self.entnewNaissanceAut.get()
        mort = self.entnewMort.get()
        nationalite = self.entnewNationalite.get()
        
        try:
            if mort == "":
                doNoReturnQuery(self.conn, f"INSERT INTO Auteurs (NomAut, PrenomAut, NaissanceAut, Nationalite) VALUES('{nomaut}', '{prenomaut}', '{naisanceaut}', '{nationalite}');")
            else:
                doNoReturnQuery(self.conn, f"INSERT INTO Auteurs (NomAut, PrenomAut, NaissanceAut, Mort, Nationalite) VALUES('{nomaut}', '{prenomaut}', '{naisanceaut}', '{mort}', '{nationalite}');")
            self.lblnewstate.config(text="Opération Réussie", fg="green")
            self.updatetable()
        except Exception as e:
            print(e)
            self.lblnewstate.config(text="Opétation échouée, revoyez les entrées", fg="red")
            doNoReturnQuery(self.conn, "ROLLBACK;")
        
    def commandConfSearch(self):
        """Confirme une recherche (envoie la requete SQL et affiche la reponse dans le tableau)"""
        # Construction de la requete
        req = "SELECT * FROM Auteurs WHERE "
        idAuteur = self.entsearchIDAuteur.get()
        nomaut = self.entsearchNomAut.get()
        prenomaut = self.entsearchPrenomAut.get()
        naisanceaut = self.entsearchNaissanceAut.get()
        mort = self.entsearchMort.get()
        nationalite = self.entsearchNationalite.get()

        if idAuteur == nomaut == prenomaut == naisanceaut == mort == nationalite == "":
            self.lblconfSearch.grid(row=13)
            return

        if idAuteur != "":
            req += "IDAuteur = " + idAuteur + " AND "
        if nomaut != "":
            req += "NomAut = '" + nomaut + "' AND "
        if prenomaut != "":
            req += "PrenomAut = '" + prenomaut + "' AND "
        if naisanceaut != "":
            req += "NaissanceAut = '" + naisanceaut + "' AND "
        if mort != "":
            req += "Mort = '" + mort + "' AND "
        if nationalite != "":
            req += "Nationalite = '" + nationalite + "'"
        
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
    a = Auteurs(window)
    tk.mainloop()