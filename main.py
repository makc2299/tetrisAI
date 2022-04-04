# Tetris game made using the tutorial on the official website pygame
# 
# sourse: https://www.pygame.org/docs/tut/MakeGames.html


#try:
import sys
import random
import math
import os
# import getopt
import pygame
import time
#import pkg_resources.py2_warn
from socket import *
from pygame.locals import *
#from ResourceHandling import *
from Button import *
from Button_circle import *
from InputField import *
from GameFunctions import *
from GeneticAlgoritm import *
from AI import *
# except ImportError, err):
# 	print ("couldn't load module. %s" % (err))
# 	sys.exit(2)

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

LIST_WINDOWS_SIZE = ([600,700],[700,800],[800,900])
INDX_WINDOWS_SIZE = 0

def infinity_loop(LIST_WINDOWS_SIZE, INDX_WINDOWS_SIZE):
	#global INDX_WINDOWS_SIZE
	#INDX = INDX_WINDOWS_SIZE
	WINDOWS_SIZE = LIST_WINDOWS_SIZE[INDX_WINDOWS_SIZE]
	button_weight = (1/3) * WINDOWS_SIZE[0] # 200
	button_height = (1/15) * WINDOWS_SIZE[1] # 50

	def main():
		# Initialise screen
		pygame.init()
		screen = pygame.display.set_mode(WINDOWS_SIZE)
		pygame.display.set_caption('Tetris AI')

		# Fill background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((255, 255, 255))

		# Display menu
		font = pygame.font.Font(None, int(100*(WINDOWS_SIZE[0]/600)))
		text = font.render("Tetris AI", 1, (0, 254, 255))
		textpos = text.get_rect()
		background.blit(text, (WINDOWS_SIZE[0]//2- textpos[2]//2,WINDOWS_SIZE[1]//7 - textpos[3]//2))

		button_1 = Button(color=(0,250,0), x = WINDOWS_SIZE[0]//2-button_weight//2,
			y = (WINDOWS_SIZE[1]//7)*2.3 - button_height//2,width=button_weight,height=button_height, text='Play', entire_window=WINDOWS_SIZE[0])
		button_2 = Button(color=(0,250,0), x = WINDOWS_SIZE[0]//2-button_weight//2,
			y = (WINDOWS_SIZE[1]//7)*3.1 - button_height//2,width=button_weight,height=button_height, text='Play AI', entire_window=WINDOWS_SIZE[0])
		button_3 = Button(color=(0,250,0), x = WINDOWS_SIZE[0]//2-button_weight//2,
			y = (WINDOWS_SIZE[1]//7)*3.9 - button_height//2,width=button_weight,height=button_height, text='Train AI', entire_window=WINDOWS_SIZE[0])
		button_4 = Button(color=(0,250,0), x = WINDOWS_SIZE[0]//2-button_weight//2,
			y = (WINDOWS_SIZE[1]//7)*4.7 - button_height//2,width=button_weight,height=button_height, text='Options', entire_window=WINDOWS_SIZE[0])
		button_5 = Button(color=(0,250,0), x = WINDOWS_SIZE[0]//2-button_weight//2,
			y = (WINDOWS_SIZE[1]//7)*5.5 - button_height//2,width=button_weight,height=button_height, text='About', entire_window=WINDOWS_SIZE[0])
		button_6 = Button(color=(0,250,0), x = WINDOWS_SIZE[0]//2-button_weight//2,
			y = (WINDOWS_SIZE[1]//7)*6.3 - button_height//2,width=button_weight,height=button_height, text='Exit', entire_window=WINDOWS_SIZE[0])
		

		# Blit everything to the screen
		screen.blit(background, (0, 0))
		pygame.display.flip()

		# Sound button click
		global menu_sound, sound_click
		sound_click = pygame.mixer.Sound('data/audio/button_click.wav')
		sound_overlay = pygame.mixer.Sound('data/audio/button_overlay.wav')
		menu_sound = pygame.mixer.Sound('data/audio/menu_sound.wav')
		menu_sound.play(-1)

		# Save state from button in options
		global button_click_state
		button_click_state = [True, True, True, True, True, True, False]

		# Event loop
		while True:
			background.blit(text, (WINDOWS_SIZE[0]//2- textpos[2]//2,WINDOWS_SIZE[1]//7 - textpos[3]//2))
			button_1.draw(background, (1,1,1))
			button_2.draw(background, (1,1,1))
			button_3.draw(background, (1,1,1))
			button_4.draw(background, (1,1,1))
			button_5.draw(background, (1,1,1))
			button_6.draw(background, (1,1,1))
			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if button_1.isOver(mouse_pos):
						sound_click.play()
						game(background, screen)
						background.fill((255, 255, 255)) # add blid from erase previous content
					if button_2.isOver(mouse_pos):
						sound_click.play()
						#play_ai(background, screen, button_click_state[2:])
						menu_play_ai(background,screen,button_click_state[2:])
						background.fill((255, 255, 255))
					if button_3.isOver(mouse_pos):
						sound_click.play()
						menu_train_ai(background,screen)
						background.fill((255, 255, 255))
					if button_4.isOver(mouse_pos):
						sound_click.play()
						try:							
							IWS, FLAG = options(background,screen, button_click_state)
							background.fill((255, 255, 255)) 
							if FLAG:
								return (IWS, FLAG)		 
						except:
							background.fill((255, 255, 255)) 
					if button_5.isOver(mouse_pos):
						sound_click.play()	     
						about(background,screen)   	     
						background.fill((255, 255, 255)) 
					if button_6.isOver(mouse_pos):
						pygame.quit()
						sys.exit()
				if event.type == pygame.MOUSEMOTION:
					if button_1.isOver(mouse_pos):
						button_1.color = (250,0,0)
					else:
						button_1.color = (0,250,0)

					if button_2.isOver(mouse_pos):
						button_2.color = (250,0,0)
					else:
						button_2.color = (0,250,0)

					if button_3.isOver(mouse_pos):
						button_3.color = (250,0,0)
					else:
						button_3.color = (0,250,0)

					if button_4.isOver(mouse_pos):
						button_4.color = (250,0,0)
					else:
						button_4.color = (0,250,0)

					if button_5.isOver(mouse_pos):
						button_5.color = (250,0,0)
					else:
						button_5.color = (0,250,0)

					if button_6.isOver(mouse_pos):
						button_6.color = (250,0,0)
					else:
						button_6.color = (0,250,0)
			screen.blit(background, (0, 0))
			pygame.display.flip()

	def game(background,screen):
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))
		menu_sound.stop()

		game_functions = GameFunctions(WINDOWS_SIZE[0],WINDOWS_SIZE[1])
		grid = game_functions.create_grid()
		current_shape = game_functions.get_shape()
		next_shape = game_functions.get_shape()
		running = True
		change_piece = False
		locked_positions = {}
		clock = pygame.time.Clock()
		current_speed = 0.27
		rate_speed_progression = 0
		fall_time = 0
		score = 0 
		tmp_score = 0
		point = 10
		game_functions.draw_score(screen, background, score, True)
		game_functions.draw_next_figure(screen, background, next_shape)
		pause = False
		crutch = True
		clear_row_sound = pygame.mixer.Sound('data/audio/clear_row.wav')

		while running:
			game_functions.draw_grid(background, grid, not button_click_state[1])
			grid = game_functions.create_grid(locked_positions)
			fall_time += clock.get_rawtime()
			clock.tick()

			# FALLING CODE
			if fall_time/1000 >= current_speed and not pause:
				fall_time = 0
				current_shape.cords = [ (x[0]+1, x[1]) for x in current_shape.cords]
				if game_functions.valid_space(current_shape.cords, grid) and not sum([ 1 if i[0] < 0 else 0 for i in current_shape.cords]) > 0:
					current_shape.cords = [ (x[0]-1, x[1]) for x in current_shape.cords]
					change_piece = True

			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
						if button_click_state[0]:
							menu_sound.play(-1)
					if event.key == pygame.K_LEFT and not pause:
						current_shape.cords = [ (x[0], x[1]-1) for x in current_shape.cords]
						if game_functions.valid_space(current_shape.cords, grid):
							current_shape.cords = [ (x[0], x[1]+1) for x in current_shape.cords]
					if event.key == pygame.K_RIGHT and not pause:
						current_shape.cords = [ (x[0], x[1]+1) for x in current_shape.cords]
						if game_functions.valid_space(current_shape.cords, grid):
							current_shape.cords = [ (x[0], x[1]-1) for x in current_shape.cords]
					# if event.key == pygame.K_DOWN and not pause:
					# 	current_shape.cords = [ (x[0]+1, x[1]) for x in current_shape.cords]
					# 	if game_functions.valid_space(current_shape.cords, grid):
					# 		current_shape.cords = [ (x[0]-1, x[1]) for x in current_shape.cords]
					if event.key == pygame.K_DOWN and not pause:
						current_speed = 0.05
					if event.key == pygame.K_UP and not pause:
						if not game_functions.valid_space(current_shape.next_rotation(False), grid):
							current_shape.next_rotation()
					if event.key == pygame.K_SPACE:
						pause = not pause


				if event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN and not pause:
						current_speed = 0.27 - (rate_speed_progression*0.02)


			# MOVE SHAPE
			for cord in current_shape.cords:
				x, y = cord
				if x > -1:
					grid[x][y] = current_shape.color

			if change_piece:
				for pos in current_shape.cords:
					locked_positions[pos] = current_shape.color
				current_shape = next_shape
				next_shape = game_functions.get_shape()
				change_piece = False

				# clear rows
				score = game_functions.clear_rows(grid, locked_positions, score, point, clear_row_sound)
				game_functions.draw_score(screen, background, score, False)
				game_functions.draw_next_figure(screen, background, next_shape)

				# difficulty progression
				if score != 0 and score % 100 == 0 and score != tmp_score:
					rate_speed_progression += 1
					point += 5
					tmp_score = score

			# screen.blit(background, (0, 0))
			# pygame.display.flip()

			# CHECK LOST
			if game_functions.check_lost(locked_positions):
				background.fill((255,255,255))	
				font = pygame.font.Font(None, int(40*(WINDOWS_SIZE[0]/600)))
				text = font.render("You Lost", 0, (10, 10, 10))
				textpos = text.get_rect()
				center = background.get_rect()
				center = center.center
				background.blit(text, (center[0]-textpos[2]//2, (center[1]-textpos[3]//2)-WINDOWS_SIZE[1]//8))
				text = font.render("Score: {}".format(score), 0, (10, 10, 10))
				textpos = text.get_rect()
				background.blit(text, (center[0]-textpos[2]//2, (center[1]-textpos[3]//2)+WINDOWS_SIZE[1]//14))

				if crutch:
					game_functions.add_to_scoreboard(score)
					crutch = False
				game_functions.draw_scoreboard(background)

				pause = True
				screen.blit(background, (0, 0))
				pygame.display.flip()

			
			screen.blit(background, (0, 0))
			pygame.display.flip()
		game_functions.clear_scoreboard()

	def about(background,screen):
		# game rules and other
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))

		texts = ["Simple tetris game made by:", 
					"https://github.com/makc2299",
					"Used stuff:",
					"https://www.youtube.com/watch?v=zfvxp7PgQ6c",
					"- YouTube guide from freeCodeCamp.org",
					"https://www.pygame.org/docs/tut/MakeGames.html",
					"- Pygame ducumentations",
					"https://freesound.org/people/joshuaempyre/",
					"- man who made menu music"]
		pygame.draw.rect(background, (0,0,0), (WINDOWS_SIZE[0]//10, WINDOWS_SIZE[1]//14,
													WINDOWS_SIZE[0] - WINDOWS_SIZE[0]//5,
													WINDOWS_SIZE[1] - WINDOWS_SIZE[1]//7), 2)
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(20*(WINDOWS_SIZE[0]/600)))
		shift = 0
		for ind, text in enumerate(texts):
			text = font.render(text, 0, (10, 10, 10))
			if ind == 0:
				textpos = text.get_rect()
			if ind == 2 or ind == 5 or ind == 7:
				shift += textpos[3]	
			background.blit(text, ((WINDOWS_SIZE[0]//8)+5, ((WINDOWS_SIZE[1]//12)+5)+shift))
			shift += textpos[3]

		running = True
		while running:
			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False

			screen.blit(background, (0, 0))
			pygame.display.flip()

	def options(background,screen, button_click_state):
		global INDX_WINDOWS_SIZE
		# game options
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))

		# BOX
		border_weight = WINDOWS_SIZE[0] - WINDOWS_SIZE[0]//5
		border_height = WINDOWS_SIZE[1] - WINDOWS_SIZE[1]//7
		pygame.draw.rect(background, (0,0,0), (WINDOWS_SIZE[0]//10, WINDOWS_SIZE[1]//14,
													border_weight,
													border_height), 2)
		# MIDDLE LINE 
		pygame.draw.line(background, (0,0,0), (WINDOWS_SIZE[0]//10, (WINDOWS_SIZE[1]//2)-(WINDOWS_SIZE[1]//28)),
						 ((WINDOWS_SIZE[0]//10)*9, (WINDOWS_SIZE[1]//2)-(WINDOWS_SIZE[1]//28)), 2)

		# ADD LABEL AND RECTANGLE AROUND HERE FROM GAME OPTIONS AND ITEMS
		font_label = pygame.font.Font('data/font/arial_narrow_7.ttf', int(25*(WINDOWS_SIZE[0]/600)))
		text = font_label.render('Game options', 0, (10, 10, 10))
		background.blit(text, ((WINDOWS_SIZE[0]//8)+5, (WINDOWS_SIZE[1]//12)+2))
		pygame.draw.rect(background, (0,0,0), (WINDOWS_SIZE[0]//10, WINDOWS_SIZE[1]//14,
													border_weight//1.6,
													border_height//17), 2)
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(WINDOWS_SIZE[0]/600)))
		texts = ["Mute music",
					"Add grid",
					"Change screensize"]

		shift = border_height//17
		shift_array = []
		for ind, text in enumerate(texts):
			text = font.render(text, 0, (10, 10, 10))
			if ind == 0:
				textpos = text.get_rect()
			background.blit(text, ((WINDOWS_SIZE[0]//8)+5, ((WINDOWS_SIZE[1]//12)+5)+shift))
			shift_array.append(((WINDOWS_SIZE[1]//12)+5)+shift)
			shift += textpos[3]*2.7

		if button_click_state[0]:
			color_1 = (0,250,0)
		else:
			color_1 = (250,0,0)

		if button_click_state[1]:
			color_2 = (0,250,0)
		else:
			color_2 = (250,0,0)

		# GAME BUTTONS
		button_1 = Button(color=color_1, x = (border_weight//2) + border_weight//3,
			y = shift_array[0],width=button_height-10,height=button_height-10, text='', entire_window=WINDOWS_SIZE[0])
		button_2 = Button(color=color_2, x = (border_weight//2) + border_weight//3,
			y = shift_array[1],width=button_height-10,height=button_height-10, text='', entire_window=WINDOWS_SIZE[0])
		button_3 = Button(color=(0,250,0), x = (border_weight//2) + border_weight//4,
			y = shift_array[2],width=button_height-10,height=button_height-10, text='<', entire_window=WINDOWS_SIZE[0])
		button_4 = Button(color=(0,250,0), x = (border_weight//2) + border_weight//2.4,
			y = shift_array[2],width=button_height-10,height=button_height-10, text='>', entire_window=WINDOWS_SIZE[0])

		# ADD LABEL AND RECTANGLE FROM AI OPTIONS AND ITEMS
		text = font_label.render('AI options off/on weights', 0, (10, 10, 10))
		background.blit(text, ((WINDOWS_SIZE[0]//8)+5, ((WINDOWS_SIZE[1]//2)-(WINDOWS_SIZE[1]//28)+8)))
		pygame.draw.rect(background, (0,0,0), (WINDOWS_SIZE[0]//10, (WINDOWS_SIZE[1]//2)-(WINDOWS_SIZE[1]//28),
													border_weight//1.6,
													border_height//17), 2)
		texts = ['Aggregate Height', 'Complete Lines', 'Holes', 'Bumpiness']

		shift = border_height//17
		shift_array = []
		for ind, text in enumerate(texts):
			text = font.render(text, 0, (10, 10, 10))
			if ind == 0:
				textpos = text.get_rect()
			background.blit(text, ((WINDOWS_SIZE[0]//8)+5, ((WINDOWS_SIZE[1]//2)+5)+shift))
			shift_array.append(((WINDOWS_SIZE[1]//2)+5)+shift)
			shift += textpos[3]*2.3

		if button_click_state[2]:
			color_3 = (0,250,0)
		else:
			color_3 = (250,0,0)

		if button_click_state[3]:
			color_4 = (0,250,0)
		else:
			color_4 = (250,0,0)

		if button_click_state[4]:
			color_5 = (0,250,0)
		else:
			color_5 = (250,0,0)

		if button_click_state[5]:
			color_6 = (0,250,0)
		else:
			color_6 = (250,0,0)		

		# WEIGHTS BUTTONS
		button_5 = Button(color=color_3, x = (border_weight//2) + border_weight//3,
			y = shift_array[0],width=button_height-10,height=button_height-10, text='', entire_window=WINDOWS_SIZE[0])
		button_6 = Button(color=color_4, x = (border_weight//2) + border_weight//3,
			y = shift_array[1],width=button_height-10,height=button_height-10, text='', entire_window=WINDOWS_SIZE[0])
		button_7 = Button(color=color_5, x = (border_weight//2) + border_weight//3,
			y = shift_array[2],width=button_height-10,height=button_height-10, text='', entire_window=WINDOWS_SIZE[0])
		button_8 = Button(color=color_6, x = (border_weight//2) + border_weight//3,
			y = shift_array[3],width=button_height-10,height=button_height-10, text='', entire_window=WINDOWS_SIZE[0])

		running = True
		while running:
			button_1.draw(background, (1,1,1))
			button_2.draw(background, (1,1,1))
			button_3.draw(background, (1,1,1))
			button_4.draw(background, (1,1,1))
			button_5.draw(background, (1,1,1))
			button_6.draw(background, (1,1,1))
			button_7.draw(background, (1,1,1))
			button_8.draw(background, (1,1,1))
			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if button_1.isOver(mouse_pos):
						sound_click.play()
						if button_click_state[0]:
							button_1.color = (250,0,0)
							menu_sound.stop()
						else:
							button_1.color = (0,250,0)
							menu_sound.play(-1)
						button_click_state[0] = not button_click_state[0]
					if button_2.isOver(mouse_pos):
						sound_click.play()							
						if button_click_state[1]:
							button_2.color = (250,0,0)
						else:
							button_2.color = (0,250,0)
						button_click_state[1] = not button_click_state[1]
					if button_3.isOver(mouse_pos):
						sound_click.play()	
						#os.execv(__file__, sys.argv)
						menu_sound.stop()
						INDX_WINDOWS_SIZE -= 1
						return (INDX_WINDOWS_SIZE % len(LIST_WINDOWS_SIZE), True)
					if button_4.isOver(mouse_pos):
						sound_click.play()
						menu_sound.stop()
						INDX_WINDOWS_SIZE += 1
						return (INDX_WINDOWS_SIZE % len(LIST_WINDOWS_SIZE), True)
					if button_5.isOver(mouse_pos):
						sound_click.play()
						if button_click_state[2]:
							button_5.color = (250,0,0)
							#menu_sound.stop()
						else:
							button_5.color = (0,250,0)
							#menu_sound.play(-1)
						button_click_state[2] = not button_click_state[2]
					if button_6.isOver(mouse_pos):
						sound_click.play()
						if button_click_state[3]:
							button_6.color = (250,0,0)
							#menu_sound.stop()
						else:
							button_6.color = (0,250,0)
							#menu_sound.play(-1)
						button_click_state[3] = not button_click_state[3]
					if button_7.isOver(mouse_pos):
						sound_click.play()
						if button_click_state[4]:
							button_7.color = (250,0,0)
							#menu_sound.stop()
						else:
							button_7.color = (0,250,0)
							#menu_sound.play(-1)
						button_click_state[4] = not button_click_state[4]
					if button_8.isOver(mouse_pos):
						sound_click.play()
						if button_click_state[5]:
							button_8.color = (250,0,0)
							#menu_sound.stop()
						else:
							button_8.color = (0,250,0)
							#menu_sound.play(-1)
						button_click_state[5] = not button_click_state[5]

				if event.type == pygame.MOUSEMOTION:
					if button_click_state[0]:
						if button_1.isOver(mouse_pos):
							button_1.color = (250,0,0)
						else:
							button_1.color = (0,250,0)

					if button_click_state[1]:
						if button_2.isOver(mouse_pos):
							button_2.color = (250,0,0)
						else:
							button_2.color = (0,250,0)

					if button_3.isOver(mouse_pos):
						button_3.color = (250,0,0)
					else:
						button_3.color = (0,250,0)

					if button_4.isOver(mouse_pos):
						button_4.color = (250,0,0)
					else:
						button_4.color = (0,250,0)

					if button_click_state[2]:
						if button_5.isOver(mouse_pos):
							button_5.color = (250,0,0)
						else:
							button_5.color = (0,250,0)

					if button_click_state[3]:
						if button_6.isOver(mouse_pos):
							button_6.color = (250,0,0)
						else:
							button_6.color = (0,250,0)

					if button_click_state[4]:
						if button_7.isOver(mouse_pos):
							button_7.color = (250,0,0)
						else:
							button_7.color = (0,250,0)

					if button_click_state[5]:
						if button_8.isOver(mouse_pos):
							button_8.color = (250,0,0)
						else:
							button_8.color = (0,250,0)

			screen.blit(background, (0, 0))
			pygame.display.flip()

	def play_ai(background,screen,weight_markers,trainer_weights=None):
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))
		menu_sound.stop()

		if trainer_weights:
			ai_player = AI( trainer_weights )
		else:
			WEIGHTS = [-0.510066, 0.760666, -0.35663, -0.184483, 0] 
			ai_player = AI( [WEIGHTS[i] if weight_markers[i] else 0 for i in range(len(WEIGHTS)) ] ) # wights 

		game_functions = GameFunctions(WINDOWS_SIZE[0],WINDOWS_SIZE[1])
		grid = game_functions.create_grid()
		current_shape = game_functions.get_shape()
		next_shape = game_functions.get_shape()
		running = True
		change_piece = False
		locked_positions = {}
		clock = pygame.time.Clock()
		current_speed = 0.02 # 0.07
		fall_time = 0
		score = 0 
		tmp_score = 0
		point = 10
		game_functions.draw_score(screen, background, score, True)
		game_functions.draw_next_figure(screen, background, next_shape)
		pause = False
		clear_row_sound = pygame.mixer.Sound('data/audio/clear_row.wav')
		current_shape.cords = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)

		while running:
			fall_speed = current_speed
			game_functions.draw_grid(background, grid, not button_click_state[1])
			grid = game_functions.create_grid(locked_positions)
			fall_time += clock.get_rawtime()
			clock.tick()

			# FALLING CODE
			if fall_time/1000 >= fall_speed and not pause:
				fall_time = 0
				current_shape.cords = [ (x[0]+1, x[1]) for x in current_shape.cords]
				if game_functions.valid_space(current_shape.cords, grid) and not sum([ 1 if i[0] < 0 else 0 for i in current_shape.cords]) > 0:
					current_shape.cords = [ (x[0]-1, x[1]) for x in current_shape.cords]
					#locked_positions = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)
					change_piece = True

			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
						if button_click_state[0]:
							menu_sound.play(-1)
					if event.key == pygame.K_SPACE:
						pause = not pause

			# MOVE SHAPE
			for cord in current_shape.cords:
				x, y = cord
				if x > -1:
					grid[x][y] = current_shape.color

			if change_piece:
				for pos in current_shape.cords:
					locked_positions[pos] = current_shape.color
				current_shape = next_shape
				current_shape.cords = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)
				next_shape = game_functions.get_shape()
				#locked_positions = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)
				change_piece = False

				# clear rows
				score = game_functions.clear_rows(grid, locked_positions, score, point, clear_row_sound)
				game_functions.draw_score(screen, background, score, False)
				game_functions.draw_next_figure(screen, background, next_shape)

			# screen.blit(background, (0, 0))
			# pygame.display.flip()

			# CHECK LOST
			if game_functions.check_lost(locked_positions):
				background.fill((255,255,255))	
				font = pygame.font.Font(None, int(40*(WINDOWS_SIZE[0]/600)))
				text = font.render("You Lost", 0, (10, 10, 10))
				textpos = text.get_rect()
				center = background.get_rect()
				center = center.center
				background.blit(text, (center[0]-textpos[2]//2, (center[1]-textpos[3]//2)-WINDOWS_SIZE[1]//8))
				text = font.render("Score: {}".format(score), 0, (10, 10, 10))
				textpos = text.get_rect()
				background.blit(text, (center[0]-textpos[2]//2, (center[1]-textpos[3]//2)+WINDOWS_SIZE[1]//14))

				pause = True
				screen.blit(background, (0, 0))
				pygame.display.flip()

			
			screen.blit(background, (0, 0))
			pygame.display.flip()
	
	def menu_train_ai(background,screen):
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))
		menu_sound.stop()

		running = True
		button_circle_click_state = [True, True, True, True, True]
		input_field_state = [True, True, True, True]
		input_area_1 = "10"
		input_area_2 = "10"
		input_area_3 = "500"
		input_area_4 = "5"

		# BOX
		border_weight = WINDOWS_SIZE[0] - WINDOWS_SIZE[0]//7
		border_height = WINDOWS_SIZE[1] - WINDOWS_SIZE[1]//9
		pygame.draw.rect(background, (0,0,0), (WINDOWS_SIZE[0]//15, WINDOWS_SIZE[1]//17,
													border_weight,
													border_height), 2)
		# LINE
		pygame.draw.line(background, (0,0,0), ((border_weight//2)+WINDOWS_SIZE[0]//15, WINDOWS_SIZE[1]//17),
												((border_weight//2)+WINDOWS_SIZE[0]//15, (WINDOWS_SIZE[1]//17)+border_height), 2)
		# COLUMNS LABEL
		font_label = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(WINDOWS_SIZE[0]/600)))
		text = font_label.render('Weights', 0, (0,0,0))
		textpos = text.get_rect()
		background.blit(text, (((border_weight//4)+WINDOWS_SIZE[0]//15) - textpos[2]//2, 
								(WINDOWS_SIZE[1]//17)+7))
		text = font_label.render('Genetic options', 0, (0,0,0))
		textpos = text.get_rect()
		background.blit(text, ((((border_weight//2)+WINDOWS_SIZE[0]//15) + border_weight//4 ) - textpos[2]//2, 
								(WINDOWS_SIZE[1]//17)+7))
		# DRAW ITEMS FROM WEIGHT
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(WINDOWS_SIZE[0]/600)))
		weghts_name = ['Aggregate Height', 'Complete Lines', 'Holes', 'Bumpiness', 'Height difference']

		shift = (WINDOWS_SIZE[1]//17) + textpos[3] + 10
		shift_array = []
		for ind, text in enumerate(weghts_name):
			text = font.render(text, 0, (10, 10, 10))
			add = font.render('add:', 0, (10, 10, 10))
			if ind == 0:
				textpos = text.get_rect()
				addpos = add.get_rect()
			background.blit(text, ((WINDOWS_SIZE[0]//15)+10, ((WINDOWS_SIZE[1]//17))+shift))
			background.blit(add, ((WINDOWS_SIZE[0]//15)+10, ((WINDOWS_SIZE[1]//17))+shift+addpos[3]+10))
			shift_array.append(((WINDOWS_SIZE[1]//17))+shift+int(addpos[3]*1.5)+10)
			shift += textpos[3]*2 + addpos[3]*2

		# CREATE CIRCLE BUTTON FROM WEIGHT
		button_circle_1 = Button_circle((250,0,0), (WINDOWS_SIZE[0]//15)+addpos[2]*2, shift_array[0], int(15*(WINDOWS_SIZE[1]/700)))
		button_circle_2 = Button_circle((250,0,0), (WINDOWS_SIZE[0]//15)+addpos[2]*2, shift_array[1], int(15*(WINDOWS_SIZE[1]/700)))
		button_circle_3 = Button_circle((250,0,0), (WINDOWS_SIZE[0]//15)+addpos[2]*2, shift_array[2], int(15*(WINDOWS_SIZE[1]/700)))
		button_circle_4 = Button_circle((250,0,0), (WINDOWS_SIZE[0]//15)+addpos[2]*2, shift_array[3], int(15*(WINDOWS_SIZE[1]/700)))
		button_circle_5 = Button_circle((250,0,0), (WINDOWS_SIZE[0]//15)+addpos[2]*2, shift_array[4], int(15*(WINDOWS_SIZE[1]/700)))

		# DRAW ITEMS FROM GENETIC OPTIONS
		genetic_param = ['Population size:', 'Number of games:', 'Duration of games:', 'Generations:' ]
		
		shift = (WINDOWS_SIZE[1]//17) + textpos[3] + 10
		shift_array = []
		for ind, text in enumerate(genetic_param):
			text = font.render(text, 0, (10, 10, 10))
			if ind == 0:
				textpos = text.get_rect()
				#addpos = add.get_rect()
			background.blit(text, (border_weight//2 + WINDOWS_SIZE[0]//15 + 10, ((WINDOWS_SIZE[1]//17))+shift))
			#background.blit(add, ((WINDOWS_SIZE[0]//15)+10, ((WINDOWS_SIZE[1]//17))+shift+addpos[3]+10))
			shift_array.append(((WINDOWS_SIZE[1]//17))+shift+textpos[3]+10)
			shift += textpos[3]*4

		# CREATE INPUT FIELDS FROM GENETIC PARAM
		weight_field = 100
		height_field = 40
		input_field_1 = InputField((border_weight/2)+WINDOWS_SIZE[0]//15 + border_weight//4 - weight_field//2,
									 shift_array[0], weight_field, height_field, (255,0,0), WINDOWS_SIZE[0] )
		input_field_2 = InputField((border_weight/2)+WINDOWS_SIZE[0]//15 + border_weight//4 - weight_field//2,
									 shift_array[1], weight_field, height_field, (255,0,0), WINDOWS_SIZE[0] )
		input_field_3 = InputField((border_weight/2)+WINDOWS_SIZE[0]//15 + border_weight//4 - weight_field//2,
									 shift_array[2], weight_field, height_field, (255,0,0), WINDOWS_SIZE[0] )
		input_field_4 = InputField((border_weight/2)+WINDOWS_SIZE[0]//15 + border_weight//4 - weight_field//2,
									 shift_array[3], weight_field, height_field, (255,0,0), WINDOWS_SIZE[0] )

		# START TRAIN BUTTON
		train_button = Button(color=(0,250,0), x = border_weight//2 + WINDOWS_SIZE[0]//15 + 10,
			y = shift_array[3]+height_field*2,width = border_weight//2 - 20, height = textpos[3]*2.4, text='Train AI', entire_window=WINDOWS_SIZE[0])

		while running:
			button_circle_1.draw(background, (1,1,1))
			button_circle_2.draw(background, (1,1,1))
			button_circle_3.draw(background, (1,1,1))
			button_circle_4.draw(background, (1,1,1))
			button_circle_5.draw(background, (1,1,1))
			input_field_1.draw(background, input_area_1)
			input_field_2.draw(background, input_area_2)
			input_field_3.draw(background, input_area_3)
			input_field_4.draw(background, input_area_4)
			train_button.draw(background, (1,1,1))
			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
						if button_click_state[0]:
							menu_sound.play(-1)
					# FILLING TEXT FIELDS
					if not input_field_state[0]:	
						if event.unicode.isnumeric():
							if len(input_area_1+event.unicode) <= 6: 
								if int(input_area_1+event.unicode) <= 100000 and int(input_area_1+event.unicode) > 0:
									input_area_1 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_1 = input_area_1[:-1]
					if not input_field_state[1]:	
						if event.unicode.isnumeric():
							if len(input_area_2+event.unicode) <= 6: 
								input_area_2 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_2 = input_area_2[:-1]
					if not input_field_state[2]:	
						if event.unicode.isnumeric():
							if len(input_area_3+event.unicode) <= 6: 
								input_area_3 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_3 = input_area_3[:-1]
					if not input_field_state[3]:	
						if event.unicode.isnumeric():
							if len(input_area_4+event.unicode) <= 6: 
								input_area_4 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_4 = input_area_4[:-1]
							
				if event.type == pygame.MOUSEBUTTONDOWN:
					# WEIGHTS ITEMS
					if button_circle_1.isOver(mouse_pos):
						sound_click.play()
						if button_circle_click_state[0]:
							button_circle_1.color = (0,250,0)
						else:
							button_circle_1.color = (250,0,0)
						button_circle_click_state[0] = not button_circle_click_state[0]
					if button_circle_2.isOver(mouse_pos):
						sound_click.play()
						if button_circle_click_state[1]:
							button_circle_2.color = (0,250,0)
						else:
							button_circle_2.color = (250,0,0)
						button_circle_click_state[1] = not button_circle_click_state[1]
					if button_circle_3.isOver(mouse_pos):
						sound_click.play()
						if button_circle_click_state[2]:
							button_circle_3.color = (0,250,0)
						else:
							button_circle_3.color = (250,0,0)
						button_circle_click_state[2] = not button_circle_click_state[2]
					if button_circle_4.isOver(mouse_pos):
						sound_click.play()
						if button_circle_click_state[3]:
							button_circle_4.color = (0,250,0)
						else:
							button_circle_4.color = (250,0,0)
						button_circle_click_state[3] = not button_circle_click_state[3]
					if button_circle_5.isOver(mouse_pos):
						sound_click.play()
						if button_circle_click_state[4]:
							button_circle_5.color = (0,250,0)
						else:
							button_circle_5.color = (250,0,0)
						button_circle_click_state[4] = not button_circle_click_state[4]

					# GENECIT ITEMS
					if input_field_1.isOver(mouse_pos):
						if input_field_state[0]:
							input_field_1.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[2] = True
							input_field_state[3] = True	
						else:
							input_field_1.border_color = (250,0,0)
						input_field_state[0] = not input_field_state[0]
					if input_field_2.isOver(mouse_pos):
						if input_field_state[1]:
							input_field_2.border_color = (0,250,0)
							input_field_state[0] = True
							input_field_state[2] = True
							input_field_state[3] = True
						else:
							input_field_2.border_color = (250,0,0)
						input_field_state[1] = not input_field_state[1]
					if input_field_3.isOver(mouse_pos):
						if input_field_state[2]:
							input_field_3.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[0] = True
							input_field_state[3] = True
						else:
							input_field_3.border_color = (250,0,0)
						input_field_state[2] = not input_field_state[2]
					if input_field_4.isOver(mouse_pos):
						if input_field_state[3]:
							input_field_4.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[2] = True
							input_field_state[0] = True
						else:
							input_field_4.border_color = (250,0,0)
						input_field_state[3] = not input_field_state[3]
					# TRAIN BUTTON ITEMS
					if train_button.isOver(mouse_pos):
						sound_click.play()
						if input_area_1 == '':
							input_area_1 = '10'
						if input_area_1 == '1':
							input_area_1 = '2'
						if input_area_1 == '':
							input_area_1 = '10'
						if input_area_1 == '':
							input_area_1 = '500'
						if input_area_1 == '':
							input_area_1 = '5'
						train_ai(background, screen, button_circle_click_state,
													 int(input_area_1),
													 int(input_area_2),
													 int(input_area_3),
													 int(input_area_4))
						background.fill((255, 255, 255))
						running = False
				if event.type == pygame.MOUSEMOTION:
					# STUFF FROM WEIGHTS
					if button_circle_click_state[0]:
						if button_circle_1.isOver(mouse_pos):
							button_circle_1.color = (0,250,0)
						else:
							button_circle_1.color = (250,0,0)

					if button_circle_click_state[1]:
						if button_circle_2.isOver(mouse_pos):
							button_circle_2.color = (0,250,0)
						else:
							button_circle_2.color = (250,0,0)

					if button_circle_click_state[2]:
						if button_circle_3.isOver(mouse_pos):
							button_circle_3.color = (0,250,0)
						else:
							button_circle_3.color = (250,0,0)

					if button_circle_click_state[3]:
						if button_circle_4.isOver(mouse_pos):
							button_circle_4.color = (0,250,0)
						else:
							button_circle_4.color = (250,0,0)

					if button_circle_click_state[4]:
						if button_circle_5.isOver(mouse_pos):
							button_circle_5.color = (0,250,0)
						else:
							button_circle_5.color = (250,0,0)
					# STUFF FROM GENETIC
					if input_field_state[0]:
						if input_field_1.isOver(mouse_pos):
							input_field_1.border_color = (0,250,0)
						else:
							input_field_1.border_color = (250,0,0)
					if input_field_state[1]:
						if input_field_2.isOver(mouse_pos):
							input_field_2.border_color = (0,250,0)
						else:
							input_field_2.border_color = (250,0,0)
					if input_field_state[2]:
						if input_field_3.isOver(mouse_pos):
							input_field_3.border_color = (0,250,0)
						else:
							input_field_3.border_color = (250,0,0)
					if input_field_state[3]:
						if input_field_4.isOver(mouse_pos):
							input_field_4.border_color = (0,250,0)
						else:
							input_field_4.border_color = (250,0,0)
					# STUFF FROM TRAIN BUTTON
					if train_button.isOver(mouse_pos):
						train_button.color = (250,0,0)
					else:
						train_button.color = (0,250,0)

			screen.blit(background, (0, 0))
			pygame.display.flip()
		
	def train_ai(background, screen, weight_markers, *genetic_param):
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))

		genetic_algoritm = GeneticAlgoritm(weight_markers, genetic_param)
		game_functions = GameFunctions(WINDOWS_SIZE[0],WINDOWS_SIZE[1])
		population = genetic_algoritm.initialized_population()

		for gener in range(1,genetic_algoritm.generations+1):
			member_results_list = []
			for member in range(1,genetic_algoritm.population_size+1):
				session_score = 0
				session_figure = 0
				for n_game in range(1,genetic_algoritm.number_game+1):
					ai_player = AI( population[member-1] )
					grid = game_functions.create_grid()
					current_shape = game_functions.get_shape()
					next_shape = game_functions.get_shape()
					running = True
					change_piece = False
					locked_positions = {}
					clock = pygame.time.Clock()
					current_speed = 0.005 # 0.07
					fall_time = 0
					score = 0 
					tmp_score = 0
					point = 10
					number_figure = 0
					game_functions.draw_score(screen, background, score, True)
					game_functions.draw_next_figure(screen, background, next_shape)
					game_functions.draw_member(screen, background, member, genetic_algoritm.population_size)
					game_functions.draw_number_game(screen, background, n_game, genetic_algoritm.number_game)
					game_functions.draw_max_figure(screen, background, number_figure, genetic_algoritm.duration_of_game)
					game_functions.draw_generations(screen, background, gener, genetic_algoritm.generations)
					pause = False
					clear_row_sound = pygame.mixer.Sound('data/audio/clear_row.wav')
					current_shape.cords = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)

					while running:
						fall_speed = current_speed
						game_functions.draw_grid(background, grid, not button_click_state[1])
						game_functions.draw_max_figure(screen, background, number_figure, genetic_algoritm.duration_of_game)
						grid = game_functions.create_grid(locked_positions)
						fall_time += clock.get_rawtime()
						clock.tick()

						# FALLING CODE
						if fall_time/1000 >= fall_speed and not pause:
							fall_time = 0
							current_shape.cords = [ (x[0]+1, x[1]) for x in current_shape.cords]
							if game_functions.valid_space(current_shape.cords, grid) and not sum([ 1 if i[0] < 0 else 0 for i in current_shape.cords]) > 0:
								current_shape.cords = [ (x[0]-1, x[1]) for x in current_shape.cords]
								#locked_positions = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)
								change_piece = True

						for event in pygame.event.get():
							mouse_pos = pygame.mouse.get_pos()
							if event.type == QUIT:
								pygame.quit()
								sys.exit()
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_q:
									running = False
								if event.key == pygame.K_ESCAPE:
									if button_click_state[0]:
										menu_sound.play(-1)
									return
								if event.key == pygame.K_SPACE:
									pause = not pause

						# MOVE SHAPE
						for cord in current_shape.cords:
							x, y = cord
							if x > -1:
								grid[x][y] = current_shape.color

						if change_piece:
							for pos in current_shape.cords:
								locked_positions[pos] = current_shape.color
							current_shape = next_shape
							current_shape.cords = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)
							next_shape = game_functions.get_shape()
							#locked_positions = ai_player.calculate_best_move(grid, locked_positions, current_shape, game_functions)
							change_piece = False
							number_figure += 1

							# clear rows
							score = game_functions.clear_rows(grid, locked_positions, score, point, clear_row_sound)
							game_functions.draw_score(screen, background, score, False)
							game_functions.draw_next_figure(screen, background, next_shape)

						# screen.blit(background, (0, 0))
						# pygame.display.flip()

						# FINISH FRAME
						if game_functions.check_lost(locked_positions, number_figure, genetic_algoritm.duration_of_game):
							running = False
						
						screen.blit(background, (0, 0))
						pygame.display.flip()

					session_score += score
					session_figure += number_figure

				member_results_list.append((population[member-1],session_score, session_figure))

			descendants = genetic_algoritm.tournament_selection(member_results_list)	
			population = descendants + [ i[0] for i in sorted(sorted(member_results_list, key=lambda x: x[2]), key=lambda x:x[1])[len(descendants):]]
			
		
		# FINISH SCREEN
		background.fill((255,255,255))	
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(45*(WINDOWS_SIZE[0]/600)))
		text = font.render("Training is over", 0, (10, 10, 10))
		textpos_1 = text.get_rect()
		center = background.get_rect().center
		background.blit(text, (center[0]-textpos_1[2]//2, (center[1]-textpos_1[3]//2)-WINDOWS_SIZE[1]//6))

		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(30*(WINDOWS_SIZE[0]/600)))
		text = font.render("Most fit weight vector:", 0, (10, 10, 10))
		textpos_2 = text.get_rect()
		background.blit(text, (center[0]-textpos_2[2]//2, center[1]-textpos_2[3]))

		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(25*(WINDOWS_SIZE[0]/600)))
		text = font.render("{}".format(',  '.join([ str(x)[:6] for x in population[-1]])), 0, (10, 10, 10))
		textpos = text.get_rect()
		background.blit(text, (center[0]-textpos[2]//2, (center[1]-textpos[3])+WINDOWS_SIZE[1]//12))

		button_1 = Button(color=(0,250,0), x = center[0]-textpos_2[2]//2,
			y = center[1]+textpos_1[3]*2.5,width=textpos_2[2],height=textpos_1[3]*1.6, text='Play with weights', entire_window=WINDOWS_SIZE[0])
		button_2 = Button(color=(0,250,0), x = center[0]-textpos_2[2]//2,
			y = center[1]+textpos_1[3]*4.8,width=textpos_2[2],height=textpos_1[3]*1.6, text='Back', entire_window=WINDOWS_SIZE[0])

		running = True
		while running:
			button_1.draw(background, (1,1,1))
			button_2.draw(background, (1,1,1))
			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if button_click_state[0]:
							menu_sound.play(-1)
						return
				if event.type == pygame.MOUSEBUTTONDOWN:
					if button_1.isOver(mouse_pos):
						sound_click.play()
						markers = [ not i for i in weight_markers]
						play_ai(background, screen, markers, population[-1])
						return
						background.fill((255, 255, 255)) # add blid from erase previous content
					if button_2.isOver(mouse_pos):
						sound_click.play()
						return
						background.fill((255, 255, 255))
				if event.type == pygame.MOUSEMOTION:
					if button_1.isOver(mouse_pos):
						button_1.color = (250,0,0)
					else:
						button_1.color = (0,250,0)

					if button_2.isOver(mouse_pos):
						button_2.color = (250,0,0)
					else:
						button_2.color = (0,250,0)

			screen.blit(background, (0, 0))
			pygame.display.flip()

		
		# screen.blit(background, (0, 0))
		# pygame.display.flip()

	def menu_play_ai(background,screen,weight_markers):
		background.fill((255, 255, 255))
		screen.blit(background, (0, 0))
		menu_sound.stop()

		running = True
		input_field_state = [True, True, True, True, True]
		input_area_1 = "-0."
		input_area_2 = "0."
		input_area_3 = "-0."
		input_area_4 = "-0."
		input_area_5 = "-0."

		center = background.get_rect().center
		font_label = pygame.font.Font('data/font/arial_narrow_7.ttf', int(40*(WINDOWS_SIZE[0]/600)))
		text = font_label.render('Input weights', 0, (0,0,0))
		textpos = text.get_rect()
		background.blit(text, (center[0]-textpos[2]//2, 2*WINDOWS_SIZE[1]//10 ))

		# CREATE INPUT FIELDS FROM WEIGHTS
		input_field_1 = InputField(50*WINDOWS_SIZE[0]//600,
									 3*WINDOWS_SIZE[1]//10, 95, textpos[3], (255,0,0), WINDOWS_SIZE[0] )
		input_field_2 = InputField(150*WINDOWS_SIZE[0]//600,
									 3*WINDOWS_SIZE[1]//10, 95, textpos[3], (255,0,0), WINDOWS_SIZE[0] )
		input_field_3 = InputField(250*WINDOWS_SIZE[0]//600,
									 3*WINDOWS_SIZE[1]//10, 95, textpos[3], (255,0,0), WINDOWS_SIZE[0] )
		input_field_4 = InputField(350*WINDOWS_SIZE[0]//600,
									 3*WINDOWS_SIZE[1]//10, 95, textpos[3], (255,0,0), WINDOWS_SIZE[0] )
		input_field_5 = InputField(450*WINDOWS_SIZE[0]//600,
									 3*WINDOWS_SIZE[1]//10, 95, textpos[3], (255,0,0), WINDOWS_SIZE[0] )

		text = font_label.render('Implement weights', 0, (0,0,0))
		textpos = text.get_rect()
		button_1 = Button(color=(0,250,0), x = center[0]-textpos[2]//2,
			y = WINDOWS_SIZE[1]//2 - WINDOWS_SIZE[1]//16,width=textpos[2],height=textpos[3]*1.5, text='Implement weights', entire_window=WINDOWS_SIZE[0])
		button_2 = Button(color=(0,250,0), x = center[0]-textpos[2]//2,
			y = WINDOWS_SIZE[1]//2 + WINDOWS_SIZE[1]//16,width=textpos[2],height=textpos[3]*1.5, text='Play default', entire_window=WINDOWS_SIZE[0])

		while running:
			button_1.draw(background, (1,1,1))
			button_2.draw(background, (1,1,1))
			input_field_1.draw(background, input_area_1)
			input_field_2.draw(background, input_area_2)
			input_field_3.draw(background, input_area_3)
			input_field_4.draw(background, input_area_4)
			input_field_5.draw(background, input_area_5)
			for event in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
						if button_click_state[0]:
							menu_sound.play(-1)
					# FILLING TEXT FIELDS
					if not input_field_state[0]:	
						if event.unicode.isnumeric():
							if len(input_area_1+event.unicode) <= 6: 
								#if int(input_area_1+event.unicode) <= 100000:
								input_area_1 += event.unicode
						if event.unicode == "-":
							if len(input_area_1+event.unicode) == 1:
								input_area_1 += event.unicode
						if event.unicode == ".":
							if len(input_area_1+event.unicode) == 3:
								input_area_1 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_1 = input_area_1[:-1]
					if not input_field_state[1]:	
						if event.unicode.isnumeric():
							if len(input_area_2+event.unicode) <= 6: 
								input_area_2 += event.unicode
						if event.unicode == ".":
							if len(input_area_2+event.unicode) == 2:
								input_area_2 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_2 = input_area_2[:-1]
					if not input_field_state[2]:	
						if event.unicode.isnumeric():
							if len(input_area_3+event.unicode) <= 6: 
								input_area_3 += event.unicode
						if event.unicode == "-":
							if len(input_area_3+event.unicode) == 1:
								input_area_3 += event.unicode
						if event.unicode == ".":
							if len(input_area_3+event.unicode) == 3:
								input_area_3 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_3 = input_area_3[:-1]
					if not input_field_state[3]:	
						if event.unicode.isnumeric():
							if len(input_area_4+event.unicode) <= 6: 
								input_area_4 += event.unicode
						if event.unicode == "-":
							if len(input_area_4+event.unicode) == 1:
								input_area_4 += event.unicode
						if event.unicode == ".":
							if len(input_area_4+event.unicode) == 3:
								input_area_4 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_4 = input_area_4[:-1]
					if not input_field_state[4]:	
						if event.unicode.isnumeric():
							if len(input_area_5+event.unicode) <= 6: 
								input_area_5 += event.unicode
						if event.unicode == "-":
							if len(input_area_5+event.unicode) == 1:
								input_area_5 += event.unicode
						if event.unicode == ".":
							if len(input_area_5+event.unicode) == 3:
								input_area_5 += event.unicode
						elif event.key == K_BACKSPACE:
							input_area_5 = input_area_5[:-1]
							
				if event.type == pygame.MOUSEBUTTONDOWN:
					# GENECIT ITEMS
					if input_field_1.isOver(mouse_pos):
						if input_field_state[0]:
							input_field_1.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[2] = True
							input_field_state[3] = True	
							input_field_state[4] = True
						else:
							input_field_1.border_color = (250,0,0)
						input_field_state[0] = not input_field_state[0]
					if input_field_2.isOver(mouse_pos):
						if input_field_state[1]:
							input_field_2.border_color = (0,250,0)
							input_field_state[0] = True
							input_field_state[2] = True
							input_field_state[3] = True
							input_field_state[4] = True
						else:
							input_field_2.border_color = (250,0,0)
						input_field_state[1] = not input_field_state[1]
					if input_field_3.isOver(mouse_pos):
						if input_field_state[2]:
							input_field_3.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[0] = True
							input_field_state[3] = True
							input_field_state[4] = True
						else:
							input_field_3.border_color = (250,0,0)
						input_field_state[2] = not input_field_state[2]
					if input_field_4.isOver(mouse_pos):
						if input_field_state[3]:
							input_field_4.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[2] = True
							input_field_state[0] = True
							input_field_state[4] = True
						else:
							input_field_4.border_color = (250,0,0)
						input_field_state[3] = not input_field_state[3]
					if input_field_5.isOver(mouse_pos):
						if input_field_state[4]:
							input_field_5.border_color = (0,250,0)
							input_field_state[1] = True
							input_field_state[2] = True
							input_field_state[3] = True
							input_field_state[0] = True
						else:
							input_field_5.border_color = (250,0,0)
						input_field_state[4] = not input_field_state[4]
					# BUTTON ITEMS
					if button_1.isOver(mouse_pos):
						sound_click.play()
						play_ai(background, screen, weight_markers, [float(input_area_1),
																	 float(input_area_2),
																	 float(input_area_3),
																	 float(input_area_4),
																	 float(input_area_5)])
						return
						background.fill((255, 255, 255)) # add blid from erase previous content
					if button_2.isOver(mouse_pos):
						sound_click.play()
						play_ai(background, screen, weight_markers)
						return
						background.fill((255, 255, 255))

				if event.type == pygame.MOUSEMOTION:
					if input_field_state[0]:
						if input_field_1.isOver(mouse_pos):
							input_field_1.border_color = (0,250,0)
						else:
							input_field_1.border_color = (250,0,0)
					if input_field_state[1]:
						if input_field_2.isOver(mouse_pos):
							input_field_2.border_color = (0,250,0)
						else:
							input_field_2.border_color = (250,0,0)
					if input_field_state[2]:
						if input_field_3.isOver(mouse_pos):
							input_field_3.border_color = (0,250,0)
						else:
							input_field_3.border_color = (250,0,0)
					if input_field_state[3]:
						if input_field_4.isOver(mouse_pos):
							input_field_4.border_color = (0,250,0)
						else:
							input_field_4.border_color = (250,0,0)
					if input_field_state[4]:
						if input_field_5.isOver(mouse_pos):
							input_field_5.border_color = (0,250,0)
						else:
							input_field_5.border_color = (250,0,0)

					# STUFF FROM BUTTON
					if button_1.isOver(mouse_pos):
						button_1.color = (250,0,0)
					else:
						button_1.color = (0,250,0)

					if button_2.isOver(mouse_pos):
						button_2.color = (250,0,0)
					else:
						button_2.color = (0,250,0)
			
			screen.blit(background, (0, 0))
			pygame.display.flip()		

	if __name__ == '__main__': 
		IWS, FLAG =main()
		if FLAG:
			return IWS

while True:
	INDX_WINDOWS_SIZE = infinity_loop(LIST_WINDOWS_SIZE, INDX_WINDOWS_SIZE)
