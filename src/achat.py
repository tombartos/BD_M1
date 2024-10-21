import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
from datetime import date
from query import *
import accueil

class Achat:
    """Ecran de la table achat avec toutes les operation qui lui correspond"""
    def __init__(self, window):
        self.window=window

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=10)

        #Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM ACHAT")
        
        #Bouton retour
        font1 = tkfont.Font(family = "Times New Roman", size=18)
        btnretour = tk.Button(self.window, text="Retour", font=font1, command=self.commandback)
        btnretour.grid(column=0, row=0, sticky="nw")

        #Label en haut de l'ecran nom de la table
        font0 = tkfont.Font(family="Times New Roman", size=30, weight="bold")
        lbl1 = tk.Label(self.window, text="Achats", font=font0)
        lbl1.grid(column=1, row=0)

        #Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Times New Roman', 17))
        style.configure("Treeview", font=('Calibri', 15))

        #Creation tableau
        self.table=ttk.Treeview(self.window, height=22)
        self.table.grid(column=0, row=1, columnspan=3)
        self.table['columns'] = ['NoAchat', 'ISBN', 'IDClient', 'DateAchat', 'QteAchat', 'PrixTotAchat']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('NoAchat', width=120)
        self.table.column('ISBN', width=200)
        self.table.column('IDClient', width=120)
        self.table.column('DateAchat', width=140)
        self.table.column('QteAchat', width=140)
        self.table.column('PrixTotAchat', width=160)

        for e in self.table['columns']:
            self.table.heading(e, text=e)

        self.table.heading('NoAchat', text='Noachat')
        self.table.heading('ISBN', text='ISBN')
        self.table.heading('IDClient', text='IDClient')
        self.table.heading('DateAchat', text='DateAchat')
        self.table.heading('QteAchat', text='QteAchat')
        self.table.heading('PrixTotAchat', text='PrixTotAchat')

        #Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent = '', index = i, values=req[i])

        #bind de la table
        self.table.bind('<ButtonRelease-1>',self.commandSelection)
        
        #Variable pour récuper un NoAchat
        self.na = None

        #Boutons nouvelle entree, supprimer et recherche
        

        self.ButNew = tk.Button(self.window, text='Nouvel Achat', font=font1, command=self.commandBuy)
        self.ButNew.grid(row=2, column=0, sticky='e')
        
        self.ButDel = tk.Button(self.window, text='Supprimer Achat', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.grid(row=2, column =1)

        self.ButSearch = tk.Button(self.window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.grid(row=2, column = 2)

        #Label Nouvelle entree
        self.lblnew = tk.Label(self.window, text="Nouvel Achat", font=font0)

        #Frame pour les entrees des nouveaux attributs qu'on cache au debut
        self.newframe=tk.Frame(self.window)

        #Attributs pour nouvelle entree
        font2 = tkfont.Font(family="Calibri", size = 25)
        self.lblnewISBN = tk.Label(self.newframe, text="ISBN", font=font2)
        self.lblnewISBN.grid(row=0, sticky='nsew')
        self.entnewISBN = tk.Entry(self.newframe)
        self.entnewISBN.grid(row=1)

        self.lblnewIDClient = tk.Label(self.newframe, text="IDClient", font=font2)
        self.lblnewIDClient.grid(row=2, column=0)
        self.entnewIDClient = tk.Entry(self.newframe)
        self.entnewIDClient.grid(row=3)

        self.lblnewQteAchat = tk.Label(self.newframe, text="QteAchat", font=font2)
        self.lblnewQteAchat.grid(row=4)
        self.entnewQteAchat = tk.Entry(self.newframe)
        self.entnewQteAchat.grid(row=5)

        self.btnconfAchat = tk.Button(self.newframe, text='Confirmer', font=font1, command=self.commandConfBuy)
        self.btnconfAchat.grid(row=6)

        #Creation du label indiquant par la suite si l'operation a reussie ou non
        self.lblnewstate = tk.Label(self.newframe, text="")
        self.lblnewstate.grid(row=7)

        #Label Rechercher
        self.lblsearch = tk.Label(self.window, text="Rechercher", font=font0)

        #Frame pour les entrees de la recherche
        self.searchframe=tk.Frame(self.window)

        #Attributs Recherche
        # NoAchat Entry
        self.lblsearchNoAchat = tk.Label(self.searchframe, text="NoAchat", font=font2)
        self.lblsearchNoAchat.grid(row=0)
        self.entsearchNoAchat = tk.Entry(self.searchframe)
        self.entsearchNoAchat.grid(row=1)

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

        # DateAchat Entry
        self.lblsearchDateAchat = tk.Label(self.searchframe, text="DateAchat", font=font2)
        self.lblsearchDateAchat.grid(row=6)
        self.entsearchDateAchat = tk.Entry(self.searchframe)
        self.entsearchDateAchat.grid(row=7)

        # QteAchat Entry
        self.lblsearchQteAchat = tk.Label(self.searchframe, text="QteAchat", font=font2)
        self.lblsearchQteAchat.grid(row=8)
        self.entsearchQteAchat = tk.Entry(self.searchframe)
        self.entsearchQteAchat.grid(row=9)

        # PrixTotAchat Entry
        self.lblsearchPrixTotAchat = tk.Label(self.searchframe, text="PrixTotAchat", font=font2)
        self.lblsearchPrixTotAchat.grid(row=10)
        self.entsearchPrixTotAchat = tk.Entry(self.searchframe)
        self.entsearchPrixTotAchat.grid(row=11)

        #Bouton Confirmer Recherche
        self.btnconfSearch = tk.Button(self.searchframe, text="Rechercher", font=font1, command=self.commandConfSearch)
        self.btnconfSearch.grid(row=12)

        #Label Erreur recherche vide
        self.lblconfSearch = tk.Label(self.searchframe, text="Veuillez remplir au moins un champ", fg='red')
        
    def updatetable(self):
        """Met à jour l'affichage du tableau"""
        #Suppression des elements
        for line in self.table.get_children():
            self.table.delete(line)

        #Remplissage avec les nouveaux elements
        req = doQuery(self.conn, "SELECT * FROM ACHAT")
        for i in range(len(req)):
            self.table.insert(parent = '', index = i, values=req[i])

        

    def commandBuy(self):
        """Affiche l'interface pour ajouter une nouvelle entree a la table"""
        self.updatetable()  #On fait une update au cas ou on etait dans recherche pour reafficher toute la table
        self.ButSearch.configure(state="active")
        self.ButNew.configure(state="disabled")
        self.searchframe.grid_forget()
        self.newframe.grid(column=3, row = 1, sticky="nsew")
        self.lblsearch.grid_forget()
        self.lblnew.grid(column=3, row=0)
        #TODO: Trouver le moyen de les decaler un peu sur la droite, peut etre avec rowconfigure
    
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
        #Vérification qu'il y ait une ligne sélectionné
        if self.na != None:
            
            try:
                doNoReturnQuery(self.conn,f"DELETE FROM Achat WHERE NoAchat = '{self.na}';")
                self.lblnewstate.config(text = "Opération Réussie", fg="green")
                self.updatetable()
                self.ButDel.configure(state = "disabled")
            except:
                self.lblnewstate.config(text = "Opétation échouée, revoyez les entrées", fg="red")
                doNoReturnQuery(self.conn, "ROLLBACK;")      
    
    def commandSelection(self,event) :
        """récupère le NoAchat de la ligne sélectionner."""
        # récupération de la ligne
        value = self.table.item(self.table.selection())['values']
        
        #Vérification si la ligne est vide ou non
        if value :
        
            #Récupération de la valeur de NoAchat
            if value[0] != self.na:
                self.na = value[0]
                self.ButDel.configure(state = "normal")
                
            #Déselectionne si la ligne est resélectionné
            else :
                self.table.selection_toggle(self.table.selection())
                self.na = None
                self.ButDel.configure(state = "disabled")
        else :
            self.na = None
            self.ButDel.configure(state = "disabled")

    def commandConfBuy(self):
        """Confirme un achat (envoie la requete SQL a la BDD pour ajouter une entree a la table Achat)"""
        #Recuperation des valeurs de la nouvelle entree
        isbn = self.entnewISBN.get()
        idclient = self.entnewIDClient.get()
        qteachat = self.entnewQteAchat.get()
        dateachat = date.today().strftime("%d/%m/%Y")
        
        try:
            a = doNoReturnQuery(self.conn, f"INSERT INTO Achat (ISBN, IDClient, DateAchat, QteAchat) VALUES('{isbn}', {idclient}, '{dateachat}', {qteachat});")
            if a == None:
                self.lblnewstate.config(text = "Opération Réussie", fg="green")
            else:
                self.lblnewstate.config(text="Info : \n" + a, fg="orange")       #Mauvaise ecriture des triggers de la base, renvoient des notices au lieu de renvoyer des erreurs donc oblige de gerer comme ca
            self.updatetable()
        except:
            self.lblnewstate.config(text = "Opétation échouée, revoyez les entrées", fg="red")
            doNoReturnQuery(self.conn, "ROLLBACK;")
        
    def commandConfSearch(self):
        """Confirme une recherche(envoie la requete SQL et affiche la reponse dans le tableau)"""
        #Construction de la requete
        req = "SELECT * FROM Achat WHERE "
        noachat = self.entsearchNoAchat.get()
        isbn = self.entsearchISBN.get()
        idclient = self.entsearchIDClient.get()
        dateachat = self.entsearchDateAchat.get()
        qteachat = self.entsearchQteAchat.get()
        prixtotachat = self.entsearchPrixTotAchat.get()

        if noachat == isbn == idclient == dateachat == qteachat == prixtotachat == "":
            self.lblconfSearch.grid(row=13)
            return

        if noachat != "":
            req+= "Noachat = " + noachat + " AND "
        if isbn != "":
            req+= "ISBN = " + isbn + " AND "
        if idclient != "":
            req+= "IDClient = " + idclient + " AND "
        if dateachat != "":
            req+= "DateAchat = '" + dateachat + "' AND "
        if qteachat != "":
            req+= "QteAchat = " + qteachat + " AND "
        if prixtotachat != "":
            req+= "PrixTotAchat = " + prixtotachat
        
        if req[-5:] == " AND ":
            req = req[:-5]
        req+=";"
        self.lblconfSearch.grid_forget() #On supprime le label d'erreur au cas ou il etait present
        
        res = doQuery(self.conn, req)   #Envoie de la requete et recuperation du resulat
        
        for line in self.table.get_children():  #Suppression des elements du tableau pour afficher le resultat de la requete
            self.table.delete(line)
        
        for i in range(len(res)):
            self.table.insert(parent = '', index = i, values=res[i])
    
    def commandback(self):
        """Retourne a l'ecran d'accueil"""
        for widget in self.window.winfo_children(): #Suppresssion de tous les elements de la fenetre
            widget.destroy()
        accueil.Accueil(self.window)
        


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1400x720")
    a = Achat(window)
    tk.mainloop()
