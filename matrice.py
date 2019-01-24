# -*- coding: utf-8 -*


from read_msh import read_msh
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix, linalg

list_element = []

class Solveur:
	def __init__(self,mesh_file):
		if mesh_file == None:
			raise ValueError("Veuillez fournir un fichier .msh à notre solveur")
		self.nb_point,self.list_point,self.nb_element,self.list_element,self.nb_noTriangle = read_msh(mesh_file)
		# Le nombre de edge est ici pour sauter les premières éléments qui sont des arêtes

	def loc2glob(self,triangle, sommet):
		if sommet <= 0 and sommet > 3:
			raise Exception("Veuillez fournir un sommet compris entre 1 et 3")

		if self.list_element[triangle-1].type == 1 and sommet >= 3:
			raise Exception("Veuillez fournir un sommet locale inférieur ou égal à 2 pour un segment!")

		return self.list_element[triangle-1].list_index[sommet] # -1 car on commence à 0

	def matriceMasse(self):
		data = []
		ind_ligne = []
		ind_col = []

		for p in range(self.nb_noTriangle+1,self.nb_element+1):
			p1 = self.list_point[self.loc2glob(p,0)-1] # -1 car on commence à 0
			p2 = self.list_point[self.loc2glob(p,1)-1]
			p3 = self.list_point[self.loc2glob(p,2)-1]

			det_jaccob = (p2[0] - p1[0])*(p3[1] - p1[1]) - (p3[0] - p1[0])*(p2[1] - p1[1])

			for i in range(3):
				I = self.loc2glob(p,i) - 1
				for j in range(3):
					J = self.loc2glob(p,j) - 1

					if I == J:
						data.append(det_jaccob/12.0)
					else:
						data.append(det_jaccob/24.0)
					ind_ligne.append(I)
					ind_col.append(J)

		self.M = coo_matrix((data, (ind_ligne,ind_col)))#.tocsr()
		# Vérification
		U = np.ones((self.nb_point,1))
		test = self.M.dot(U)
		print(sum(test))

	def matriceRigidite(self):
		# self.D = np.zeros((self.nb_point,self.nb_point)) # Matrice de rigidité # à faire au format COO
		data = []
		ind_ligne = []
		ind_col = []

		grad_phi = [np.array([[-1,-1]]), np.array([[1,0]]), np.array([[0,1]])] # gradient de phi dans le triangle de ref

		for p in range(self.nb_noTriangle+1,self.nb_element+1):
			p1 = self.list_point[self.loc2glob(p,0)-1] # -1 car on commence à 0
			p2 = self.list_point[self.loc2glob(p,1)-1]
			p3 = self.list_point[self.loc2glob(p,2)-1]

			det_jaccob = (p2[0] - p1[0])*(p3[1] - p1[1]) - (p3[0] - p1[0])*(p2[1] - p1[1])

			B_rigidite = 1.0/det_jaccob * np.array([[p3[1] - p1[1], p1[1] - p2[1]],
								   					[p1[0] - p3[0], p2[0] - p1[0]]])

			for i in range(3):
				I = self.loc2glob(p,i) - 1
				for j in range(3):
					J = self.loc2glob(p,j) - 1

					ind_ligne.append(I)
					ind_col.append(J)

					d_temp = grad_phi[j].dot(B_rigidite)
					# D[I,J] += det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i]))
					# print det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i]))
					data.append((det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i])))[0][0]) # [0][0] car dot donne une liste de liste avec seulement une valeur
					
		self.D = coo_matrix((data, (ind_ligne,ind_col)))#.tocsr()
		# Vérification
		U = np.ones((self.nb_point,1))
		print(sum(self.D.dot(U)))


	def assemblage(self):
		self.matriceMasse()
		self.matriceRigidite()

		self.A = (self.M + self.D).tolil() # pour faciliter la mise à 0 de la matrice
		self.B = np.zeros((self.nb_point,1),dtype=complex)

		for index,element in enumerate(self.list_element):
			if element.physical == 3: # bord du sous-marin
				# print(index, " ", element)
				for point in element.list_index: # les points du bord
					# print(point," ",self.list_point[point])
					self.A[point-1,:] = 0
					self.A[:, point-1] = 0
					self.A[point-1,point-1] = 1
					self.B[point-1] = self.u_inc(self.list_point[point-1][0], self.list_point[point-1][1])


		self.A = self.A.tocsr()
		# print type(self.A)
		self.U = linalg.spsolve(self.A, self.B)

		# print self.U
		np.savetxt("test.csv",self.U, delimiter=",")
		# 
		# print self.A
		# np.savetxt("test.csv",self.A, delimiter = ",")
		# print(A)
		
	def u_inc(self,x,y):
		alpha = 1
		return np.exp(np.complex(0,2*np.pi)*(x*np.cos(alpha) + y*np.sin(alpha)))


	def export(self, output = "maillage.vtu"):
		with open(output,"w") as file:
			file.write('<VTKFile type="UnstructuredGrid" version="1.0" byte_order="LittleEndian" header_type="UInt64">')
			file.write('\n<UnstructuredGrid>')
			file.write('\n<Piece NumberOfPoints="' + str(self.nb_point) + '" NumberOfCells="' + str(self.nb_element) + '">')
			file.write('\n<Points>')
			file.write('\n<DataArray NumberOfComponents="3" type="Float64">')

			for coordonnee in self.list_point:
				file.write('\n' + str(coordonnee[0]) + ' ' + str(coordonnee[1]) + ' ' + str(coordonnee[2]))

			file.write('\n</DataArray>')
			file.write('\n</Points>')
			file.write('\n<Cells>')
			
			off = 0 # valeur de offset en int
			offsets = "" # pour ne pas parcourir plusieurs fois les éléments
			types = ""



			file.write('\n<DataArray type="Int32" Name="connectivity">')
			for indice, element in enumerate(self.list_element):
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
			for reel in self.U.real:
				file.write('\n'+str(reel))
			file.write('\n</DataArray>')

			file.write('\n<DataArray type="Float64" Name="Imag part" format="ascii">')
			for imag in self.U.imag:
				file.write('\n'+str(imag))
			file.write('\n</DataArray>')

			file.write('\n</PointData>\n</Piece>\n</UnstructuredGrid>\n</VTKFile>')
