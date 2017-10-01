#!/usr/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 17:03:59 2016

@author: Licia AMICHI
"""
import numpy   
import dataStructure
import time

def createDic( matrix):
    d = dict() 
    for i in range( len(matrix)):
         for j in range( len(matrix)):
             if matrix[i][j] != str(0)   :
                 if matrix[i][j] in d:
                    a = list()
                    for s in range (len(d[matrix[i][j]])):
                        a.append(d[matrix[i][j]][s])
                    a.append( i * len(matrix) + ( j + 1))
                    d[matrix[i][j]] = a
                 else:
                    d[matrix[i][j]] = list()
                    d[matrix[i][j]].append(i * len(matrix) + ( j + 1 ))
    return d

def createOcc(d, size):
    v = dict()
    for i in d.keys():
        v[i] = dict()
        g = 0
        listI = list()
        listJ = list()
        while g < len(d[i]):
            listI.append(int((d[i][g] - 1) / size))
            listJ.append((d[i][g] - 1) % size)
            g += 1
        for ii in listI:
            v[i][ii] = dict()
            for jj in listJ:
                v[i][ii][jj] = 1                                    
    return v 
    

        
def generateListD(matrix, l):

    listDep = list()
    if len(l) == 1:
        x = list(l.keys())[0]
        compt = 0
        for y in l[x].keys():
            if compt == 0:
                init = y
            if compt == len(l[x]) - 1:
                final = y
            compt += 1
        if init > 0:
            if matrix[x][init - 1] == str(0):
                g = init - 1
                continu = 1
                while( g >= 0  and continu) :
                    if matrix[x][g] == str(0):
                        listDep.append((x, g, init - g))
                        g -= 1
                    else:
                        continu = 0
            
        if final + 1 < len(matrix):
            if  matrix[x][final  + 1] == str(0):
                g = final + 1 
                continu = 1
                while( g < len(matrix)  and continu) :
                    if matrix[x][g] == str(0):
                        listDep.append((x, g, g - final))
                        g += 1
                    else:
                        continu = 0
    else:   
        compt = 0
        for g in l.keys():
            if compt == 0:
                init = g
            if compt == len(l) - 1:
                final = g
            compt += 1
        y = list(l[init].keys())[0]
        if init > 0:
            if matrix[init - 1][y] == str(0):  
                g = init - 1
                continu = 1 
                while( g >= 0  and continu) :
                    if matrix[g][y] == str(0):
                        listDep.append((g, y, init -g))
                        g -= 1
                    else:
                        continu = 0
        
        if final + 1 < len(matrix):
            if (matrix[final + 1][y] == str(0)):
                g = final + 1 
                continu = 1
                while( g < len(matrix)  and continu) :
                    if matrix[g][y] == str(0):
                        listDep.append((g, y, g - final ))
                        g += 1
                    else:
                        continu = 0
               
                 
    return listDep           
            
        
def createNewMatrix(m, dep, l, car):
    nbCell = 0 
    
    matrix = numpy.zeros(shape = ( len(m), len(m)), dtype = dict)
    for ii in range(len(m)):
        for jj in range(len(m)):
            matrix[ii][jj] = m[ii][jj] 
        
    for i in l.keys() :
        for j in l[i].keys():
            if nbCell == 0:
                x = i
                y = j
            matrix[i][j] = str(0)
            nbCell += 1
    if len(l) == 1 : # déplacement sur la ligne
        nbCell = len(l[x])
        if y > dep[1]: # déplacement à gauche
            path = 1
        else:       # déplacement à droite
            path = -1
           
        for k in range(nbCell):
            matrix[dep[0]][dep[1] + k * path] = car
   
    else:           # déplacement sur la colonne
        nbCell = len(l)
        if x > dep[0]:  # déplacement en haut
            path = 1
        else :
            path = -1
        
        for k in range(nbCell):
            matrix[dep[0] + k * path][dep[1]] = car
            
    return matrix
        
        
def isInList(matrix, listeNode):     
    i = 0

    while i < len(listeNode):  
        x = 0
        continu = 1
        while x < len(matrix) and continu:
            y = 0
            while y < len(matrix) and continu:
                if str(matrix[x][y]) == str(listeNode[i].matrix[x][y]):
                    y += 1
                else:
                    continu = 0
            x += 1
        if continu == 0 :
            i += 1 
        
        else : 
            return i
    
    if continu == 0 and i == len(listeNode):
        return -1
                
def minHop(l):
    nb = 0
    ind = -1
    for i in range( len(l)):
        if l[i].took =="n":
            if nb == 0:
                minHop = l[i].nbHop
                ind = i
                nb += 1
            else:
                if l[i].nbHop < minHop:
                    minHop = l[i].nbHop
                    ind = i
    return ind
            
        

        
def createGraph( matrix, mode):
    #matrix = generateStruct ( fileName )
    #configuration courante    
    actualNode = 0
    #liste des configurations
    listeNode = dict()
    actualMatrix = numpy.zeros(shape = ( len(matrix), len(matrix)), dtype = dict)
    for ii in range(len(matrix)):
        for jj in range(len(matrix)):
            actualMatrix[ii][jj] = matrix[ii][jj] 
    ddd = createDic( actualMatrix)
    actualDic  = createOcc(ddd, len(actualMatrix))
    #ajout de la configuration à la liste des configuration
    listeNode[actualNode] = dataStructure.Node(actualNode, matrix ,"n", -1, -1)
    found = 1
    i = actualNode
    i += 1
    while found :
         #Si configuration but
        if  2 in actualDic['g'] and 4 and 5 in actualDic['g'][2] :
            found = 0 
        else:
            for l in actualDic.keys():  
                listDep =  generateListD(actualMatrix, actualDic[l])
                for dep in listDep:
                    if mode == "RHC":
                        nbHop = dep[2]
                    if mode == "RHM":
                        nbHop = 1
                    newMatrix = createNewMatrix(actualMatrix, dep, actualDic[l], l)
                    exist = isInList(newMatrix, listeNode)
                    if exist == -1 :
                        listeNode[i] = dataStructure.Node(i, newMatrix ,"n", nbHop + listeNode[actualNode].nbHop , actualNode)
                        i += 1
                    else :
                        if nbHop + listeNode[actualNode].nbHop < listeNode[exist].nbHop:
                            listeNode[exist].parent = actualNode
                            listeNode[exist].nbHop = listeNode[actualNode].nbHop + nbHop
            
            listeNode[actualNode].took = "t"
            actualNode = minHop(listeNode) 
            if actualNode == -1:
                found = 0
            else:
                actualMatrix = listeNode[actualNode].matrix
                actualDic  = createOcc(createDic(actualMatrix), len(matrix))  
  
    nbb = listeNode[actualNode].nbHop + 1
    pere = listeNode[actualNode].parent
    fils = actualNode
    while pere > -1 :
        listeNode[pere].son = fils
        fils = pere
        pere = listeNode[pere].parent

    return listeNode, nbb
 
def showSolution(matrix, mode):  
     start_time = time.time()
     listeNode, nbb = createGraph(matrix, mode)
     interval = time.time() - start_time
     return  listeNode, nbb, interval
     

    
 
#openFile("../puzzles/débutant/jam1.txt")           
#createGraph("../puzzles/débutant/jam1.txt")        
    
         

#createGrid("../puzzles/débutant/question.txt")

#resolvePl("../puzzles/débutant/question.txt")