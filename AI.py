import pygame
import math
import random

class AI():

	def __init__(self, weights):
		self.weight_params = weights

	def calculate_best_move(self, grid, positions, shape, game_functions):
		best_chioce = []
		tmp_positions = positions.copy()
		rotation_id = shape.rotation_id

		while True:
			shifted_shape = shape.cords
			flag = True
			
			# Take leftmost positions
			while flag:
				for cords in shifted_shape:
					if cords[1] < 0:
						shifted_shape = [(cords[0], cords[1]) for cords in shifted_shape]
						flag = False
						break
				else:
					shifted_shape = [(cords[0], cords[1]-1) for cords in shifted_shape]		
			flag = True	

			# Make iterations from left-1 side to right 
			while True:
				shifted_shape = [(cords[0], cords[1]+1) for cords in shifted_shape]
				if sum([1 if cords[1] > 9 else 0 for cords in shifted_shape]) != 0:
					break
				work_shape = shifted_shape.copy()
				# Lower the figure down
				f = True
				while f:
					for cords in work_shape:
						if cords in positions or cords[0] == 20:
							work_shape = [(cords[0]-1, cords[1]) for cords in work_shape]
							for cords in work_shape:
								tmp_positions[cords] = shape.color
							f = False
							break
					else:
						work_shape = [(cords[0]+1, cords[1]) for cords in work_shape]
					if not f:
						best_chioce.append(self.calculate_weighting_coefficient(tmp_positions, shifted_shape))
						tmp_positions = positions.copy()
			shape.next_rotation()
			if shape.rotation_id == rotation_id:
				break

		# Selelc best move
		best_score = max(best_chioce, key = lambda x: x[1])
		all_best_score_positions = [(pos,score,up_pos) for pos, score, up_pos in best_chioce if score == best_score[1]]
		#print(best_chioce)
		#print(all_best_score_positions)
		#print (random.choice(all_best_score_positions)[2])
		return random.choice(all_best_score_positions)[2]


	# Metrics from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
	def calculate_weighting_coefficient(self,positions, shifted_shape):
		pseudo_grid = [ [ 1 if (x, y) in positions else 0 for y in range(10) ] for x in range(20)]

		# Aggregate Height
		aggregate_height = {}
		for i in range(10):
			for j in range(20):
				if pseudo_grid[j][i] == 1:
					aggregate_height[i] = 20 - j
					break
				if j == 19:
					aggregate_height[i] = 0
		aggregate_height_value = sum(aggregate_height.values())

		# Complete Lines
		separating_value = 0
		complete_lines = 0
		for i in range(len(pseudo_grid)-1,-1,-1):
			if 0 not in pseudo_grid[i]:
				complete_lines += 1
			if 1 not in pseudo_grid[i]:
				separating_value = i
				break		

		# Holes
		holes = 0
		for i in range(10):
			for j in range(19,separating_value,-1):
				if pseudo_grid[j][i] == 0 and j-1 > separating_value and pseudo_grid[j-1][i] == 1:
					holes += 1

		#Bumpiness
		values = list(aggregate_height.values())
		test = []
		bumpiness = 0
		for i in range(len(values)-1):
			test.append((values[i], values[i+1]))
			bumpiness += abs(values[i] - values[i+1])

		#Height difference
		max_height = min(positions, key=lambda x: x[0])
		min_height = max(positions, key=lambda x: x[0])
		height_difference = abs(max_height[0] - min_height[0])

		#Putting the heuristic together
		a,b,c,d,e = self.weight_params
		score = a*aggregate_height_value + b*complete_lines + c*holes + d*bumpiness + e*height_difference # highest score better
		return (positions, score, shifted_shape)


					





