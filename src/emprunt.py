import tkinter as tk
from datetime import date
from query import *
import accueil

import tkinter.font as tkfont
import tkinter.ttk as ttk

class Emprunt:
    """Ecran de la table emprunt avec toutes les operations qui lui correspondent"""
    def __init__(self, window):
        self.window = window

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=10)

        # Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM EMPRUNT")
        
        # Bouton retour
        font1 = tkfont.Font(family="Times New Roman", size=18)
        btnretour = tk.Button(self.window, text="Retour", font=font1, command=self.commandback)
        btnretour.grid(column=0, row=0, sticky="nw")

        # Label en haut de l'ecran nom de la table
        font0 = tkfont.Font(family="Times New Roman", size=30, weight="bold")
        lbl1 = tk.Label(self.window, text="Emprunts", font=font0)
        lbl1.grid(column=1, row=0)

        # Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Times New Roman', 17))
        style.configure("Treeview", font=('Calibri', 15))

        # Creation tableau
        self.table = ttk.Treeview(self.window, height=22)
        self.table.grid(column=0, row=1, columnspan=3)
        self.table['columns'] = ['NoEmp', 'ISBN', 'IDClient', 'DateDeb', 'DateFin', 'QteEmp', 'StatutEmp', 'StatutLivre']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('NoEmp', width=120)
        self.table.column('ISBN', width=200)
        self.table.column('IDClient', width=120)
        self.table.column('DateDeb', width=140)
        self.table.column('DateFin', width=140)
        self.table.column('QteEmp', width=140)
        self.table.column('StatutEmp', width=160)
        self.table.column('StatutLivre', width=160)

        for e in self.table['columns']:
            self.table.heading(e, text=e)

        # Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

        # bind de la table
        self.table.bind('<ButtonRelease-1>', self.commandSelection)
        
        # Variable pour recuperer un NoEmp
        self.ne = None

        # Boutons nouvelle entree, supprimer et recherche
        self.ButNew = tk.Button(self.window, text='Nouvel Emprunt', font=font1, command=self.commandBorrow)
        self.ButNew.grid(row=2, column=0, sticky='e')
        
        self.ButDel = tk.Button(self.window, text='Supprimer Emprunt', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.grid(row=2, column=1)

        self.ButSearch = tk.Button(self.window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.grid(row=2, column=2)

        # Label Nouvelle entree
        self.lblnew = tk.Label(self.window, text="Nouvel Emprunt", font=font0)

        # Frame pour les entrees des nouveaux attributs qu'on cache au debut
        self.newframe = tk.Frame(self.window)

        # Attributs pour nouvelle entree
        font2 = tkfont.Font(family="Calibri", size=25)
        self.lblnewISBN = tk.Label(self.newframe, text="ISBN", font=font2)
        self.lblnewISBN.grid(row=0, sticky='nsew')
        self.entnewISBN = tk.Entry(self.newframe)
        self.entnewISBN.grid(row=1)

        self.lblnewIDClient = tk.Label(self.newframe, text="IDClient", font=font2)
        self.lblnewIDClient.grid(row=2, column=0)
        self.entnewIDClient = tk.Entry(self.newframe)
        self.entnewIDClient.grid(row=3)

        self.lblnewQteEmp = tk.Label(self.newframe, text="QteEmp", font=font2)
        self.lblnewQteEmp.grid(row=4)
        self.entnewQteEmp = tk.Entry(self.newframe)
        self.entnewQteEmp.grid(row=5)

        self.lblnewDateFin = tk.Label(self.newframe, text="DateFin", font=font2)
        self.lblnewDateFin.grid(row=6)
        self.entnewDateFin = tk.Entry(self.newframe)
        self.entnewDateFin.grid(row=7)


        self.lblnewStatutLivre = tk.Label(self.newframe, text="StatutLivre", font=font2)
        self.lblnewStatutLivre.grid(row=8)
        self.entnewStatutLivre = tk.Entry(self.newframe)
        self.entnewStatutLivre.grid(row=9)

        self.btnconfEmp = tk.Button(self.newframe, text='Confirmer', font=font1, command=self.commandConfBorrow)
        self.btnconfEmp.grid(row=10)

        # Creation du label indiquant par la suite si l'operation a reussie ou non
        self.lblnewstate = tk.Label(self.newframe, text="")
        self.lblnewstate.grid(row=11)

        # Label Rechercher
        self.lblsearch = tk.Label(self.window, text="Rechercher", font=font0)

        # Frame pour les entrees de la recherche
        self.searchframe = tk.Frame(self.window)

        # Attributs Recherche
        # NoEmp Entry
        self.lblsearchNoEmp = tk.Label(self.searchframe, text="NoEmp", font=font2)
        self.lblsearchNoEmp.grid(row=0)
        self.entsearchNoEmp = tk.Entry(self.searchframe)
        self.entsearchNoEmp.grid(row=1)

        # ISBN Entry
        self.lblsearchISBN = tk.Label(self.searchframe, text="ISBN", font=font2)
        self.lblsearchISBN.grid(row=2)
        self.entsearchISBN = tk.Entry(self.searchframe)
        self.entsearchISBN.grid(row=3)

        # IDClient Entry
        self.lblsearchIDClient = tk.Label(self.searchframe, text="IDClient", font=font2)
        self.lblsearchIDClient.grid(row=4)
        self.entsearchIDClient = tk.Entry(self.searchframe)
        self.entsearchIDClient.grid(row=5)

        # DateDeb Entry
        self.lblsearchDateDeb = tk.Label(self.searchframe, text="DateDeb", font=font2)
        self.lblsearchDateDeb.grid(row=6)
        self.entsearchDateDeb = tk.Entry(self.searchframe)
        self.entsearchDateDeb.grid(row=7)

        # DateFin Entry
        self.lblsearchDateFin = tk.Label(self.searchframe, text="DateFin", font=font2)
        self.lblsearchDateFin.grid(row=8)
        self.entsearchDateFin = tk.Entry(self.searchframe)
        self.entsearchDateFin.grid(row=9)

        # QteEmp Entry
        self.lblsearchQteEmp = tk.Label(self.searchframe, text="QteEmp", font=font2)
        self.lblsearchQteEmp.grid(row=10)
        self.entsearchQteEmp = tk.Entry(self.searchframe)
        self.entsearchQteEmp.grid(row=11)

        # StatutEmp Entry
        self.lblsearchStatutEmp = tk.Label(self.searchframe, text="StatutEmp", font=font2)
        self.lblsearchStatutEmp.grid(row=12)
        self.entsearchStatutEmp = tk.Entry(self.searchframe)
        self.entsearchStatutEmp.grid(row=13)

        # StatutLivre Entry
        self.lblsearchStatutLivre = tk.Label(self.searchframe, text="StatutLivre", font=font2)
        self.lblsearchStatutLivre.grid(row=14)
        self.entsearchStatutLivre = tk.Entry(self.searchframe)
        self.entsearchStatutLivre.grid(row=15)

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
        req = doQuery(self.conn, "SELECT * FROM EMPRUNT")
        for i in range(len(req)):
            self.table.insert(parent='', index=i, values=req[i])

    def commandBorrow(self):
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
        # Verification qu'il y ait une ligne selectionnee
        if self.ne is not None:
            try:
                doNoReturnQuery(self.conn, f"DELETE FROM Emprunt WHERE NoEmp = '{self.ne}';")
                self.lblnewstate.config(text="Opération Réussie", fg="green")
                self.updatetable()
                self.ButDel.configure(state="disabled")
            except:
                self.lblnewstate.config(text="Opétation échouée, revoyez les entrées", fg="red")
                doNoReturnQuery(self.conn, "ROLLBACK;")
    
    def commandSelection(self, event):
        """Recupere le NoEmp de la ligne selectionnee."""
        # Recuperation de la ligne
        value = self.table.item(self.table.selection())['values']
        
        # Verification si la ligne est vide ou non
        if value:
            # Recuperation de la valeur de NoEmp
            if value[0] != self.ne:
                self.ne = value[0]
                self.ButDel.configure(state="normal")
            # Deselectionne si la ligne est reselectionnee
            else:
                self.table.selection_toggle(self.table.selection())
                self.ne = None
                self.ButDel.configure(state="disabled")
        else:
            self.ne = None
            self.ButDel.configure(state="disabled")

    def commandConfBorrow(self):
        """Confirme un emprunt (envoie la requete SQL a la BDD pour ajouter une entree a la table Emprunt)"""
        # Recuperation des valeurs de la nouvelle entree
        isbn = self.entnewISBN.get()
        idclient = self.entnewIDClient.get()
        qteemp = self.entnewQteEmp.get()
        datedeb = date.today().strftime("%d/%m/%Y")
        datefin = self.entnewDateFin.get()
        statutlivre = self.entnewStatutLivre.get()
        
        try:
            a =doNoReturnQuery(self.conn, f"INSERT INTO Emprunt (ISBN, IDClient, DateDeb, DateFin, QteEmp, StatutEmp, StatutLivre) VALUES('{isbn}', {idclient}, '{datedeb}', '{datefin}', {qteemp}, 'non rendu', '{statutlivre}');")
            if a == None:
                self.lblnewstate.config(text="Opération Réussie", fg="green")
            else:
                self.lblnewstate.config(text="Info :\n" + a, fg="orange")            #Mauvaise ecriture des triggers de la base, renvoient des notices au lieu de renvoyer des erreurs donc oblige de gerer comme ca
            self.updatetable()
        except Exception as e:
            print(e)
            self.lblnewstate.config(text="Opétation échouée, revoyez les entrées \n" + str(e), fg="red")
            doNoReturnQuery(self.conn, "ROLLBACK;")
        
    def commandConfSearch(self):
        """Confirme une recherche (envoie la requete SQL et affiche la reponse dans le tableau)"""
        # Construction de la requete
        req = "SELECT * FROM Emprunt WHERE "
        noemp = self.entsearchNoEmp.get()
        isbn = self.entsearchISBN.get()
        idclient = self.entsearchIDClient.get()
        datedeb = self.entsearchDateDeb.get()
        datefin = self.entsearchDateFin.get()
        qteemp = self.entsearchQteEmp.get()
        statutemp = self.entsearchStatutEmp.get()
        statutlivre = self.entsearchStatutLivre.get()

        if noemp == isbn == idclient == datedeb == datefin == qteemp == statutemp == statutlivre == "":
            self.lblconfSearch.grid(row=17)
            return

        if noemp != "":
            req += "NoEmp = " + noemp + " AND "
        if isbn != "":
            req += "ISBN = " + isbn + " AND "
        if idclient != "":
            req += "IDClient = " + idclient + " AND "
        if datedeb != "":
            req += "DateDeb = '" + datedeb + "' AND "
        if datefin != "":
            req += "DateFin = '" + datefin + "' AND "
        if qteemp != "":
            req += "QteEmp = " + qteemp + " AND "
        if statutemp != "":
            req += "StatutEmp = '" + statutemp + "' AND "
        if statutlivre != "":
            req += "StatutLivre = '" + statutlivre + "'"
        
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
    e = Emprunt(window)
    tk.mainloop()
