# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 15:34:25 2016

@author: 3525162
"""


import numpy
from Tkinter import *
#import tkinter.font as tkFont
from gurobipy import *
from programme import *
from programme2 import *
from dataStructure import *
import sys

    #__________________________Couleurs de voitures___________________________#
palette1 = [ "#FF6600", "#660000", "#669933", "#333333", "#669999", "#009966", "#000000", "#99FF33", "#666633", "#00CCFF" , "#FF9966", "#F00066","#663300", "#66FF00"]

    #__________________________Couleurs de camions____________________________#
palette2 = [ "#663300", "#99CC33", "#999966", "#FFCC00", "#66FFCC" , "#999999", "#993300","#663300", "#66FF00","#003366", "#FF3300", "#FFCC00", "#66CC00", "#990099"]


x0, y0 = 60, 60
c1 = 75

def windowPalette():
    window = Tk()
    window.configure(background="#FFFFCC")
    for i in range(len(palette1)):
        Button(window, text = " Voiture c"+str(i +1) ,fg = "#FFFFFF", bg = palette1[i]).pack()
    for i in range(len(palette2)):
        Button(window, text = " Camion t"+str(i +1) ,fg = "#FFFFFF", bg = palette2[i]).pack()
        
    window.mainloop()

def generateStruct ( fileName ) :
    
    pf = open( fileName, "r")
    lignes = pf.readlines()
    pf.close()
    size = lignes[0].split()
    
    #__________________________dimensions de la grille________________________#
    sizeLigne = int( size[0])
    sizeColumn = int( size[1])
    if "g"  not in lignes[3] :
        sys.exit("Configuration impossible")
    
    #______________________Matrice représentant la grille ____________________#
    matrix = numpy.zeros(shape = ( sizeLigne, sizeColumn), dtype = dict)
    for i in range( 1, len( lignes)):
        a = lignes[i].split()
        matrix[i-1] = a
    

    
    return matrix
    

def createGrid( matrix, N ):
    
    #matrix = generateStruct( fileName)
    window = Tk()
    window.configure(background="#FFFFCC")
    size = len (matrix)
 
    
    canvas = Canvas( window, width = 900, height = 600, bg = "#FFFFCC")    
    for k in range( size + 1):
        if k > 0 :
            for j in range(size):
                if ( matrix[j][k-1] == 'g' ) :
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = '#CC0000', outline = '#CC0000' ) 
                elif matrix[j][k-1] == '0'  :
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = '#33FFCC',stipple = 'gray12', outline = '#009966' )
                elif matrix[j][k-1][0] == 'c':
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = palette1[int(matrix[j][k-1].replace('c',''))-1], outline = palette1[int(matrix[j][k-1].replace('c',''))-1])
                elif matrix[j][k-1][0] == 't':
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = palette2[int(matrix[j][k-1].replace('t',''))-1], outline = palette2[int(matrix[j][k-1].replace('t',''))-1])
                
    canvas.create_line(x0 + c1 * size, y0 + c1 * 2, x0 + c1 * size, y0 + c1 * 3, fill = "#CC0000", width = 3 )
    canvas.create_text( x0 + c1 * (size + 1) , y0 + c1 * 2.5, text = "SORTIE", fill = "#99CC99", font = "Helvetica 26 bold")
    
    def resolutionPL1():
        x, y, obj = resolvePl( matrix, N , "RHM")
        show1(y, obj, 1)
        
    def resolutionPL2():
        x, y, obj = resolvePl( matrix, N , "RHC")  
        show1(y, obj, 2)
        
    def resolutionGraphe1():
        listeNode, nbb, interval = showSolution(matrix, "RHM")
        show2(listeNode, nbb, 1, interval)
    def resolutionGraphe2():
        listeNode, nbb, interval = showSolution(matrix, "RHC")
        show2(listeNode, nbb, 2, interval)
        
    
    b1 = Button(window, text = "Résolution PL RHM", bg = "#009966", command = resolutionPL1)
    b1.config(height = 1, width = 60)
    b2 = Button(window, text = "Résolution PL RHC", bg = "#009966", command = resolutionPL2)
    b2.config(height = 1, width = 60)
    b3 = Button(window, text = "Résoltion Dijkstra RHM", bg = "#009966", command = resolutionGraphe1)
    b3.config(height = 1, width = 60)
    b4 = Button(window, text = "Résoltion Dijkstra RHC", bg = "#009966", command = resolutionGraphe2)
    b4.config(height = 1, width = 60)
    b1.pack()
    b2.pack()
    b3.pack()
    b4.pack()
    canvas.pack()
    window.mainloop()
    
def show1(y, obj, mode):
    window = Tk()
    window.configure(background="#FFFFCC")
    if mode == 1:
        welcomeLabel2 = Label(window, text = "Le nombre de mouvement minimum = "+ str(obj.objVal),fg = "#99CC99",bg = "#FFFFCC", font = "Helvetica 12 bold")
    if mode ==2 :
        welcomeLabel2 = Label(window, text = "Le nombre de total de cases de l'ensemble des mouvements = "+ str(obj.objVal),fg = "#99CC99",bg = "#FFFFCC", font = "Helvetica 12 bold")
    welcomeLabel2.place( x = 200, y = 120, width = 200, height = 200)
    welcomeLabel2.pack()
    kl = y['g'][16][17].keys()
    kl.sort()
    for k in kl:
        for i in y.keys():
            for j in y[i].keys():
                for l in y[i][j].keys():
                #for k in y[i][j][l].keys():
                    if y[i][j][l][k].x == 1:
                        mvt = "Déplacement du véhicule "+str(i)+str(" de la case ")+str(j)+str(" vers ")+str(l)+str(" au terme du ")+str(k)+str(" eme mouvement")
                        welcomeLabel = Label(window, text = mvt , fg = "#000000", bg = "#FFFFCC",font = "Helvetica 10 bold")
                        welcomeLabel.place( x = 10 )
                        welcomeLabel.pack()
    windowPalette()    
    window.mainloop()
    
def show2(listeNode, nbb, mode, interv):
    matrix = listeNode[0].matrix
    if mode == 1:
        msg = " Le nombre de mouvement minimum =" + str(nbb)
    elif mode == 2:
        msg = "Le nombre de total de cases de l'ensemble des mouvements ="+ str(nbb)
    i = 0
    while listeNode[i].son > -1:
        i = listeNode[i].son
        matrix = listeNode[i].matrix
        if listeNode[i].son == -1:
            a = showMat(matrix, 1, msg, interv, len(listeNode))
        else :
            a = showMat(matrix,0, msg, interv,len(listeNode))
            windowPalette()
        a.destroy()

    
def showMat( matrix, mode, msg, interv, nConfR):
        window1 = Tk()
        window1.configure(background="#FFFFCC")
        size = len (matrix)
        canvas = Canvas( window1, width = 900, height = 600, bg = "#FFFFCC")    
        for k in range( size + 1):
            if k > 0 :
                for j in range(size):
                    if ( matrix[j][k-1] == 'g' ) :
                        canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = '#CC0000', outline = '#CC0000' )
                 
                    elif matrix[j][k-1] == '0'  :
                         canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = '#33FFCC',stipple = 'gray12', outline = '#009966' )
                    elif matrix[j][k-1][0] == 'c':
                         canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = palette1[int(matrix[j][k-1].replace('c',''))-1], outline = palette1[int(matrix[j][k-1].replace('c',''))-1])
                    elif matrix[j][k-1][0] == 't':
                         canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = palette2[int(matrix[j][k-1].replace('t',''))-1], outline = palette2[int(matrix[j][k-1].replace('t',''))-1])
                
                
        canvas.create_line(x0 + c1 * size, y0 + c1 * 2, x0 + c1 * size, y0 + c1 * 3, fill = "#CC0000", width = 3 )
        canvas.create_text( x0 + c1 * (size + 1) , y0 + c1 * 2.5, text = "SORTIE", fill = "#99CC99", font = "Helvetica 26 bold")
        Label(window1, text = msg , fg = "#99CC99", bg = "#FFFFCC",font = "Helvetica 16 bold").pack()
        Label(window1, text = "Le temps d'exécution total = "+str(interv), fg = "#99CC99", bg = "#FFFFCC",font = "Helvetica 16 bold").pack()
        Label(window1, text = "Le nombre de configurations réalisables est = "+str(nConfR), fg = "#99CC99", bg = "#FFFFCC",font = "Helvetica 16 bold").pack()
        if mode == 0 :
            b1 = Button(window1, text = "Configuration suivante", bg = "#009966",command = window1.quit)
            b1.config(height = 2, width = 60)
            b1.pack()
        elif mode == 1:
            Label(window1, text = "          Solution finale        ", fg = "#99CC99", bg = "#FFFFCC",font = "Helvetica 36 bold").pack()
        canvas.pack()
        window1.mainloop()
        return window1