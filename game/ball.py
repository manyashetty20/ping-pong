
import pygame
import random

class Ball:
    
    COLOR = (255, 255, 255)

    def __init__(self, x, y, width, height, screen_width, screen_height):
        
        self.initial_x = x
        self.initial_y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.x = x
        self.y = y
        
        self.dx = 0
        self.dy = 0
        self.reset() 

    def draw(self, screen):
        """
        Draws the ball on the screen as an ellipse.
        This is the missing method.
        """
        pygame.draw.ellipse(screen, self.COLOR, self.rect())

    def move(self):
        """Updates the ball's position based on its velocity."""
        self.x += self.dx
        self.y += self.dy

    def rect(self):
        """Returns a pygame.Rect object representing the ball's current position."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self):
        """Resets the ball to the center with a new random velocity."""
        self.x = self.initial_x
        self.y = self.initial_y
        
        direction = 1 if random.random() < 0.5 else -1
        self.dx = 7 * direction
        self.dy = random.uniform(-4, 4)