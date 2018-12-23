# -*- coding: utf-8 -*


import sys
from read_msh import read_msh


if __name__ == '__main__':

	assert len(sys.argv) == 2, "Veuillez fournir un seul fichier .msh, par exemple: \npython2 main.py file.msh"
	nb_point,list_point,nb_element,list_element = read_msh(sys.argv[1])
	

print list_element
