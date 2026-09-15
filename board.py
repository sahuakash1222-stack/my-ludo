import pygame

class Board:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.square_size = 40
        self.board_color = (240, 240, 240)
        self.line_color = (100, 100, 100)
        
        # Ludo board positions (simplified for 2 players)
        # Total 52 squares + 4 home squares per player
        self.total_squares = 52
        self.home_squares = 4
        
    def draw(self, screen):
        """Draw the Ludo board"""
        # Fill background
        screen.fill(self.board_color)
        
        # Draw outer border
        pygame.draw.rect(screen, self.line_color, (50, 50, 700, 700), 3)
        
        # Draw grid
        self._draw_grid(screen)
        
        # Draw home areas for each player
        self._draw_home_areas(screen)
    
    def _draw_grid(self, screen):
        """Draw the main board grid"""
        start_x, start_y = 50, 50
        
        for i in range(18):
            # Horizontal lines
            pygame.draw.line(screen, self.line_color, 
                           (start_x, start_y + i * self.square_size),
                           (start_x + 700, start_y + i * self.square_size), 1)
            # Vertical lines
            pygame.draw.line(screen, self.line_color,
                           (start_x + i * self.square_size, start_y),
                           (start_x + i * self.square_size, start_y + 700), 1)
    
    def _draw_home_areas(self, screen):
        """Draw home areas for players"""
        font = pygame.font.Font(None, 20)
        
        # Player 1 (Red) - Top Left
        pygame.draw.rect(screen, (255, 200, 200), (50, 50, 80, 80))
        text = font.render("P1 Home", True, (255, 0, 0))
        screen.blit(text, (55, 80))
        
        # Player 2 (Yellow) - Bottom Right
        pygame.draw.rect(screen, (255, 255, 200), (670, 670, 80, 80))
        text = font.render("P2 Home", True, (255, 255, 0))
        screen.blit(text, (675, 700))
    
    def get_position(self, player_id, piece_index, square_number):
        """Get pixel coordinates for a piece on the board"""
        if square_number == -1:  # In home
            # Home position based on piece index
            home_x = 60 + (piece_index % 2) * 30
            home_y = 60 + (piece_index // 2) * 30
            return (home_x, home_y)
        
        # Simplified board path - you can make this more complex
        x = 50 + (square_number % 17) * 40 + 20
        y = 50 + (square_number // 17) * 40 + 20
        
        return (x, y)
