import pygame
import sys
from game import LudoGame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ludo Game - 2 Player")
    clock = pygame.time.Clock()
    
    # Initialize game
    game = LudoGame()
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.roll_dice()
        
        # Update game state
        game.update()
        
        # Draw everything
        screen.fill(WHITE)
        game.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
