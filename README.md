# RushHour

Welcome to Rush Hour SOLVER !

## Introduction:
Pour pouvoir utiliser ce solveur il faut disposer au préalable du langage de programmation Python(v2.7) sur votre machine,
et du solveur Gurobi.
 
Le solveur Rush Hour possède 6 fichiers sources en langage python:

	* dataStructure.py : classe qui définit la structure de données Node.
	* grid.py : contient les fonctions qui génèrent les différentes fenêtres, et qui font appel aux fonctions
	  	 de résolutions choisies à travers l'interface graphique.
	* programme.py: contient la fonction principale de résolution par programmation linéaire, et qui prend 
	      comme paramètre le mode de résolution: "RHM" ou "RHC".
	* programme2.py: contient les fonctions nécessaires à la résolution par l'algorithme de Dijkstra.
	* windows.py : contient la fonction qui génère la première fenêtre.
	* main.py: contient la fonction principale qui fait appel à toutes les autres fonctions.

Cette version permet de bénéficier de ces 4 méthodes de résolution:

 * Résolution par programmation linéaire en variables binaires, minimisant le nombre de mouvements.
 * Résolution par programmation linéaire en variables binaires, minimisant le nombre total de cases de l'ensemble des mouvements.
 * Résolution par l'algorithme de Dijkstra, minimisant le nombre de mouvements.
 * Résolution par l'algorithme de Dijkstra, minimisant le nombre total de cases de l'ensemble des mouvements.
		
## How to use:
Pour pouvoir tester les différentes méthodes il faut entrer ces lignes de commande dans un interpréteur de commande du langage python:

cas Ipython:

  * %run dataStructure.py
	* %run windows.py
	* %run grid.py
	* %run programme2.py
	* %run programme1.py
	* %run main.py
