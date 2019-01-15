# -*- coding: utf-8 -*


from read_msh import read_msh
import numpy as np

def loc2glob(triangle, sommet):
	if sommet <= 0 and sommet > 3:
		raise Exception("Veuillez fournir un sommet compris entre 1 et 3")

	if list_element[triangle].type == 1 and sommet >= 3:
		raise Exception("Veuillez fournir un sommet locale inférieur ou égal à 2 pour un segment!")

	return list_element[triangle].list_index[sommet - 1]



def assemblage(mesh_file):
	nb_point,list_point,nb_element,list_element = read_msh(mesh_file)

	A = np.zeros(nb_point,nb_point)
	B = np.zeros(nb_point)

	M_ref = 1/24 * np.matrix([[2,1,1], # matrice élémentaire de référence
							  [1,2,1],
							  [1,1,2]])

	for p in range(nb_element):
		p1 = list_point[loc2glob(list_element[p],0)]
		p2 = list_point[loc2glob(list_element[p],1)]
		p3 = list_point[loc2glob(list_element[p],2)]

		det_jaccob = (p2[0] - p1[0])*(p3[1] - p1[1]) - (p3[0] - p1[0])*(p2[1] - p1[1])
		mat_elem = det_jaccob * M_ref
		for i in range(3): # Pour etre cohérant avec l'algo
			I = loc2glob(list_element[p],i)
			for j in range(3):
				J = loc2glob(list_element[p],j)

				A[I,J] += mat_elem # a faire

		B[I] += 1 # a faire

	return A,B