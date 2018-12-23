# -*- coding: utf-8 -*


class Element:
	def __init__(self, elem_type, tag, index):
		self.type = elem_type
		self.tag = tag
		self.list_index = []
		for i in index:
			self.list_index.append(int(i))

	def __str__(self):
		return "Type : " + str(self.type) + ", tag : " + str(self.tag) +", index : " + str(self.list_index)
