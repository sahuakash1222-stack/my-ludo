import pygame

class Piece:
    def __init__(self, player_id, piece_id, color):
        self.player_id = player_id
        self.piece_id = piece_id
        self.color = color
        self.position = -1  # -1 means in home, 0-51 is board position
        self.is_home = True
        self.radius = 8
    
    def move(self, steps):
        """Move piece forward by steps"""
        if self.is_home and steps > 0:
            self.is_home = False
            self.position = 0
        else:
            self.position += steps
        
        # Check if reached home (position 52+)
        if self.position >= 52:
            self.is_home = True
            self.position = -1
    
    def draw(self, screen, x, y):
        """Draw the piece"""
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), self.radius, 2)


class Player:
    def __init__(self, player_id, name, color):
        self.player_id = player_id
        self.name = name
        self.color = color
        self.pieces = [
            Piece(player_id, 0, color),
            Piece(player_id, 1, color),
            Piece(player_id, 2, color),
            Piece(player_id, 3, color)
        ]
        self.score = 0
    
    def move_piece(self, piece_index, steps):
        """Move a specific piece"""
        if 0 <= piece_index < len(self.pieces):
            self.pieces[piece_index].move(steps)
            return True
        return False
    
    def all_pieces_home(self):
        """Check if all pieces are home (finished)"""
        return all(piece.is_home for piece in self.pieces)
    
    def get_available_moves(self):
        """Get list of pieces that can be moved"""
        available = []
        for i, piece in enumerate(self.pieces):
            if not piece.is_home or True:  # Can always try to move
                available.append(i)
        return available
    
    def draw(self, screen):
        """Draw all pieces for this player"""
        for piece in self.pieces:
            if piece.is_home:
                # Draw in home area
                home_x = 60 + (piece.piece_id % 2) * 30
                home_y = 60 + (piece.piece_id // 2) * 30
                
                if self.player_id == 1:  # Player 2
                    home_x = 680 + (piece.piece_id % 2) * 30
                    home_y = 680 + (piece.piece_id // 2) * 30
                
                piece.draw(screen, home_x, home_y)
            else:
                # Draw on board
                x = 50 + (piece.position % 17) * 40 + 20
                y = 50 + (piece.position // 17) * 40 + 20
                piece.draw(screen, x, y)
