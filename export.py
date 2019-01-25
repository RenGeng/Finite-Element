# -*- coding: utf-8 -*

"""

Fonction permettant de lire le fichier .msh généré par GMSH

"""

from matrice import Solveur

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


def export(solution, output = "Data/maillage.vtu"):
	"""
	export la solution trouvé au format .vtu lisible par paraview

	solution doit être une instance de la classe Solveur

	le fichier généré par défaut est maillage.vtu
	"""
	if not isinstance(solution, Solveur):
		raise ValueError("La solution que vous donnez doit être de type Solveur")


	with open(output,"w") as file:
		file.write('<VTKFile type="UnstructuredGrid" version="1.0" byte_order="LittleEndian" header_type="UInt64">')
		file.write('\n<UnstructuredGrid>')
		file.write('\n<Piece NumberOfPoints="' + str(solution.nb_point) + '" NumberOfCells="' + str(solution.nb_element) + '">')
		file.write('\n<Points>')
		file.write('\n<DataArray NumberOfComponents="3" type="Float64">')

		for coordonnee in solution.list_point:
			file.write('\n' + str(coordonnee[0]) + ' ' + str(coordonnee[1]) + ' ' + str(coordonnee[2]))
		
		file.write('\n</DataArray>')
		file.write('\n</Points>')
		file.write('\n<Cells>')
			
		off = 0 # valeur de offset en int
		offsets = "" # pour ne pas parcourir plusieurs fois les éléments
		types = ""

		file.write('\n<DataArray type="Int32" Name="connectivity">')
		for indice, element in enumerate(solution.list_element):
			file.write('\n' + " ".join(str(s-1) for s in element.list_index))

			if element.type == 1: # segment
				types += "\n" + str(3) # 3 représente un segment pour paraview
				off += 2
			elif element.type == 2: # triangle
				types += "\n" + str(5) # 5 représente un triangle pour paraview
				off += 3

			offsets += "\n" + str(off)

		file.write('\n</DataArray>')

		file.write('\n<DataArray type="Int32" Name="offsets">')
		file.write(offsets)
		file.write('\n</DataArray>')

		file.write('\n<DataArray type="UInt8" Name="types">')
		file.write(types)
		file.write('\n</DataArray>')
		file.write('\n</Cells>')

		file.write('\n<PointData Scalars="solution">')

		file.write('\n<DataArray type="Float64" Name="Real part" format="ascii">')
		for reel in solution.U.real:
			file.write('\n'+str(reel))
		file.write('\n</DataArray>')

		file.write('\n<DataArray type="Float64" Name="Imag part" format="ascii">')
		for imag in solution.U.imag:
			file.write('\n'+str(imag))
		
		file.write('\n</DataArray>')

		file.write('\n</PointData>\n</Piece>\n</UnstructuredGrid>\n</VTKFile>')
