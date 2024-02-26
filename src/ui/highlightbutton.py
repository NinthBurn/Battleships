import pygame

class HighlightButton():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self, surface):
		# Draws the button and returns True if it has been pressed. Otherwise, it returns False.
		action = False
		pos = pygame.mouse.get_pos()
		#surface.blit(self.image, (self.rect.x, self.rect.y))
		if self.rect.collidepoint(pos):
			surface.blit(self.image, (self.rect.x, self.rect.y))
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action