import pygame
import math
from shapes import *

class GameObjects():

	def __init__(self, cords, color, all_rotations, rotation_id):
		self.cords = cords
		self.color = color
		self.all_rotations = all_rotations
		self.rotation_id = rotation_id

	def __str__(self):
		return '{}'.format(self.cords)

	def next_rotation(self, placehold=True):
		new_id = (self.rotation_id+1) % len(self.all_rotations)
		rotation_shape = self.all_rotations[new_id]
		new_cords = list(map(lambda x,y: (x[0]+y[0], x[1]+y[1]), self.cords, rotation_shape[1]))

		if rotation_shape[2] == 'S_key_1':
			if placehold:
				self.cords = new_cords[:2][::-1] + new_cords[2:][::-1]
				self.rotation_id = new_id
			else:
				return new_cords[:2][::-1] + new_cords[2:][::-1]
		if rotation_shape[2] == 'S_key_2':
			if placehold:
				self.cords = new_cords[2:] + new_cords[:2]
				self.rotation_id = new_id
			else:
				return new_cords[2:] + new_cords[:2]


		if rotation_shape[2] == 'Z_key_1':
			if placehold:
				b = new_cords.pop(1)
				c = new_cords.pop()
				self.cords = [c] + ([b] + new_cords[::-1])
				self.rotation_id = new_id
			else:
				b = new_cords.pop(1)
				c = new_cords.pop()
				return [c] + ([b] + new_cords[::-1])
		if rotation_shape[2] == 'Z_key_2': 
			if placehold:
				b = new_cords.pop()
				c = new_cords.pop(0)
				a = [c] + new_cords[::-1]
				a.append(b)
				self.cords = a
				self.rotation_id = new_id
			else:
				b = new_cords.pop()
				c = new_cords.pop(0)
				a = [c] + new_cords[::-1]
				a.append(b)
				return a


		if rotation_shape[2] == 'I_key_1':
			if placehold:
				self.cords = new_cords
				self.rotation_id = new_id
			else:
				return new_cords
		if rotation_shape[2] == 'I_key_2':
			if placehold:
				self.cords = new_cords[::-1]
				self.rotation_id = new_id
			else:
				return new_cords[::-1]


		if rotation_shape[2] == 'O_key_1':
			if placehold:
				self.cords = new_cords
				self.rotation_id = new_id
			else:
				return new_cords


		if rotation_shape[2] == 'J_key_1':
			if placehold:
				self.cords = [new_cords.pop(2)] + new_cords[::-1]
				self.rotation_id = new_id
			else:
				return [new_cords.pop(2)] + new_cords[::-1]
		if rotation_shape[2] == 'J_key_2':
			if placehold:
				self.cords = [new_cords.pop(1)] + new_cords
				self.rotation_id = new_id
			else:
				return [new_cords.pop(1)] + new_cords
		if rotation_shape[2] == 'J_key_3':
			if placehold:
				b = new_cords.pop(1)
				a = new_cords[::-1]
				a.append(b)
				self.cords = a
				self.rotation_id = new_id
			else:
				b = new_cords.pop(1)
				a = new_cords[::-1]
				a.append(b)
				return a
		if rotation_shape[2] == 'J_key_4':
			if placehold:
				b = new_cords.pop(2)
				new_cords.append(b)
				self.cords = new_cords
				self.rotation_id = new_id
			else:
				b = new_cords.pop(2)
				new_cords.append(b)
				return new_cords

		if rotation_shape[2] == 'L_key_1': 
			if placehold:
				b = new_cords[::-1].pop()
				self.cords = [b] + new_cords[::-1]
				self.rotation_id = new_id
			else:
				b = new_cords[::-1].pop()
				return [b] + new_cords[::-1]
		if rotation_shape[2] == 'L_key_2': 
			if placehold:
				b = new_cords.pop(0)
				new_cords.append(b)
				self.cords = new_cords
				self.rotation_id = new_id
			else:
				b = new_cords.pop(0)
				new_cords.append(b) 
				return new_cords
		if rotation_shape[2] == 'L_key_3': 
			if placehold:
				b = new_cords.pop()
				new_cords = new_cords[::-1]
				new_cords.append(b)
				self.cords = new_cords
				self.rotation_id = new_id
			else:
				b = new_cords.pop()
				new_cords = new_cords[::-1]
				new_cords.append(b)
				return new_cords
		if rotation_shape[2] == 'L_key_4': 
			if placehold:
				b = new_cords.pop()
				self.cords = [b] + new_cords
				self.rotation_id = new_id
			else:
				b = new_cords.pop()
				return [b] + new_cords

		if rotation_shape[2] == 'T_key_1': 
			if placehold:
				b = new_cords.pop(1)
				self.cords = [b] + new_cords[::-1]
				self.rotation_id = new_id
			else:
				b = new_cords.pop(1)
				return [b] + new_cords[::-1]
		if rotation_shape[2] == 'T_key_2': 
			if placehold:
				b = new_cords.pop(0)
				c = new_cords.pop()
				new_cords.append(b)
				new_cords.append(c)
				self.cords = new_cords
				self.rotation_id = new_id
			else:
				b = new_cords.pop(0)
				c = new_cords.pop()
				new_cords.append(b)
				new_cords.append(c)
				return new_cords
		if rotation_shape[2] == 'T_key_3': 
			if placehold:
				b = new_cords.pop(2)
				a = new_cords[::-1]
				a.append(b)
				self.cords = a
				self.rotation_id = new_id
			else:
				b = new_cords.pop(2)
				a = new_cords[::-1]
				a.append(b)
				return a
		if rotation_shape[2] == 'T_key_4': 
			if placehold:
				b = new_cords.pop(0)
				c = new_cords.pop(1)
				a = [b] + new_cords[::-1]
				a.append(c)
				self.cords = a
				self.rotation_id = new_id
			else:
				b = new_cords.pop(0)
				c = new_cords.pop(1)
				a = [b] + new_cords[::-1]
				a.append(c)
				return a
