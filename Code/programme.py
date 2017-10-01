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

#createGrid("../puzzles/intermédiaire/jam17.txt")    
    
def resolvePl( matrix, N, mode):
     
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
     model.setParam('TimeLimit', 2*60)
     #Déclaration des variables de décision
     x = dict()
     z = dict()
     y = dict()
     v = dict()
     p = dict()
     m = dict()
     

     for i in d.keys():
         x[i] = dict()
         y[i] = dict()
         z[i] = dict()
         v[i] = len(d[i]) 
         m[i] = dict()
         
         if (d[i][1] - d[i][0]) == 1 :  #cas déplacement horizontale
             ba = int(d[i][0] / len(matrix)) * len(matrix) + 1
             if v[i] == 2 : 
                 bf = (int(d[i][0] / len(matrix)) + 1 ) * len(matrix)  
             if v[i] == 3 :
                 bf = (int(d[i][0] / len(matrix)) + 1) * len(matrix) - 1
             pas = 1
         
         if(d[i][1] - d[i][0]) == len(matrix) :
             if d[i][0] % len(matrix) != 0:
                 ba = d[i][0] % len(matrix)
             else :
                 ba = len(matrix)
             if v[i] == 2 : 
                 bf = ba + len(matrix) * (len(matrix) - 1)
             if v[i] == 3 :
                 bf = ba + len(matrix) * (len(matrix) - 2)
             pas = len(matrix)
                 
         for l in range( ba, bf, pas):
             x[i][l] = dict()
             y[i][l] = dict()
             z[i][l] = dict()
             m[i][l] = list()
             
             for bcl in range( l, l + (v[i] * pas) , pas):
                 m[i][l].append(bcl)               
                
             for k in range( N + 1 ):
                 x[i][l][k] = model.addVar( vtype = GRB.BINARY)
                 z[i][l][k] = model.addVar( vtype = GRB.BINARY)
                        
             for f in range(ba, bf, pas):
                 if f!= l :
                     y[i][l][f] = dict()
                     for k in range( 1, N +1):
                         y[i][l][f][k] = model.addVar(vtype = GRB.BINARY)
        
         for ss in range( 0, (v[i] - 1) * pas , pas):
             z[i][bf + ss] = dict()
             for k in range( N + 1):
                      z[i][bf + ss ][k] = model.addVar(vtype = GRB.BINARY)

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
     
     for i in d.keys():
         for j in y[i].keys() :
             for l in y[i][j].keys() :
                 for k in range(1, N + 1):
                     if mode == "RHM":
                         obj += y[i][j][l][k] #* (len(p[j][l]) - 1)
                     if mode == "RHC":
                         obj += y[i][j][l][k] * (len(p[j][l]) - 1)
                     
     model.setObjective( obj, GRB.MINIMIZE)
     
     # Définition des contraintes
     
     # 1) Contraintes initiales
     for i in d.keys() :
         for j in x[i].keys():
             if d[i][0] == j :
                 model.addConstr(x[i][j][0] == 1) 
  

    
     # 2) Contrainte de résolution
       
     
     # S z[i][j][k] == vi seul v[i] cases sont occupées par le véhicule idans sa rangée
     for k in range( N +1 ): 
         for i in d.keys():
             model.addConstr(quicksum(z[i][j][k] for j in z[i].keys()) == v[i])
            
     
     #v[i] * x[i][j][k] <= S z[i][m][k] avec m E m[i] assure que z[i][cm][k] = 1 pour toute case cm occupée par i au terme du k ème mouvement        
     for i in d.keys():
         for j in x[i].keys():
             for k in range (N + 1 ): 
                 model.addConstr(quicksum(z[i][cm][k] for cm in m[i][j]) >= ( x[i][j][k] * v[i]))
                       

     # S z[i][j][k] <= 1 assure qu'une case est occupée au plus par un seul véhicule             
     for j in range(len(matrix) * len(matrix) + 1):
         for k in range(N + 1):
             model.addConstr(quicksum(z[i][j][k] for i in d.keys() if j in z[i].keys()) <=  1 )

      
     # y[i][j][l][k] <= 1 - S z[î][p][k-1]                       
     for i in d.keys():
         for j in y[i].keys():
             for l in y[i][j].keys():
                 for k in range( 1, N +1 ):
                        for cm in p[j][l]:
                         #model.addConstr(y[i][j][l][k] <= 1 - (quicksum(z[ii][cm][k -1] for ii in d.keys() for cm in p[j][l] if cm in z[ii].keys() and ii != i and cm in m[ii]) / len(p[j][l])))  
                            model.addConstr(y[i][j][l][k] <= 1 - (quicksum(z[ii][cm][k -1] for ii in d.keys() if cm in z[ii].keys() and ii != i and cm in m[ii]) )) 
                         
            
      # x[g][17][N] == 1
     model.addConstr(x['g'][17][N] ==1)

            
                                  
      #S y[i][j][l][k] <= 1 au plus un déplacement
     for k in range(1, N + 1):       
         model.addConstr(quicksum(y[i][j][l][k] for i in d.keys() for j in y[i].keys() for l in y[i][j].keys()) <= 1)  
  
            
      #y[i][j][l][k]-x[i][l][k] == 0                            
     for i in d.keys(): 
         for k in range(1, N + 1 ):
              for j in y[i].keys():
                  model.addConstr(quicksum(y[i][j][l][k] for l in y[i][j].keys()) <= x[i][j][k - 1] )
                  #model.addConstr(quicksum(y[i][l][j][k] for l in y[i].keys() if j in y[i][l].keys()) <= x[i][j][k])
     for i in d.keys(): 
         for k in range(1, N + 1 ):
              for j in y[i].keys():
                  for l in y[i][j].keys():
                      model.addConstr( y[i][j][l][k] <= x[i][l][k])
                      model.addConstr(x[i][j][k -1] + x[i][l][k] - y[i][j][l][k] <= 1)
                      #model.addConstr( (2 * y[i][j][l][k]) <= x[i][j][k -1] + x[i][l][k] )
    
                      
    
     for k in range(1, N + 1):
        for i in d.keys():
            model.addConstr(quicksum(x[i][j][k] for j in x[i].keys()) == 1 )



    
      
     model.optimize()    

     print(model)
         
     
     return x,y, model

  
                     
        
        
          
#print(generateStruct("../puzzles/débutant/jam1.txt"))
#createGrid("../puzzles/intermédiaire/jam17.txt")

#resolvePl("../puzzles/débutant/jam3.txt", 14)