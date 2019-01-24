# -*- coding: utf-8 -*

import sys
from matrice import Solveur
from export import export




if __name__ == '__main__':

	assert len(sys.argv) == 2, "Veuillez fournir un seul fichier .msh, par exemple: \npython2 main.py file.msh"
	test = Solveur(sys.argv[1])

	test.matriceMasse()
	test.matriceRigidite()
	test.matriceRobin()
	test.assemblage()
	export(test)
