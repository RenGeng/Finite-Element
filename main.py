# -*- coding: utf-8 -*

import sys
sys.path.insert(0,'python/')
from matrice import Solveur
from export import export
from argparse import ArgumentParser
from numpy import pi
from os.path import splitext

parser = ArgumentParser()




if __name__ == '__main__':

	# assert len(sys.argv) >= 2, "Veuillez fournir un seul fichier .msh, par exemple: \npython2 main.py file.msh"


	# Add more options if you like
	parser.add_argument("-f", "--file", dest="meshFile",
	                help="Fichier du Maillage generer avec GMSH",required=True, metavar="FILE")

	parser.add_argument("-d", "--dirichlet",
	                dest="Dirichlet", default=3,metavar="N",
	                help="Physical de la condition de Dirichlet [par defaut 3]",type=int)

	parser.add_argument("-r", "--robin",
	                dest="Robin", default=2,metavar="N",
	                help="Physical de la condition de Robin-Fourier [par defaut 2]",type=int)

	parser.add_argument("-a", "--alpha",
	                dest="alpha", default=pi/2,metavar="r",
	                help="Valeur de la variable alpha [par defaut pi/2]",type=float)

	parser.add_argument("-k",
	                dest="k", default=2*pi,metavar="r",
	                help="Valeur de la variable k [par defaut 2*pi]",type=float)

	parser.add_argument("-p", "--paraview", dest="paraview",
	                help="Nom du fichier paraview exporté [par defaut 'paraview/maillage.vtu']",default="Paraview/FILE.vtu", metavar="FILE")
	#paraview

	args = parser.parse_args()

	# print(args.meshFile)
	args.paraview = "Paraview/"+splitext(args.meshFile.split("/")[-1])[0]+".vtu"
	print(args.paraview)

	test = Solveur(args.meshFile,args.k,args.alpha,args.Dirichlet,args.Robin)

	test.matriceMasse()
	test.matriceRigidite()
	test.matriceRobin()
	test.assemblage()
	test.export_all()
	export(test,output=args.paraview)


