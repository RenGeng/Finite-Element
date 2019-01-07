# -*- coding: utf-8 -*


class Element:
	def __init__(self, elem_type, physical, index):
		self.type = elem_type
		self.physical = physical # Bord ou domaine
		self.list_index = []
		for i in index:
			self.list_index.append(int(i))

	def __str__(self):
		return "Type : " + str(self.type) + ", tag : " + str(self.physical) +", index : " + str(self.list_index)
