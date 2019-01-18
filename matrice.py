# -*- coding: utf-8 -*


from read_msh import read_msh
import numpy as np

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
		self.M = np.zeros((self.nb_point,self.nb_point)) # Matrice de masse # à faire au format COO

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
						self.M[I,J] += det_jaccob/12.0 # car 2 fois l'aire
					else:
						self.M[I,J] += det_jaccob/24.0


		# Vérification

		# Matrice de masse
		U = np.ones((self.nb_point,1))
		test = self.M.dot(U)
		print(sum(test))

	def matriceRigidite(self):
		self.D = np.zeros((self.nb_point,self.nb_point)) # Matrice de rigidité # à faire au format COO

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
					d_temp = grad_phi[j].dot(B_rigidite)
					self.D[I,J] += det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i]))

		# Vérification

			# Matrice de rigidité
		U = np.ones((self.nb_point,1))
		print(sum(self.D.dot(U)))


	def assemblage(self):
		self.matriceMasse()
		self.matriceRigidite()

		A = self.M + self.D
		self.B = np.zeros(self.nb_point,dtype=complex)

		print(self.list_point[0])

		for index,element in enumerate(self.list_element):
			if element.physical == 3: # bord du sous-marin
				# print(index, " ", element)
				for point in element.list_index: # les points du bord
					# print(point," ",self.list_point[point])
					A[point-1,:] = 0
					A[:, point-1] = 0
					A[point-1,point-1] = 1
					self.B[point-1] = self.u_inc(self.list_point[point-1][0], self.list_point[point-1][1])

		np.savetxt("test.csv",A)
		# print(A)
		
	def u_inc(self,x,y):
		alpha = 1
		return np.exp(np.complex(0,2*np.pi)*(x*np.cos(alpha) + y*np.sin(alpha)))
