import pygame

class Paddle:
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = self.PADDLE_WIDTH
        self.height = self.PADDLE_HEIGHT
        self.speed = 7

    def draw(self, screen):
        """A new method to draw the paddle."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def move(self, direction, screen_height):
        """Moves the paddle up (direction=-1) or down (direction=1)."""
        self.y += self.speed * direction
        
        if self.y < 0:
            self.y = 0
        if self.y > screen_height - self.height:
            self.y = screen_height - self.height

    def rect(self):
        """Returns the pygame.Rect object for the paddle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """AI logic to track the center of the ball."""
        
        if ball.rect().centery < self.rect().centery:
            self.move(-1, screen_height) # Move up
        elif ball.rect().centery > self.rect().centery:
            self.move(1, screen_height) # Move down