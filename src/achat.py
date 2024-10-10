import tkinter as tk
from query import *
window = None

class Achat:
    """Ecran de la table achat avec toutes les operation qui lui correspond"""
    def __init__(self):
        conn = initConn()
        table = doQuery(conn, "SELECT * FROM ACHAT")
        print(table)

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1280x720")
    a = Achat()
    tk.mainloop()