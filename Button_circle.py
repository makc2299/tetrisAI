import pygame

class Button_circle():
	def __init__(self, color, x, y, R):
		self.color = color
		self.x = x
		self.y = y
		self.R = R

	def draw(self,win,outline=None):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.circle(win, outline, (self.x, self.y), self.R-1, 2)
			
		pygame.draw.circle(win, self.color, (self.x, self.y), self.R, 0)
		
		
	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if (pos[0] - self.x)**2 + (pos[1] - self.y)**2 <= self.R**2 :
			return True
			
		return False