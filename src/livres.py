import tkinter as tk
from datetime import date
from query import *
import accueil

import tkinter.font as tkfont
import tkinter.ttk as ttk

class Livres:
    """Ecran de la table livres avec toutes les operations qui lui correspondent"""
    def __init__(self, window):
        self.window = window

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=10)

        # Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM LIVRES")
        
        # Bouton retour
        font1 = tkfont.Font(family="Times New Roman", size=18)
        btnretour = tk.Button(self.window, text="Retour", font=font1, command=self.commandback)
        btnretour.grid(column=0, row=0, sticky="nw")

        # Label en haut de l'ecran nom de la table
        font0 = tkfont.Font(family="Times New Roman", size=30, weight="bold")
        lbl1 = tk.Label(self.window, text="Livres", font=font0)
        lbl1.grid(column=1, row=0)

        # Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Times New Roman', 17))
        style.configure("Treeview", font=('Calibri', 15))

        # Creation tableau
        self.table = ttk.Treeview(self.window, height=22)
        self.table.grid(column=0, row=1, columnspan=3)
        self.table['columns'] = ['ISBN', 'Titre', 'IDAuteur', 'NomEdit', 'DateSortie', 'Genre', 'QteDispo', 'PrixAchat']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('ISBN', width=200)
        self.table.column('Titre', width=200)
        self.table.column('IDAuteur', width=120)
        self.table.column('NomEdit', width=140)
        self.table.column('DateSortie', width=140)
        self.table.column('Genre', width=140)
        self.table.column('QteDispo', width=140)
        self.table.column('PrixAchat', width=160)

        for e in self.table['columns']:
            self.table.heading(e, text=e)

        # Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

        # bind de la table
        self.table.bind('<ButtonRelease-1>', self.commandSelection)
        
        # Variable pour récuper un ISBN
        self.isbn = None

        # Boutons nouvelle entree, supprimer et recherche
        self.ButNew = tk.Button(self.window, text='Nouveau Livre', font=font1, command=self.commandAdd)
        self.ButNew.grid(row=2, column=0, sticky='e')
        
        self.ButDel = tk.Button(self.window, text='Supprimer Livre', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.grid(row=2, column=1)

        self.ButSearch = tk.Button(self.window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.grid(row=2, column=2)

        # Label Nouvelle entree
        self.lblnew = tk.Label(self.window, text="Nouveau Livre", font=font0)

        # Frame pour les entrees des nouveaux attributs qu'on cache au debut
        self.newframe = tk.Frame(self.window)

        # Attributs pour nouvelle entree
        font2 = tkfont.Font(family="Calibri", size=25)
        self.lblnewISBN = tk.Label(self.newframe, text="ISBN", font=font2)
        self.lblnewISBN.grid(row=0, sticky='nsew')
        self.entnewISBN = tk.Entry(self.newframe)
        self.entnewISBN.grid(row=1)

        self.lblnewTitre = tk.Label(self.newframe, text="Titre", font=font2)
        self.lblnewTitre.grid(row=2, column=0)
        self.entnewTitre = tk.Entry(self.newframe)
        self.entnewTitre.grid(row=3)

        self.lblnewIDAuteur = tk.Label(self.newframe, text="IDAuteur", font=font2)
        self.lblnewIDAuteur.grid(row=4)
        self.entnewIDAuteur = tk.Entry(self.newframe)
        self.entnewIDAuteur.grid(row=5)

        self.lblnewNomEdit = tk.Label(self.newframe, text="NomEdit", font=font2)
        self.lblnewNomEdit.grid(row=6)
        self.entnewNomEdit = tk.Entry(self.newframe)
        self.entnewNomEdit.grid(row=7)

        self.lblnewDateSortie = tk.Label(self.newframe, text="DateSortie", font=font2)
        self.lblnewDateSortie.grid(row=8)
        self.entnewDateSortie = tk.Entry(self.newframe)
        self.entnewDateSortie.grid(row=9)

        self.lblnewGenre = tk.Label(self.newframe, text="Genre", font=font2)
        self.lblnewGenre.grid(row=10)
        self.entnewGenre = tk.Entry(self.newframe)
        self.entnewGenre.grid(row=11)

        self.lblnewQteDispo = tk.Label(self.newframe, text="QteDispo", font=font2)
        self.lblnewQteDispo.grid(row=12)
        self.entnewQteDispo = tk.Entry(self.newframe)
        self.entnewQteDispo.grid(row=13)

        self.lblnewPrixAchat = tk.Label(self.newframe, text="PrixAchat", font=font2)
        self.lblnewPrixAchat.grid(row=14)
        self.entnewPrixAchat = tk.Entry(self.newframe)
        self.entnewPrixAchat.grid(row=15)

        self.btnconfLivre = tk.Button(self.newframe, text='Confirmer', font=font1, command=self.commandConfAdd)
        self.btnconfLivre.grid(row=16)

        # Creation du label indiquant par la suite si l'operation a reussie ou non
        self.lblnewstate = tk.Label(self.newframe, text="")
        self.lblnewstate.grid(row=17)

        # Label Rechercher
        self.lblsearch = tk.Label(self.window, text="Rechercher", font=font0)

        # Frame pour les entrees de la recherche
        self.searchframe = tk.Frame(self.window)

        # Attributs Recherche
        # ISBN Entry
        self.lblsearchISBN = tk.Label(self.searchframe, text="ISBN", font=font2)
        self.lblsearchISBN.grid(row=0)
        self.entsearchISBN = tk.Entry(self.searchframe)
        self.entsearchISBN.grid(row=1)

        # Titre Entry
        self.lblsearchTitre = tk.Label(self.searchframe, text="Titre", font=font2)
        self.lblsearchTitre.grid(row=2)
        self.entsearchTitre = tk.Entry(self.searchframe)
        self.entsearchTitre.grid(row=3)

        # IDAuteur Entry
        self.lblsearchIDAuteur = tk.Label(self.searchframe, text="IDAuteur", font=font2)
        self.lblsearchIDAuteur.grid(row=4)
        self.entsearchIDAuteur = tk.Entry(self.searchframe)
        self.entsearchIDAuteur.grid(row=5)

        # NomEdit Entry
        self.lblsearchNomEdit = tk.Label(self.searchframe, text="NomEdit", font=font2)
        self.lblsearchNomEdit.grid(row=6)
        self.entsearchNomEdit = tk.Entry(self.searchframe)
        self.entsearchNomEdit.grid(row=7)

        # DateSortie Entry
        self.lblsearchDateSortie = tk.Label(self.searchframe, text="DateSortie", font=font2)
        self.lblsearchDateSortie.grid(row=8)
        self.entsearchDateSortie = tk.Entry(self.searchframe)
        self.entsearchDateSortie.grid(row=9)

        # Genre Entry
        self.lblsearchGenre = tk.Label(self.searchframe, text="Genre", font=font2)
        self.lblsearchGenre.grid(row=10)
        self.entsearchGenre = tk.Entry(self.searchframe)
        self.entsearchGenre.grid(row=11)

        # QteDispo Entry
        self.lblsearchQteDispo = tk.Label(self.searchframe, text="QteDispo", font=font2)
        self.lblsearchQteDispo.grid(row=12)
        self.entsearchQteDispo = tk.Entry(self.searchframe)
        self.entsearchQteDispo.grid(row=13)

        # PrixAchat Entry
        self.lblsearchPrixAchat = tk.Label(self.searchframe, text="PrixAchat", font=font2)
        self.lblsearchPrixAchat.grid(row=14)
        self.entsearchPrixAchat = tk.Entry(self.searchframe)
        self.entsearchPrixAchat.grid(row=15)

        # Bouton Confirmer Recherche
        self.btnconfSearch = tk.Button(self.searchframe, text="Rechercher", font=font1, command=self.commandConfSearch)
        self.btnconfSearch.grid(row=16)

        # Label Erreur recherche vide
        self.lblconfSearch = tk.Label(self.searchframe, text="Veuillez remplir au moins un champ", fg='red')
        
    def updatetable(self):
        """Met à jour l'affichage du tableau"""
        # Suppression des elements
        for line in self.table.get_children():
            self.table.delete(line)

        # Remplissage avec les nouveaux elements
        req = doQuery(self.conn, "SELECT * FROM LIVRES")
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

    def commandAdd(self):
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
        if self.isbn is not None:
            try:
                doNoReturnQuery(self.conn, f"DELETE FROM LIVRES WHERE ISBN = '{self.isbn}';")
                self.lblnewstate.config(text="Opération Réussie", fg="green")
                self.updatetable()
                self.ButDel.configure(state="disabled")
            except:
                self.lblnewstate.config(text="Opération échouée, revoyez les entrées", fg="red")
                doNoReturnQuery(self.conn, "ROLLBACK;")
    
    def commandSelection(self, event):
        """Récupère l'ISBN de la ligne sélectionnée."""
        # Récupération de la ligne
        value = self.table.item(self.table.selection())['values']
        
        # Vérification si la ligne est vide ou non
        if value:
            # Récupération de la valeur de ISBN
            if value[0] != self.isbn:
                self.isbn = value[0]
                self.ButDel.configure(state="normal")
            # Déselectionne si la ligne est resélectionnée
            else:
                self.table.selection_toggle(self.table.selection())
                self.isbn = None
                self.ButDel.configure(state="disabled")
        else:
            self.isbn = None
            self.ButDel.configure(state="disabled")

    def commandConfAdd(self):
        """Confirme un ajout de livre (envoie la requete SQL a la BDD pour ajouter une entree a la table Livres)"""
        # Recuperation des valeurs de la nouvelle entree
        isbn = self.entnewISBN.get()
        titre = self.entnewTitre.get()
        idauteur = self.entnewIDAuteur.get()
        nomedit = self.entnewNomEdit.get()
        datesortie = self.entnewDateSortie.get()
        genre = self.entnewGenre.get()
        qtedispo = self.entnewQteDispo.get()
        prixachat = self.entnewPrixAchat.get()
        
        try:
            doNoReturnQuery(self.conn, f"INSERT INTO LIVRES (ISBN, Titre, IDAuteur, NomEdit, DateSortie, Genre, QteDispo, PrixAchat) VALUES('{isbn}', '{titre}', {idauteur}, '{nomedit}', '{datesortie}', '{genre}', {qtedispo}, {prixachat});")
            self.lblnewstate.config(text="Opération Réussie", fg="green")
            self.updatetable()
        except:
            self.lblnewstate.config(text="Opération échouée, revoyez les entrées", fg="red")
            doNoReturnQuery(self.conn, "ROLLBACK;")
        
    def commandConfSearch(self):
        """Confirme une recherche (envoie la requete SQL et affiche la reponse dans le tableau)"""
        # Construction de la requete
        req = "SELECT * FROM LIVRES WHERE "
        isbn = self.entsearchISBN.get()
        titre = self.entsearchTitre.get()
        idauteur = self.entsearchIDAuteur.get()
        nomedit = self.entsearchNomEdit.get()
        datesortie = self.entsearchDateSortie.get()
        genre = self.entsearchGenre.get()
        qtedispo = self.entsearchQteDispo.get()
        prixachat = self.entsearchPrixAchat.get()

        if isbn == titre == idauteur == nomedit == datesortie == genre == qtedispo == prixachat == "":
            self.lblconfSearch.grid(row=17)
            return

        if isbn != "":
            req += "ISBN = '" + isbn + "' AND "
        if titre != "":
            req += "Titre = '" + titre + "' AND "
        if idauteur != "":
            req += "IDAuteur = " + idauteur + " AND "
        if nomedit != "":
            req += "NomEdit = '" + nomedit + "' AND "
        if datesortie != "":
            req += "DateSortie = '" + datesortie + "' AND "
        if genre != "":
            req += "Genre = '" + genre + "' AND "
        if qtedispo != "":
            req += "QteDispo = " + qtedispo + " AND "
        if prixachat != "":
            req += "PrixAchat = " + prixachat
        
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
    l = Livres(window)
    tk.mainloop()