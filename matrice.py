# -*- coding: utf-8 -*


from read_msh import read_msh
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix, linalg

# k = 10#2 * np.pi # nombre d'onde

class Solveur:
	def __init__(self,mesh_file,k,alpha,PhysicalDir,PhysicalRob):
		if mesh_file == None:
			raise ValueError("Veuillez fournir un fichier .msh à notre solveur")
		self.nb_point,self.list_point,self.nb_element,self.list_element,self.nb_noTriangle = read_msh(mesh_file)

		self.k = k
		self.alpha =alpha 
		self.PhysicalDir = PhysicalDir
		self.PhysicalRob = PhysicalRob

		print("")
		print("k=",k," alpha=",alpha," Physical Dirichlet=",PhysicalDir," Physical Robin-Fourier=",PhysicalRob,"\n\n")
		# Le nb.noTriangle est ici pour sauter les premières éléments qui sont des arêtes

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
						# data.append(np.complex(0,1)*k*k*det_jaccob/12.0)
					else:
						data.append(det_jaccob/24.0)
						# data.append(np.complex(0,1)*k*k*det_jaccob/24.0)
					ind_ligne.append(I)
					ind_col.append(J)

		self.M = coo_matrix((np.array(data)*self.k*self.k, (ind_ligne,ind_col))).tocsr()

		# print("\n\n\n",self.M)
		# np.savetxt("Data/M.csv",self.M.todense(),fmt='%.12f',delimiter=',')

		# Vérification
		print("################### Vérification pour la matrice de masse ##################")
		U = np.ones((self.nb_point,1))
		test = self.M.dot(U)
		print(sum(test))
		print("Shape:",self.M.shape, "\n\n")

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
			
			B_temp = np.matmul(np.transpose(B_rigidite),B_rigidite)

			for i in range(3):
				I = self.loc2glob(p,i) - 1
				for j in range(3):
					J = self.loc2glob(p,j) - 1

					ind_ligne.append(I)
					ind_col.append(J)

					d_temp = grad_phi[j].dot(B_temp)
					
					# D[I,J] += det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i]))
					# print det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i]))
					data.append((-det_jaccob/2.0 * d_temp.dot(np.transpose(grad_phi[i])))[0][0]) # [0][0] car dot donne une liste de liste avec seulement une valeur
					
		self.D = coo_matrix((data, (ind_ligne,ind_col))).tocsr()
	
		# np.savetxt("Data/D.csv",self.D.todense(),fmt='%.12f',delimiter=',')

		# Vérification
		print("################## Vérification pour la matrice de rigidité ##################")
		print("Shape:",self.D.shape)
		U = np.ones((self.nb_point,1))
		print(sum(self.D.dot(U)))
		print("\n\n")

	def matriceRobin(self):
		"""
		Matrice pour la condition au bord de type Robin-Fourier.
		"""

		data = []
		ind_ligne = []
		ind_col = []
		for p in range(self.nb_noTriangle+1):
			# print("Robin")
			if self.list_element[p-1].physical == self.PhysicalRob: # bord de l'ellipse
				p1 = self.list_point[self.loc2glob(p,0)-1] # -1 car on commence à 0
				p2 = self.list_point[self.loc2glob(p,1)-1]

				#sigma =[p1,p2]
				sigma = np.linalg.norm((p1[0]-p2[0],p1[1]-p2[1]))
				for i in range(2):
					I = self.loc2glob(p,i) - 1
					for j in range(2):
						J = self.loc2glob(p,j) - 1

						if I == J:
							data.append(sigma/3.0)
							# data.append(-np.complex(0,1)*sigma/3.0)
						else:
							data.append(sigma/6.0)
							# data.append(-np.complex(0,1)*sigma/6.0)
						ind_ligne.append(I)
						ind_col.append(J)

		self.Mbord = coo_matrix((np.array(data)*np.complex(0,-self.k), (ind_ligne,ind_col)),shape=(self.nb_point, self.nb_point),dtype=complex).tocsr()
		
		print("################## Matrice de bord ##################")
		# print("Mbord",self.Mbord.todense())
		print("Shape:",self.Mbord.shape)
		print("\n\n")


	def assemblage(self):
		# self.matriceMasse()
		# self.matriceRigidite()

		self.A = (self.M + self.D + self.Mbord).tolil() # pour faciliter la mise à 0 de la matrice
		self.B = np.zeros(self.nb_point,dtype=complex)

		for index, element in enumerate(self.list_element):
			if element.physical == self.PhysicalDir: # bord du sous-marin
				# print(index, " ", element)
				for point in element.list_index: # les points du bord
					#print(point," ",self.list_point[point])
					self.A[point-1,:] = 0
					# self.A[:, point-1] = 0
					self.A[point-1,point-1] = 1
					self.B[point-1] = -self.u_inc(self.list_point[point-1][0], self.list_point[point-1][1])

		self.A = self.A.tocsr()

		print("################## Assemblage ##################")
		
		# for i in self.B:
		# 	print(i)
		# print(self.B)
		self.U = linalg.spsolve(self.A, self.B)

		# np.savetxt("Data/U.csv",self.U,fmt='%.12f',delimiter=',')
		# np.savez("Data/A.data",self.A)
		#np.savetxt("points.csv",self.list_point,delimiter=",",header="X,Y,Z")
		
	def u_inc(self,x,y):
		alpha = self.alpha
		return np.exp(np.complex(0,1)*self.k*(x*np.cos(alpha) + y*np.sin(alpha)))

	# def save_sparse_matrix(filename, x):
	#     x_csr = x.tocsr()
	#     row = x_csr.row
	#     col = x_csr.col
	#     data = x_csr.data
	#     shape = x_csr.shape
	#     np.savez(filename, row=row, col=col, data=data, shape=shape)


	# def load_sparse_matrix(filename):
	#     y = np.load(filename)
	#     z = sparse.csr_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])
	# 	return z

