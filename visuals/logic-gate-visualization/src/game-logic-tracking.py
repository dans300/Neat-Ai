import pygame
import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class LogicState:
    matrix: List[List[int]]
    commands: List[str]
    timestamp: str

class LogicStateTracker:
    def __init__(self):
        self.states: List[LogicState] = []
        self.load_states()
    
    def add_state(self, matrix, commands):
        state = LogicState(
            matrix=matrix,
            commands=commands,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.states.append(state)
        self.save_states()
    
    def load_states(self):
        try:
            with open('logic_states.json', 'r') as f:
                data = json.load(f)
                self.states = [LogicState(**state) for state in data]
        except FileNotFoundError:
            self.states = []
    
    def save_states(self):
        with open('logic_states.json', 'w') as f:
            json.dump([state.__dict__ for state in self.states], f, indent=2)

    def draw_visualization(self, screen, start_y):
        CELL_SIZE = 30
        GATE_WIDTH = 60
        GATE_HEIGHT = 40
        
        for state_idx, state in enumerate(self.states[-5:]):  # Show last 5 states
            y_offset = start_y + (state_idx * 150)
            
            # Draw matrix
            for row_idx, row in enumerate(state.matrix):
                for col_idx, cell in enumerate(row):
                    x = 50 + (col_idx * CELL_SIZE)
                    y = y_offset + (row_idx * CELL_SIZE)
                    color = (0, 100, 200) if cell == 1 else (40, 40, 50)
                    pygame.draw.rect(screen, color, (x, y, CELL_SIZE-2, CELL_SIZE-2))
            
            # Draw AND gate
            gate_x = 250
            gate_y = y_offset + 20
            
            # Draw gate body
            pygame.draw.arc(screen, (255, 255, 255), 
                          (gate_x, gate_y, GATE_WIDTH, GATE_HEIGHT),
                          0, 3.14159, 2)
            pygame.draw.line(screen, (255, 255, 255),
                           (gate_x, gate_y),
                           (gate_x, gate_y + GATE_HEIGHT), 2)
            
            # Connect 1s to gate inputs
            ones_positions = [(row_idx, col_idx) 
                            for row_idx, row in enumerate(state.matrix)
                            for col_idx, cell in enumerate(row) if cell == 1]
            
            for idx, (row, col) in enumerate(ones_positions):
                start_x = 50 + (col * CELL_SIZE) + CELL_SIZE//2
                start_y = y_offset + (row * CELL_SIZE) + CELL_SIZE//2
                end_x = gate_x
                end_y = gate_y + (idx * 10)
                pygame.draw.line(screen, (255, 255, 255),
                               (start_x, start_y), (end_x, end_y), 2)
            
            # Draw commands and connect to gate output
            for cmd_idx, cmd in enumerate(state.commands):
                cmd_x = gate_x + GATE_WIDTH + 50
                cmd_y = y_offset + (cmd_idx * 30)
                
                # Command box
                pygame.draw.rect(screen, (60, 60, 70),
                               (cmd_x, cmd_y, 80, 25))
                
                # Command text
                font = pygame.font.Font(None, 24)
                text = font.render(cmd, True, (255, 255, 255))
                screen.blit(text, (cmd_x + 10, cmd_y + 5))
                
                # Connect gate to command
                pygame.draw.line(screen, (255, 255, 255),
                               (gate_x + GATE_WIDTH, gate_y + GATE_HEIGHT//2),
                               (cmd_x, cmd_y + 12), 2)

# In your main game code, create the tracker
logic_tracker = LogicStateTracker()

# In your game loop, update the tracker
def blue_player_logic(game_matrix):
    # Your existing logic here
    
    # Add state to tracker
    logic_tracker.add_state(blue_last_state, blue_last_action)
    
    # In your draw function, add the visualization
    logic_tracker.draw_visualization(screen, HEIGHT - 200)
