# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:31:34 2016

@author: 3525162
"""
from Tkinter import *
import os
from grid import *

def welcome():
    
    window = Tk()
    canvas = Canvas( window, width = 900, height = 600, bg = "#993333")
    

    window.configure(background="#FFFFCC")
    welcomeLabel = Label(window, text = "          Solveur du jeu Rush Hour         ", fg = "#99CC99", bg = "#FFFFCC",font = "Helvetica 36 bold")
    welcomeLabel.place( x = 100, y = 450, width = 200, height = 200)
    welcomeLabel.pack()
    welcomeLabel2 = Label(window, text = "       Veuillez choisir un niveau       ",fg = "#99CC99",bg = "#FFFFCC", font = "Helvetica 12 bold")
    welcomeLabel2.place( x = 200, y = 120, width = 200, height = 200)
    welcomeLabel2.pack()
    welcomeLabel3 = Label(canvas, text = "          ", fg = "#993333", bg = "#FFFFCC",font = "Helvetica 40 bold")
    welcomeLabel3.pack()
  
    var = StringVar()
   #b1 = Radiobutton( window, text = "Débutant      ",indicatoron =0,  padx = 100,pady = 10, borderwidth = 5, bg ="#009966",  variable = v, value = "débutant")
    Radiobutton( window, text = "Débutant      ",  padx = 100,pady = 10, borderwidth = 5, bg ="#009966", value = "../puzzles/débutant/",  variable = var).pack()
    Radiobutton( window, text = "Intermédiaire",  padx = 100,pady = 10, borderwidth = 5, bg ="#009966", value = "../puzzles/intermédiaire/", variable = var).pack()
    Radiobutton( window, text = "Avancé         ",  padx = 100,pady = 10, borderwidth = 5, bg ="#009966", value = "../puzzles/avancé/", variable = var).pack()
    Radiobutton( window, text = "Expert          ", padx = 100,pady = 10, borderwidth = 5, bg ="#009966", value = "../puzzles/expert/", variable = var).pack()
    Radiobutton( window, text = "Test             ",  padx = 100,pady = 10, borderwidth = 5, bg ="#009966", value = "../puzzles/test/", variable = var).pack()

    def openDir():
        l = (os.listdir(var.get()))
        l.sort()
        window.destroy()
        window1 = Tk()
        window1.configure(background="#FFFFCC")
        welcomeLabel1 = Label(window1, text = "          Veuillez choisir une carte         ", fg = "#99CC99", bg = "#FFFFCC",font = "Helvetica 36 bold")
        welcomeLabel1.place( x = 100, y = 450, width = 200, height = 200)
        welcomeLabel1.pack()
        var1 = StringVar()
        
        for i in range(len(l)) :
            Radiobutton( window1, text = l[i],  padx = 100,pady = 10, borderwidth = 5, bg ="#009966", value = var.get()+l[i] ,  variable = var1).pack()
         
        def openFil():
            N = 0
            print(var.get())
            if var.get() == "../puzzles/débutant/".decode('utf-8') :
                N = 14
            if var.get() == "../puzzles/intermédiaire/".decode('utf-8'):
                N = 25
            if var.get() == "../puzzles/avancé/".decode('utf-8'):
                N = 31
            if var.get() == "../puzzles/expert/".decode('utf-8'):
                N = 50
            if var.get() == "../puzzles/test/".decode('utf-8'):  
                nbIt = Label(window1, text="Enterz le nombre de déplacement maximum").pack()
                nn = IntVar()
                def affect():
                    N = int(e.get())
                    nameFile = var1.get()
                    createGrid(generateStruct ( nameFile), N)
                e = Entry(nbIt, textvariable = nn)
                e.pack()
                b3 = Button(window1, text = "Valider", command = affect)
                b3.pack()

            if N != 0 :    
                nameFile = var1.get()
                createGrid(generateStruct ( nameFile), N)
            
        b2 = Button(window1, text = "Afficher", command = openFil)
        b2.pack()
        
        window1.mainloop()
        
    b1 = Button(window, text = "commencer", command = openDir)
  
    b1.pack()

    canvas.pack()

    def openRules():
        pf = open( "../Fichiers/rules.txt", "r")
        ligne = pf.readlines()
        window2 = Tk()
        window2.configure(background="#FFFFCC")
        for i in range(len(ligne)):
            Label(window2, text = ligne[i] , fg = "#000000", bg = "#FFFFCC",font = "Helvetica 10 bold").pack()
        window2.mainloop()
        
    def openManuel():
        pf = open( "../Fichiers/manuel.txt", "r")
        ligne = pf.readlines()
        window2 = Tk()
        window2.configure(background="#FFFFCC")
        for i in range(len(ligne)):
            Label(window2, text = ligne[i] , fg = "#000000", bg = "#FFFFCC",font = "Helvetica 10 bold").pack()
        window2.mainloop()
        
    def openSolveur(): 
        pf = open( "../Fichiers/solveur.txt", "r")
        ligne = pf.readlines()
        window2 = Tk()
        window2.configure(background="#FFFFCC")
        for i in range(len(ligne)):
            Label(window2, text = ligne[i] , fg = "#000000", bg = "#FFFFCC",font = "Helvetica 10 bold").pack()
        window2.mainloop()
    
    def openRead(): 
        pf = open( "../Fichiers/README.txt", "r")
        ligne = pf.readlines()
        window2 = Tk()
        window2.configure(background="#FFFFCC")
        for i in range(len(ligne)):
            Label(window2, text = ligne[i] , fg = "#000000", bg = "#FFFFCC",font = "Helvetica 10 bold").pack()
        window2.mainloop()
      
    #Barre d'outils  
    toolBar = Menu(window)
    menuu = Menu(toolBar)
    menuu.add_command(label = "Régles du jeu Rush Hour", command = openRules)
    menuu.add_separator()
    menuu.add_command(label = "A propos du Solveur", command= openSolveur)
    menuu.add_separator()
    #menuu.add_command(label = "Satistiques sauvegardées", command= openRules)
    #menuu.add_separator()
    menuu.add_command(label = "README", command = openRead)
    menuu.add_separator()
    menuu.add_command(label = "Quitter", command = window.quit)
    toolBar.add_cascade(label = "Menu", menu = menuu)
    
    menuHelp = Menu(toolBar)
    menuHelp.add_command(label = "Manuel d'utilisation", command= openManuel)
    toolBar.add_cascade(label = "Aide", menu = menuHelp)
      
    
    window.config(menu = toolBar)
    window.mainloop()
    