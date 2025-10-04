import pygame
from game.game_engine import GameEngine

pygame.init()
pygame.mixer.init() 

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and engine.game_state == "game_over":
                    running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()