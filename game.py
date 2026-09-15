import pygame
import random
from board import Board
from player import Player

class LudoGame:
    def __init__(self):
        self.board = Board()
        self.players = [
            Player(0, "Player 1", (255, 0, 0)),      # Red
            Player(1, "Player 2", (255, 255, 0))     # Yellow
        ]
        self.current_player_index = 0
        self.dice_value = 0
        self.dice_rolled = False
        self.game_over = False
        
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def roll_dice(self):
        """Roll the dice and move to next player if conditions aren't met"""
        if self.dice_rolled or self.game_over:
            return
        
        self.dice_value = random.randint(1, 6)
        self.dice_rolled = True
        print(f"{self.get_current_player().name} rolled {self.dice_value}")
        
        # Auto move to next player after 2 seconds
        pygame.time.set_timer(pygame.USEREVENT, 2000)
    
    def move_piece(self, piece_index):
        """Move a piece for the current player"""
        if not self.dice_rolled or self.dice_value == 0:
            return False
        
        player = self.get_current_player()
        if piece_index < len(player.pieces):
            player.move_piece(piece_index, self.dice_value)
            self.dice_rolled = False
            self.dice_value = 0
            return True
        
        return False
    
    def next_player(self):
        """Switch to next player"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.dice_rolled = False
        self.dice_value = 0
        print(f"\n{self.get_current_player().name}'s turn!")
    
    def handle_click(self, pos):
        """Handle mouse clicks on pieces"""
        # This will be extended to handle piece selection and movement
        pass
    
    def update(self):
        """Update game state"""
        # Check for game over
        for player in self.players:
            if player.all_pieces_home():
                self.game_over = True
                print(f"{player.name} WINS!")
    
    def draw(self, screen):
        """Draw the game"""
        self.board.draw(screen)
        
        # Draw all pieces
        for player in self.players:
            player.draw(screen)
        
        # Draw dice value
        font = pygame.font.Font(None, 36)
        if self.dice_value > 0:
            dice_text = font.render(f"Dice: {self.dice_value}", True, (0, 0, 0))
            screen.blit(dice_text, (600, 50))
        
        # Draw current player
        current_text = font.render(f"Turn: {self.get_current_player().name}", True, self.get_current_player().color)
        screen.blit(current_text, (50, 50))
        
        # Draw instructions
        small_font = pygame.font.Font(None, 24)
        instructions = small_font.render("Press SPACE to roll dice", True, (0, 0, 0))
        screen.blit(instructions, (50, 750))
