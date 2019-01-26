# -*- coding: utf-8 -*

"""

Fonction permettant de lire le fichier .msh généré par GMSH

"""

from matrice import Solveur

def export(solution, output = "maillage.vtu"):
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
