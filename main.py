# -*- coding: utf-8 -*

import sys
from matrice import assemblage





if __name__ == '__main__':

	assert len(sys.argv) == 2, "Veuillez fournir un seul fichier .msh, par exemple: \npython2 main.py file.msh"
	A,B = assemblage(sys.argv[1])
	print(A)
