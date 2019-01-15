# -*- coding: utf-8 -*

"""

Fonction permettant de lire le fichier .msh généré par GMSH

"""

from Element import Element

def read_msh(mesh):
	list_point = [] # liste de points

	list_element = [] # liste d'élément (triangles, segments)
	
	nb_triangle = 0

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
			element = map(int,file.readline().split(" ")) # transforme la liste en int
			nb_tag = element[2]
			# print element[3+nb_tag:]
			if element[1] == 2: # quand c'est un triangle
				nb_triangle += 1
			list_element.append(Element(element[1], element[3], element[3+nb_tag:]))

	return nb_point,list_point,nb_element,list_element,nb_triangle
