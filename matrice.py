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

	def assemblage(self):
		A = np.zeros((self.nb_point,self.nb_point))
		B = np.zeros(self.nb_point)

		for p in range(self.nb_noTriangle+1,self.nb_element+1):
			p1 = self.list_point[self.loc2glob(p,0)-1] # -1 car on commence à 0
			p2 = self.list_point[self.loc2glob(p,1)-1]
			p3 = self.list_point[self.loc2glob(p,2)-1]

			# print "triangle: ", p
			# print "index 0: ", self.loc2glob(p,0)
			# print p1

			# print "index 1: ", self.loc2glob(p,1)
			# print p2

			# print "index 2: ", self.loc2glob(p,2)
			# print p3

			det_jaccob = (p2[0] - p1[0])*(p3[1] - p1[1]) - (p3[0] - p1[0])*(p2[1] - p1[1])

			for i in range(3):
				I = self.loc2glob(p,i) - 1
				for j in range(3):
					J = self.loc2glob(p,j) - 1

					if I == J:
						A[I,J] += det_jaccob/12 # car 2 fois l'aire
					else:
						A[I,J] += det_jaccob/24

			B[I] += 1 # a faire

		U = np.ones((self.nb_point,1))
		test = A.dot(U)
		print sum(test)

		# print A

		return A,B