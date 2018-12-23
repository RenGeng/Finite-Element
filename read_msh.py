# -*- coding: utf-8 -*

"""

Fonction permettant de lire le fichier .msh généré par GMSH

"""

from Element import Element

def read_msh(mesh):
	list_point = {} # liste de points

	list_element = {} # liste d'élément (triangles, segments)
	i = 0
	with open(mesh,"r") as file:

		# Skip les 4 premières lignes
		while file.readline() != "$Nodes\n":
			pass
		nb_point = int(file.readline())

		for i in range(nb_point):
			point = file.readline().split(" ")
			list_point[point[0]] = (float(point[1]), float(point[2]), float(point[3]))
		
		file.readline()
		file.readline()

		nb_element = int(file.readline())
		for i in range(nb_element):
			element = map(int,file.readline().split(" ")) # transforme la liste en int
			nb_tag = element[2]
			# print element[3+nb_tag:]
			list_element[element[0]] = Element(element[1], element[3], element[3+nb_tag:])

	return nb_point,list_point,nb_element,list_element
