# -*- coding: utf-8 -*


import sys
from read_msh import read_msh


def loc2glob(triangle, sommet):
	if list_element[triangle].type == 1 and sommet >= 3:
		raise Exception("Veuillez fournir un sommet locale inférieur ou égal à 2 pour un segment!")

	return list_element[triangle].list_index[sommet - 1]



if __name__ == '__main__':

	assert len(sys.argv) == 2, "Veuillez fournir un seul fichier .msh, par exemple: \npython2 main.py file.msh"
	nb_point,list_point,nb_element,list_element = read_msh(sys.argv[1])

	print loc2glob(6549,3)
