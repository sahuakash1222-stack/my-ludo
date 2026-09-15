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
        self.selected_piece = None  # Track which piece is selected
        self.message = "Press SPACE to roll dice"
        
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def roll_dice(self):
        """Roll the dice"""
        if self.dice_rolled or self.game_over:
            return
        
        self.dice_value = random.randint(1, 6)
        self.dice_rolled = True
        self.selected_piece = None
        self.message = f"{self.get_current_player().name} rolled {self.dice_value}! Click a piece to move it."
        print(f"{self.get_current_player().name} rolled {self.dice_value}")
    
    def move_piece(self, piece_index):
        """Move a specific piece for the current player"""
        if not self.dice_rolled or self.dice_value == 0:
            self.message = "Roll the dice first!"
            return False
        
        player = self.get_current_player()
        if piece_index < len(player.pieces):
            piece = player.pieces[piece_index]
            
            # Check if piece is in home and can move out (optional: only on 6)
            if piece.is_home and self.dice_value != 6:
                self.message = "Need a 6 to move piece out of home!"
                return False
            
            player.move_piece(piece_index, self.dice_value)
            self.dice_rolled = False
            self.dice_value = 0
            self.selected_piece = None
            self.message = f"Moved piece {piece_index + 1}. Next player's turn!"
            self.next_player()
            return True
        
        return False
    
    def next_player(self):
        """Switch to next player"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.dice_rolled = False
        self.dice_value = 0
        self.message = f"{self.get_current_player().name}'s turn! Press SPACE to roll."
        print(f"\n{self.get_current_player().name}'s turn!")
    
    def handle_click(self, pos):
        """Handle mouse clicks on pieces"""
        player = self.get_current_player()
        
        # Check if any piece was clicked
        for i, piece in enumerate(player.pieces):
            piece_pos = self._get_piece_screen_position(player, piece)
            distance = ((pos[0] - piece_pos[0])**2 + (pos[1] - piece_pos[1])**2)**0.5
            
            if distance < 15:  # Click radius
                if self.dice_rolled and self.dice_value > 0:
                    self.selected_piece = i
                    self.move_piece(i)
                else:
                    self.message = "Roll the dice first!"
                return
        
        self.message = "Click on your piece to move it!"
    
    def _get_piece_screen_position(self, player, piece):
        """Get the screen position of a piece"""
        if piece.is_home:
            home_x = 60 + (piece.piece_id % 2) * 30
            home_y = 60 + (piece.piece_id // 2) * 30
            
            if player.player_id == 1:  # Player 2
                home_x = 680 + (piece.piece_id % 2) * 30
                home_y = 680 + (piece.piece_id // 2) * 30
            
            return (home_x, home_y)
        else:
            x = 50 + (piece.position % 17) * 40 + 20
            y = 50 + (piece.position // 17) * 40 + 20
            return (x, y)
    
    def update(self):
        """Update game state"""
        # Check for game over
        for player in self.players:
            if player.all_pieces_home() and not all(p.piece_id == -1 for p in player.pieces):
                if all(p.position == -1 for p in player.pieces):
                    self.game_over = True
                    self.message = f"🎉 {player.name} WINS! 🎉"
                    print(f"\n🎉 {player.name} WINS! 🎉")
    
    def draw(self, screen):
        """Draw the game"""
        self.board.draw(screen)
        
        # Draw all pieces
        for player in self.players:
            player.draw(screen, self.selected_piece if player == self.get_current_player() else None)
        
        # Draw dice value
        font = pygame.font.Font(None, 36)
        if self.dice_value > 0:
            dice_text = font.render(f"Dice: {self.dice_value}", True, (0, 0, 0))
            screen.blit(dice_text, (600, 50))
        
        # Draw current player
        current_text = font.render(f"Turn: {self.get_current_player().name}", True, self.get_current_player().color)
        screen.blit(current_text, (50, 50))
        
        # Draw messages
        small_font = pygame.font.Font(None, 20)
        message_text = small_font.render(self.message, True, (50, 50, 50))
        screen.blit(message_text, (50, 750))
        
        # Draw game over message
        if self.game_over:
            big_font = pygame.font.Font(None, 72)
            game_over_text = big_font.render(f"{self.get_current_player().name} WINS!", True, self.get_current_player().color)
            screen.blit(game_over_text, (150, 350))
