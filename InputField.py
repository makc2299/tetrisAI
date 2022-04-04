import pygame

class InputField():

	def __init__(self, x, y, weight, height, border_color, entire_window):
		self.x = x
		self.y = y
		self.weight = weight
		self.height = height
		self.border_color = border_color
		self.entire_window = entire_window

	def draw(self, backgraund, text):
		pygame.draw.rect(backgraund, self.border_color, (self.x,self.y,
						self.weight*(self.entire_window/600),self.height*(self.entire_window/600)),2)


		#font = pygame.font.SysFont('comicsans', 25)
		font = pygame.font.Font('data/font/arial_narrow_7.ttf', int(20*(self.entire_window/600)))
		text = font.render(text, 1, (0,0,0))
		textpos = text.get_rect()
		if textpos[2] < self.weight-5:
			backgraund.fill((255,255,255),  (self.x+2,self.y+2,(self.weight-3)*(self.entire_window/600),(self.height-3)*(self.entire_window/600)))
			backgraund.blit(text, (self.x + ((self.weight/2)*(self.entire_window/600) - text.get_width()/2), self.y + ((self.height/2)*(self.entire_window/600) - text.get_height()/2)))

	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.weight*(self.entire_window/600):
			if pos[1] > self.y and pos[1] < self.y + self.height*(self.entire_window/600):
				return True
			
		return False