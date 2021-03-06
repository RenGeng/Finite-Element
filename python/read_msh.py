# -*- coding: utf-8 -*

"""

Fonction permettant de lire le fichier .msh généré par GMSH

"""

from Element import Element

def read_msh(mesh):
	"""
	Lecture du fichier mesh en entrée et retourne:
		- le nombre de point composant le mesh
		- la liste des coordonnées de chaque point
		- le nombre d'élément (segment, triangle, ...)
		- la liste des éléments (voir classe Element)
		- le nombre d'élément qui n'est pas un triangle (pour travailler sur les segments)
	"""
	
	list_point = [] # liste de points

	list_element = [] # liste d'élément (triangles, segments)
	
	nb_noTriangle = 0 # nombre d'élément qui ne sont pas des triangles

	i = 0
	with open(mesh,"r") as file:

		# Skip les 4 premières lignes
		while file.readline() != "$Nodes\n":
			pass
		nb_point = int(file.readline())

		for i in range(nb_point):
			point = file.readline().split(" ")
			list_point.append((float(point[1]), float(point[2]), float(point[3])))
		
		file.readline()
		file.readline()

		nb_element = int(file.readline()) # nombre totale d'élément
		for i in range(nb_element):
			element = list(map(int,file.readline().split(" ")))
			# element = map(int,file.readline().split(" ")) # transforme la liste en int
			nb_tag = element[2]
			# print element[3+nb_tag:]
			if element[1] != 2: # quand c'est un edge
				nb_noTriangle += 1
			list_element.append(Element(element[1], element[3], element[3+nb_tag:]))
			# tag1 = 1 si c'est l'intérieur
			# tag1 = 2 si c'est l'ellips
			# tag1 = 3 si c'est le sous-marin
	return nb_point,list_point,nb_element,list_element,nb_noTriangle
