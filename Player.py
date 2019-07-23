

#images
import pygame
pygame.init()

from Constants import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT
from Utils import load_image

from copy import deepcopy

class Player:
	width = 30
	height = 50

	vel_x = 0
	vel_y = 0
	max_falling_speed = 20

	acceleration = 0.5
	max_vel_x = 7

	color = (255, 0, 0)
	speed = 5

	def __init__(self):
		self.x = 30
		self.y = 500
		self.score = 0 # negate floor platform

		
		self.spritesheet_image = load_image('12.png')
		self.spritesheet = []


		# Idle

		self.cropped = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.cropped2 = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped2.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.cropped3 = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped3.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.spritesheet.append(self.cropped)
		self.spritesheet.append(self.cropped2)
		self.spritesheet.append(self.cropped3)
		
		# Going right
		self.cropped4 = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped4.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.cropped5 = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped5.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.cropped6 = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped6.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.spritesheet.append(self.cropped4)
		self.spritesheet.append(self.cropped5)
		self.spritesheet.append(self.cropped6)

		# Going left
		self.spritesheet.append(pygame.transform.flip(self.cropped4, True, False))
		self.spritesheet.append(pygame.transform.flip(self.cropped5, True, False))
		self.spritesheet.append(pygame.transform.flip(self.cropped6, True, False))

		# Jumping
		self.cropped7 = pygame.Surface((36, 58), pygame.SRCALPHA, 32)
		self.cropped7.blit(self.spritesheet_image, (0, 0), (0, 0, 36, 58))
		self.spritesheet.append(self.cropped7)
		self.spritesheet.append(self.cropped7)
		self.spritesheet.append(self.cropped7)

		self.sprite_index_x = 0
		self.sprite_index_y = 0
		self.frame_counter = 0
		self.frame_delay = 9

	def draw(self, game_display, camera):
		game_display.blit(self.spritesheet[self.sprite_index_y*3 + self.sprite_index_x], (self.x, self.y-camera.y))

		self.frame_counter += 1
		if self.frame_counter >= self.frame_delay:
			self.sprite_index_x += 1
			if self.sprite_index_x > 2:
				self.sprite_index_x = 0
			self.frame_counter = 0
	
	def update(self):
		self.x += self.vel_x
		self.y += self.vel_y
		self.vel_y += GRAVITY
		if self.vel_y > self.max_falling_speed:
			self.vel_y = self.max_falling_speed
		if self.x <= 0:
			self.x = 0
		if self.x + self.width >= SCREEN_WIDTH:
			self.x = SCREEN_WIDTH - self.width

	def combo(self):
		if self.x == 0:
			if self.vel_y < 0:
				if self.vel_x < 0:
					self.vel_y -= 10
					self.vel_x *= -2.5
		if self.x + self.width >= SCREEN_WIDTH:
			if self.vel_y < 0:
				if self.vel_x > 0:
					self.vel_y -= 10
					self.vel_x *= -2.5

	def on_platform(self, platform):
		# return platform.rect.top <= self.y + self.height
		return platform.rect.collidepoint((self.x, self.y + self.height)) or \
			platform.rect.collidepoint((self.x+self.width, self.y + self.height))

	def on_any_platform(self, platform_controller, floor):
		for p in platform_controller.platform_set:
			if self.on_platform(p):
				return True
		if self.on_platform(floor):
			return True
		return False
	
	def collide_platform(self, platform, index):
		for i in range(0,self.vel_y):
			if pygame.Rect(self.x, self.y-i, self.width, self.height).colliderect(platform.rect):
				if platform.rect.collidepoint((self.x, self.y + self.height-i)) or \
		 	platform.rect.collidepoint((self.x+self.width, self.y + self.height-i)): #do not change! no on_platform here
					self.y = platform.y - self.height
					if not platform.collected_score:
						self.score += 10
						if self.score < index * 10:
							self.score = index * 10
						platform.collected_score = True

	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

	def fallen_off_screen(self, camera):
		if self.y - camera.y + self.height >= SCREEN_HEIGHT:
			return True
		return False
