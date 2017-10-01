#!/usr/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 17:03:59 2016

@author: Licia AMICHI
"""

import numpy
from Tkinter import *
#import tkinter.font as tkFont
from gurobipy import *


    #__________________________Couleurs de voitures___________________________#
palette1 = [ "#003366", "#FF3300", "#FFCC00", "#66CC00", "#990099", "#FF66CC", "#000000", "#330000", "#666633", "#00CCFF" , "#FF9966", "#F0066","#663300", "#66FF00"]

    #__________________________Couleurs de camions____________________________#
palette2 = [ "#FF66CC", "#000000", "#330000", "#666633", "#00CCFF" , "#FF9966", "#F0066","#663300", "#66FF00","#003366", "#FF3300", "#FFCC00", "#66CC00", "#990099"]


x0, y0 = 60, 60
c1 = 75

def generateStruct ( fileName ) :
    
    pf = open( fileName, "r")
    lignes = pf.readlines()
    pf.close()
    size = lignes[0].split()
    
    #__________________________dimensions de la grille________________________#
    sizeLigne = int( size[0])
    sizeColumn = int( size[1])
    

    
    #______________________Matrice représentant la grille ____________________#
    matrix = numpy.zeros(shape = ( sizeLigne, sizeColumn), dtype = dict)
    for i in range( 1, len( lignes)):
        matrix[i-1] = lignes[i].split()

    return matrix
    


def createGrid( fileName ):
    
    matrix = generateStruct( fileName)
    window = Tk()
    size = len (matrix)
 
    
    canvas = Canvas( window, width = 900, height = 600, bg = "white")    
    for k in range( size + 1):
        if k > 0 :
            for j in range(size):
                if ( matrix[j][k-1] == 'g' ) :
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = '#CC0000')
                elif matrix[j][k-1] == '0'  :
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = '#FFCC99')
                elif matrix[j][k-1][0] == 'c':
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = palette1[int(matrix[j][k-1][1])-1])
                elif matrix[j][k-1][0] == 't':
                    canvas.create_rectangle(  x0 + c1 * (k-1) , y0 + c1 * j, x0 + c1 * k ,  y0 + c1 * (j + 1), fill = palette2[int(matrix[j][k-1][1])-1])
                
    canvas.create_line(x0 + c1 * size, y0 + c1 * 2, x0 + c1 * size, y0 + c1 * 3, fill = "#330066", width = 3 )
    canvas.create_text( x0 + c1 * (size + 1) , y0 + c1 * 2.5, text = "SORTIE", fill = "#330066", font = "Helvetica 26 bold")
    canvas.pack()
    
    window.mainloop()
  

def move( d , v, matrixLength):
    if (d[1] - d[0]) == 1 :  #cas déplacement horizontale
             ba = int(d[0] / matrixLength) * matrixLength + 1
             if v == 2 : 
                 bf = (int(d[0] / matrixLength) + 1 ) * matrixLength 
             if v == 3 :
                 bf = (int(d[0] / matrixLength) + 1) * matrixLength - 1
             pas = 1
         
    if(d[1] - d[0]) == matrixLength :
             if d[0] % matrixLength != 0:
                 ba = d[0] % matrixLength
             else :
                 ba = matrixLength
             if v == 2 : 
                 bf = ba + matrixLength * (matrixLength - 1)
             if v == 3 :
                 bf = ba + matrixLength * (matrixLength - 2)
             pas = matrixLength
    return ba, bf, pas
    
    
    
    
    
def resolvePl( fileName, N ):

     matrix = generateStruct( fileName)
     
     #Determiner le sous-esnemble de variables à utiliser
     d = dict()
     
     for i in range( len(matrix)):
         for j in range( len(matrix)):
             if matrix[i][j] != '0' :
                 if matrix[i][j] in d:
                    a = list()
                    for s in range (len(d[matrix[i][j]])):
                        a.append(d[matrix[i][j]][s])
                    a.append( i * len(matrix) + ( j + 1))
                    d[matrix[i][j]] = a
                 else:
                    d[matrix[i][j]] = list()
                    d[matrix[i][j]].append(i * len(matrix) + ( j + 1 ))
  
    
     model = Model('Resolver')
     
     #Déclaration des variables de décision
     v = dict()
     p = dict()
     m = dict()
     listX = tuplelist()
     listY = tuplelist()
     listZ = tuplelist()
     
     for i in d.keys():
         v[i] = len(d[i]) 
         m[i] = dict()
         
         ba, bf, pas = move( d[i] , v[i], len(matrix))

         for l in range( ba, bf, pas):
             m[i][l] = list()
             
             for bcl in range( l, l + (v[i] * pas) , pas):
                 m[i][l].append(bcl)               
                
             for k in range( N + 1 ):
                 if (i,l,k) not in listX:
                     listX.append((i, l, k))
                 if (i,l,k) not in listZ:
                     listZ.append((i, l, k))
                 for ss in range( 0, (v[i] - 1) * pas , pas):
                     if (i, ss + bf , k) not in listZ:
                         listZ.append((i, ss + bf , k))
                        
             for f in range(ba, bf, pas):
                 if f!= l :
                     for k in range( 1, N +1):
                         if (i,l,f,k) not in listY:
                             listY.append((i, l, f, k))
        


     

     x = dict()
     for (i,j,k) in listX :
         x[(i,j,k)] = model.addVar(vtype = GRB.BINARY)
                    
     y = dict()
     for (i, j, l, k) in listY :
         y[( i, j, l, k)] = model.addVar(vtype = GRB.BINARY)
         
     z = dict()
     for ( i, j, k) in listZ :
         z[( i, j, k)] = model.addVar(vtype = GRB.BINARY)

     model.update()  

     
     #construction de p    
     for i in range(1, len(matrix) * len(matrix) + 1) :
        p[i] = dict()
        for j in range( 1, len (matrix) * len(matrix) + 1):
            cc = 0
            if (i % len(matrix)) == ( j % len(matrix)) : # meme colonne 
                pas = len(matrix)
                cc =1
            if int(i / len(matrix)) == int(j / len(matrix)) : # meme ligne
                pas = 1
                cc = 1
            if cc == 1 : 
                g = min(i,j)
                bs = max(i,j)
                p[bs] = dict()
                while g <= bs:
                    if g not in p.keys():
                        p[g] = dict()
                    p[g][bs] = list()
                    p[bs][g] = list()
                    g += pas
                    
            
     for i in p.keys():
        for j in p[i].keys():
            if (i % len(matrix)) == ( j % len(matrix)) : # meme colonne 
                pas = len(matrix)
            if int(i / len(matrix)) == int(j / len(matrix)) : # meme ligne
                pas = 1
            g = min(i,j)
            bs = max(i,j)
            for g in range(min(i , j) , max( i, j) + 1 , pas):
                for bcl in range(g, bs +1, pas):
                    if bcl not in p[g][bs]:
                        p[g][bs].append(bcl)
                p[bs][g] = p[g][bs]

       
     # Définition fonction objectif              
     obj = LinExpr()
     obj = 0    
     
     for (i, j, k, l) in listY:
         obj += y[(i, j, k, l)]
                     
     model.setObjective( obj, GRB.MINIMIZE)
     
     # Définition des contraintes
     
     # 1) Contraintes initiales
     nb = 0.0
     for ( i, j, k) in listX:
         if d[i][0] == j:
             model.addConstr(x[(i,j,0)] == 1)
             nb += 1
         else :
             model.addConstr(x[(i,j,0)] == 0)

                
                 

     
     # 2) Contrainte de résolution
     
     #v[i] * x[i][j][k] <= S z[i][m][k] avec m E m[i] assure que z[i][cm][k] = 1 pour toute case cm occupée par i au terme du k ème mouvement     
     for (i, j, k) in listX:
         model.addConstr(quicksum(z[(i, cm, k)] for cm in m[i][j]) >= ( x[(i, j, k)] * v[i]))
     

                             

     # S z[i][j][k] <= 1 assure qu'une case est occupée au plus par un seul véhicule         
     for (i, j, k) in listZ:
         model.addConstr(quicksum(z[(ii, j, k)] for ii in d.keys() if (ii, j, k) in listZ) <= 1)
         
         
         
     # S z[i][j][k] == vi seul v[i] cases sont occupées par le véhicule idans sa rangée
     for (i, j, k) in listZ:
         model.addConstr(quicksum(z[(i,jj,k)] for jj in range(1, len(matrix) * len(matrix) +1) if (i, jj, k) in listZ) == v[i])

            
     # y[i][j][l][k] <= 1 - S z[î][p][k-1]                  
     for (i,j,l,k) in listY:
         for cm in p[j][l]:
             model.addConstr(y[(i,j,l,k)] <= (1 - quicksum(z[(ii,pp,c)] for (ii,pp ,c) in listZ if ii != i and c == k-1 and pp == cm)))
             
          
     # x[g][17][N] == 1
     model.addConstr(x[('g', 17, N)] == 1)

     #S y[i][j][l][k] <= 1 au plus un déplacement
    
     for k in range(1 , N + 1):
         model.addConstr(quicksum(y[(i,j,l,c)] for (i,j,l,c) in listY if c == k)  <= 1)

                  
      #y[i][j][l][k]-x[i][l][k] == 0
                  
     for (i,j,l,k) in listY:
         model.addConstr(y[(i,j,l,k)] <= x[(i,j,k -1)])
         model.addConstr(y[(i,j,l,k)] <= x[(i,l,k)])
         model.addConstr(x[(i,j,k-1)] + x[(i,l,k)] - y[(i,j,l,k)] <= 1)

    
     """for k in range(N + 1):
         model.addConstr( quicksum( x[i][j][k] for i in d.keys() for j in x[i].keys()) == nb )"""

     """for kk in range( N + 1):
         model.addConstr(quicksum( x[(i,j,k)] for (i,j,k) in listX if k == kk) == nb)"""
    
     for k in range(N + 1):
         model.addConstr(quicksum( x[(i,j,k)] for (i,j,kk) in listX if kk == k ) == len(d))

         
     model.optimize()    

     print(model)

     """for (i,j,k) in listX :
         somme = 0
         for cm in m[i][j]:
             somme += z[(i,cm,k)].x
         print(somme - v[i]* x[(i,j,k)].x)"""
         
         
     """for(i,j,k) in listZ :
         somme = 0
         for ii in d.keys():
             if (ii,j,k) in listZ:
                 somme+= z[(ii,j,k)].x
         print "z",ii," ",k,"=",somme"""
         

             
     """for (i,j,k) in listZ:
         somme =0
         for jj in range(1,37):
             if (i,jj,k) in listZ:
                 somme += z[(i,jj,k)].x
         print "z",i,"=",somme - v[i]"""
             

     """for i in d.keys():
         for j in y[i].keys():
             for l in y[i][j].keys():
                 for k in range(1, N + 1):
                     if y[i][j][l][k].x == 1.0 :
                         print "y",i,j,l,k,"=",y[i][j][l][k].x"""
     
     print ""
     print 'Solution optimale:'
     print ""
     #print 'Valeur de la fonction objectif : ', model.objVal

      
     for (i,j,l,k) in listY:
         if y[(i,j,l,k)].x == 1:
             print(" ",i," ",j," ",l," ",k)
                     
  
        
          
#print(generateStruct("../puzzles/débutant/jam1.txt"))
#createGrid("../puzzles/intermédiaire/jam17.txt")"""

resolvePl("../puzzles/débutant/jam1.txt", 14)
