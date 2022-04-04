import pygame 
import random
import datetime
from shapes import *
from GameObjects import *
from functools import reduce

class GameFunctions():

	def __init__(self, windows_weight, windows_height, interfase_color=[0,0,0]):
		self.windows_weight = windows_weight
		self.windows_height = windows_height
		self.interfase_color = interfase_color
		self.tetris_block_x = 10
		self.tetris_block_y = 20
		self.play_area_weight = windows_weight - windows_weight//7
		self.play_area_height = windows_height - windows_height//12
		self.size_block_x = self.play_area_weight//(self.tetris_block_x+4) 
		self.size_block_y = self.play_area_height//(self.tetris_block_y+4)
		self.grid_cords = ( self.size_block_x * 2, self.size_block_y *2)
		self.gap = 70
		
	def __str__(self):
		print ('Class wich contain some game functions')

	def create_grid(self, locked_positions={}):
		grid = [[locked_positions[(x,y)] if (x,y) in locked_positions else (255,255,255) for y in range(10) ] for x in range(20)]
		return grid

	def draw_grid(self,background, grid, grid_on): # ADD TO OPTIONS ON/OFF GRID !!!

		if grid_on:
			for i in range(len(grid)):
				for j in range(len(grid[i])):
					pygame.draw.rect(background, grid[i][j], (self.grid_cords[0] + j*self.size_block_x,
						self.grid_cords[1] + i*self.size_block_y, self.size_block_x, self.size_block_y), 0)
					pygame.draw.rect(background, (0,0,0), (self.grid_cords[0] + j*self.size_block_x,
						self.grid_cords[1] + i*self.size_block_y, self.size_block_x, self.size_block_y), 1)	
			pygame.draw.rect(background, (0,0,0), (self.grid_cords[0] ,self.grid_cords[1],
					self.size_block_x*(j+1), self.size_block_y*(i+1)), 2)
		else:
			for i in range(len(grid)):
				for j in range(len(grid[i])):
					pygame.draw.rect(background, grid[i][j], (self.grid_cords[0] + j*self.size_block_x,
						self.grid_cords[1] + i*self.size_block_y, self.size_block_x, self.size_block_y), 0)
			pygame.draw.rect(background, (0,0,0), (self.grid_cords[0] ,self.grid_cords[1],
					self.size_block_x*(j+1), self.size_block_y*(i+1)), 2)

	def get_shape(self):
		shape = random.choice(shapes)
		forma = random.choice(shape)
		rotation_id = shape.index(forma)
		positions = []
		x = 0
		y = 5

		for i, line in enumerate(forma[0]):
			row = list(line)
			for j, column in enumerate(row):
				if column == '0':
					positions.append((x + i, y + j))
		for i, pos in enumerate(positions):
			positions[i] = (pos[0] - 4, pos[1] - 2)
		
		return GameObjects(positions, shape_colors[shapes.index(shape)], shape, rotation_id)

	def valid_space(self, shape, grid):
		accepted_positions = [[(x, y) for y in range(10) if grid[x][y] == (255,255,255)] for x in range(20)]
		accepted_positions = reduce(lambda x,y: x+y ,accepted_positions)
		for pos in shape:
			if pos not in accepted_positions:
				if pos[0] > -1:
					return True
				if pos[1] < 0 or pos[1] > 9:
					return True

		return False
			
	def clear_rows(self, grid, locked_positions, score, point, music):
		inc = 0
		for i in range(len(grid)-1,-1,-1):
			if (255,255,255) not in grid[i]:
				music.play()
				for j in range(len(grid[i])):
					try:
						del locked_positions[(i,j)]
					except:
						continue
				inc += 1
				l = i - 1
				while len([ 1 for x in grid[l] if x == (255,255,255) ]) < 10 and len([ 1 for x in grid[l] if x == (255,255,255) ]) > 0:
					for j in range(len(grid[l])):
						if grid[l][j] != (255,255,255):
							locked_positions[(l+inc,j)] = grid[l][j]
							grid[l][j] = (255,255,255)
							try:
								del locked_positions[(l,j)]
							except:
								continue
					#grid[l] = [(255,255,255) for _ in range(10)]
					if l > -1:
						l -= 1
					else:
						break
				
				score += point
		return score

	def draw_score(self, screen, background, score, first_input):
		if score > 1000:
			score = str(score//1000)+'k'
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(self.windows_height/600)))
		text = font.render("Score:{}".format(score), 0, (10, 10, 10))
		textpos = text.get_rect()
		background.fill((255,255,255), pygame.Rect(self.play_area_weight-self.gap,
											 self.play_area_height//3,
											 textpos[2]+80,
											 textpos[3]))

		background.blit(text, (self.play_area_weight-self.gap, self.play_area_height//3))

	def draw_next_figure(self, screen, background, shape):
		sx = 7
		sy = 16
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(self.windows_height/600)))
		text = font.render("Next:", 0, (10, 10, 10))
		textpos = text.get_rect()
		background.blit(text, (self.play_area_weight-self.gap,
							 self.play_area_height- ((self.windows_weight//2)+textpos[3])))

		background.fill((255,255,255), pygame.Rect((self.grid_cords[0] + self.tetris_block_x*self.size_block_x)+1,
											self.play_area_height- self.windows_weight//2,
													(self.windows_weight//7)*2,
													(self.windows_height//12)*4))

		for cord in shape.cords:
			x,y = cord
			pygame.draw.rect(background, shape.color, (self.grid_cords[0] + ((sx+y)*self.size_block_x),
					self.grid_cords[1] + (sy+x)*self.size_block_y, self.size_block_x, self.size_block_y))

	def check_lost(self, positions, number_figures=None, figure_limit=None):
		for cord in positions.keys():
			if cord[0] < 1:
				return True
		if number_figures:
			if number_figures >= figure_limit:
				return True
		return False

	def add_to_scoreboard(self, score):
		with open('scoreboard.txt','a') as file:
			file.write(str(datetime.datetime.now()).split()[0]+' '+str(score)+';\n')

	def draw_scoreboard(self, background):
		with open('scoreboard.txt') as file:
			data = file.readlines()
		
		res = sorted([ (x.split()[0],x.split()[-1][:-1]) for x in data ], key=lambda x : int(x[1]), reverse=True)
		shift = 0
		font = pygame.font.Font(None, int(35*(self.windows_weight/600)))
		center = background.get_rect()
		center = center.center
		for ind, x in enumerate(res[:5]):
			text = font.render(str(ind+1)+'. '+x[0]+' '+x[1] , 0, (10, 10, 10))
			if ind == 0:
				textpos = text.get_rect()
			background.blit(text, (center[0]-textpos[2]//2,
								((center[1]-textpos[3]//2)+self.windows_height//5)+shift))
			shift += textpos[3]

	def clear_scoreboard(self):
		with open('scoreboard.txt', "r") as file:
			data = file.readlines()
		if len(data) > 20:
			res = sorted([ (x.split()[0],x.split()[-1][:-1]) for x in data ], key=lambda x : int(x[1]), reverse=True)[:10]
			with open("scoreboard.txt", "w") as file:
				for line in res:
					file.write(line[0]+' '+line[1]+';\n')

	# Functions from drawing genetic parameters stuff
			
	def draw_member(self, screen, background, member, population):
		if population > 1000:
			population = str(population//1000)+'k'
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(self.windows_height/600)))
		text_1 = font.render("Member", 0, (10, 10, 10))
		text_2 = font.render("{}/{}".format(member,population), 0, (10, 10, 10))
		textpos_1 = text_1.get_rect()
		textpos_2 = text_2.get_rect()
		background.blit(text_1, (self.grid_cords[0]+self.size_block_x//4, self.size_block_x*16.3))
		background.fill((255,255,255), (self.grid_cords[0]+self.size_block_x//4, self.size_block_x*16.3+textpos_1[3], textpos_2[2]*2, textpos_2[3]))
		background.blit(text_2, (self.grid_cords[0]+self.size_block_x//4, self.size_block_x*16.3+textpos_1[3]))

	def draw_number_game(self, screen, background, number, games):
		if games > 1000:
			games = str(games//1000)+'k'
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(self.windows_height/600)))
		text_1 = font.render("Game", 0, (10, 10, 10))
		text_2 = font.render("{}/{}".format(number,games), 0, (10, 10, 10))
		textpos_1 = text_1.get_rect()
		textpos_2 = text_2.get_rect()
		background.blit(text_1, (self.grid_cords[0]+self.size_block_x*7+self.size_block_x//4, self.size_block_x*16.3))
		background.fill((255,255,255), (self.grid_cords[0]+self.size_block_x*7+self.size_block_x//4, self.size_block_x*16.3+textpos_1[3], textpos_2[2]*2, textpos_2[3]))
		background.blit(text_2, (self.grid_cords[0]+self.size_block_x*7+self.size_block_x//4, self.size_block_x*16.3+textpos_1[3]))

	def draw_max_figure(self, screen, background, n_figure, max_figure):
		if max_figure > 1000:
			max_figure = str(max_figure//1000)+'k'
		if n_figure > 1000:
			n_figure = str(n_figure//1000)+'k'
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(self.windows_height/600)))
		text_1 = font.render("Figure:", 0, (10, 10, 10))
		text_2 = font.render("{}/{}".format(n_figure,max_figure), 0, (10, 10, 10))
		textpos_1 = text_1.get_rect()
		textpos_2 = text_2.get_rect()
		background.blit(text_1, (self.play_area_weight-self.gap, self.play_area_height//6))
		background.fill((255,255,255), (self.play_area_weight-self.gap, self.play_area_height//6+textpos_1[3], textpos_2[2]*2, textpos_2[3]))
		background.blit(text_2, (self.play_area_weight-self.gap, self.play_area_height//6+textpos_1[3]))

	def draw_generations(self, screen, background, n_gener, generations):
		if n_gener > 1000:
			n_gener = str(n_gener//1000)+'k'
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(self.windows_height/600)))
		text_1 = font.render("Generation:", 0, (10, 10, 10))
		text_2 = font.render("{}/{}".format(n_gener,generations), 0, (10, 10, 10))
		textpos_1 = text_1.get_rect()
		textpos_2 = text_2.get_rect()
		background.blit(text_1, (self.grid_cords[0]+self.size_block_x//4, self.size_block_x//2))
		background.fill((255,255,255), (self.grid_cords[0]+self.size_block_x//4+textpos_1[2], self.size_block_x//2, textpos_2[2]*2, textpos_2[3]))
		background.blit(text_2, (self.grid_cords[0]+self.size_block_x//4+textpos_1[2]+self.size_block_x//4, self.size_block_x//2))

	

	