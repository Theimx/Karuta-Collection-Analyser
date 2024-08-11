import pygame
import random

pygame.init()


# Configuration
WIDTH, HEIGHT = 600, 600  
ROWS, COLS = 30, 30  
CUBE_SIZE = WIDTH // COLS 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_grid(win, text_grid):
    for row in range(ROWS):
        for col in range(COLS):
            if text_grid[row][col] == 'X':
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(win, color, (col * CUBE_SIZE, row * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
            pygame.draw.rect(win, BLACK, (col * CUBE_SIZE, row * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), 1)

def createWorld(text_grid):
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("World Grid Simulation")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        win.fill(WHITE)
        draw_grid(win, text_grid)
        pygame.display.flip()
        clock.tick(60)

class Mouse:
    def __init__(self, mouse_id):
        self.max_speed = random.uniform(-1.7, 1.7)  # Vitesse maximale aléatoire entre -1.7 et 1.7
        self.current_speed = 0.0  # Vitesse actuelle initialisée à 0
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )  # Couleur aléatoire
        self.direction = random.choice([-1, 1])  # Direction aléatoire, -1 pour gauche, 1 pour droite
        self.id = mouse_id  # ID de la souris, donné par l'utilisateur

    def __str__(self):
        return f"Mouse(ID={self.id}, Max Speed={self.max_speed}, Current Speed={self.current_speed}, Color={self.color}, Direction={'Left' if self.direction == -1 else 'Right'})"


text_grid = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

createWorld(text_grid)

# Exemple de création de souris
mouse1 = Mouse(1)
mouse2 = Mouse(2)

print(mouse1)
print(mouse2)
