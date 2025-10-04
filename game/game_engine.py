
import pygame
from .paddle import Paddle
from .ball import Ball 

class GameEngine:
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BALL_WIDTH, BALL_HEIGHT = 15, 15 
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.player = Paddle(10, height // 2 - Paddle.PADDLE_HEIGHT // 2)
        self.ai = Paddle(width - 10 - Paddle.PADDLE_WIDTH, height // 2 - Paddle.PADDLE_HEIGHT // 2)
        self.ai.speed = 5
        
        self.ball = Ball(width // 2, height // 2, self.BALL_WIDTH, self.BALL_HEIGHT, self.width, self.height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5
        self.game_state = "playing"
        self.winner = None

        self.score_font = pygame.font.SysFont("monospace", 50)
        self.menu_font = pygame.font.SysFont("monospace", 30)

        try:
            self.paddle_hit_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        except pygame.error:
            print("Warning: Sound files not found.")
            self.paddle_hit_sound = self.wall_bounce_sound = self.score_sound = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.game_state == "playing":
            if keys[pygame.K_w]:
                self.player.move(-1, self.height)
            if keys[pygame.K_s]:
                self.player.move(1, self.height)
        
        elif self.game_state == "game_over":
            if keys[pygame.K_1]: self.reset_game(3)
            if keys[pygame.K_2]: self.reset_game(5)
            if keys[pygame.K_3]: self.reset_game(7)

    def update(self):
        if self.game_state != "playing":
            return

        self.ball.move()
        self.ai.auto_track(self.ball, self.height)
        self._handle_collisions()
        self._check_score()
        self._check_for_winner()

    def render(self, screen):
        screen.fill(self.BLACK)
        if self.game_state == "playing":
            self._draw_playing_screen(screen)
        elif self.game_state == "game_over":
            self._draw_game_over_screen(screen)

    def _handle_collisions(self):
        if self.ball.y <= 0 or (self.ball.y + self.ball.height) >= self.height:
            self.ball.dy *= -1
            if self.wall_bounce_sound: self.wall_bounce_sound.play()

        if self.player.rect().colliderect(self.ball.rect()):
            self._handle_paddle_collision(self.player)
            if self.paddle_hit_sound: self.paddle_hit_sound.play()
            
        if self.ai.rect().colliderect(self.ball.rect()):
            self._handle_paddle_collision(self.ai)
            if self.paddle_hit_sound: self.paddle_hit_sound.play()

    def _handle_paddle_collision(self, paddle):
        self.ball.dx *= -1
        
        middle_y = paddle.rect().centery
        difference_in_y = middle_y - self.ball.rect().centery
        reduction_factor = (paddle.height / 2) / 7 
        y_vel = difference_in_y / reduction_factor
        self.ball.dy = -1 * y_vel

    def _check_score(self):
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound: self.score_sound.play()
            self.ball.reset()
        elif (self.ball.x + self.ball.width) >= self.width:
            self.player_score += 1
            if self.score_sound: self.score_sound.play()
            self.ball.reset()
    
    def _check_for_winner(self):
        if self.player_score >= self.winning_score:
            self.winner = "Player"
            self.game_state = "game_over"
        elif self.ai_score >= self.winning_score:
            self.winner = "AI"
            self.game_state = "game_over"

    def _draw_playing_screen(self, screen):
        for i in range(10, self.height, self.height // 20):
            if i % 2 == 1: continue
            pygame.draw.rect(screen, self.WHITE, (self.width//2 - 2, i, 4, self.height//20))
            
        player_text = self.score_font.render(f"{self.player_score}", 1, self.WHITE)
        ai_text = self.score_font.render(f"{self.ai_score}", 1, self.WHITE)
        screen.blit(player_text, (self.width // 4 - player_text.get_width() // 2, 20))
        screen.blit(ai_text, (self.width * 3 // 4 - ai_text.get_width() // 2, 20))

        self.player.draw(screen)
        self.ai.draw(screen)
        self.ball.draw(screen)
    
    def _draw_game_over_screen(self, screen):
        winner_text = self.score_font.render(f"{self.winner} Wins!", 1, self.WHITE)
        screen.blit(winner_text, (self.width//2 - winner_text.get_width()//2, self.height//4))

        replay_text = self.menu_font.render("Press a key to play again or Q to quit", 1, self.WHITE)
        screen.blit(replay_text, (self.width//2 - replay_text.get_width()//2, self.height//2))
        
        option1_text = self.menu_font.render("[1] - Best of 3", 1, self.WHITE)
        screen.blit(option1_text, (self.width//2 - option1_text.get_width()//2, self.height//2 + 50))
        
        option2_text = self.menu_font.render("[2] - Best of 5", 1, self.WHITE)
        screen.blit(option2_text, (self.width//2 - option2_text.get_width()//2, self.height//2 + 90))

        option3_text = self.menu_font.render("[3] - Best of 7", 1, self.WHITE)
        screen.blit(option3_text, (self.width//2 - option3_text.get_width()//2, self.height//2 + 130))

    def reset_game(self, winning_score):
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = winning_score
        self.winner = None
        self.game_state = "playing"
        self.ball.reset()