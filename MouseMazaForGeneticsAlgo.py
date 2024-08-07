import pygame
import sys
import math

# Initialisation de PyGame
pygame.init()

# Définir les dimensions de la fenêtre et des cubes
WIDTH, HEIGHT = 600, 600  # Taille de la fenêtre
ROWS, COLS = 30, 30  # Nombre de lignes et colonnes
CUBE_SIZE = WIDTH // COLS  # Taille de chaque cube

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Créer la fenêtre
win = pygame.display.set_mode((WIDTH, HEIGHT),pygame.NOFRAME)
pygame.display.set_caption("Mouse and Borders Simulation")

# Grille textuelle
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
    "X##########XXXXXX############X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "X############################X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

class Border:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CUBE_SIZE, CUBE_SIZE)

    def draw(self, win):
        pygame.draw.rect(win, BLACK, self.rect)

class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0  # Vitesse initiale
        self.direction = 0  # Angle en degrés
        self.radius = 5

    def update(self, accel, turn):
        # Update speed and direction
        self.speed += accel
        self.speed = max(-1, min(1, self.speed))  # Limiter la vitesse entre -1 et 1
        self.direction += turn
        rad = math.radians(self.direction)

        # Update position
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)  # y-axis is inverted in pygame

        # Keep mouse within window bounds
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

def draw_grid(win, text_grid):
    for row in range(ROWS):
        for col in range(COLS):
            if text_grid[row][col] == 'X':
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(win, color, (col * CUBE_SIZE, row * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
            pygame.draw.rect(win, BLACK, (col * CUBE_SIZE, row * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), 1)

def main():
    clock = pygame.time.Clock()
    mouse = Mouse(WIDTH // 2, HEIGHT // 2)
    borders = []

    # Créer les objets Border en fonction de la grille textuelle
    for row in range(ROWS):
        for col in range(COLS):
            if text_grid[row][col] == 'X':
                borders.append(Border(col * CUBE_SIZE, row * CUBE_SIZE))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gestion des touches
        keys = pygame.key.get_pressed()
        accel = 0
        turn = 0
        if keys[pygame.K_UP]:
            accel = 0.1
        elif keys[pygame.K_DOWN]:
            accel = -0.1
        if keys[pygame.K_LEFT]:
            turn = 2
        elif keys[pygame.K_RIGHT]:
            turn = -2

        # Mettre à jour la souris
        mouse.update(accel, turn)

        # Vérifier les collisions
        mouse_rect = mouse.get_rect()
        for border in borders:
            if mouse_rect.colliderect(border.rect):
                print("Collision detected!")
                # Réinitialiser la position de la souris pour simplifier la gestion des collisions
                mouse.x, mouse.y = WIDTH // 2, HEIGHT // 2
                mouse.speed = 0
                mouse.direction = 0

        # Dessiner la grille, les bordures et la souris
        win.fill(WHITE)
        draw_grid(win, text_grid)
        for border in borders:
            border.draw(win)
        mouse.draw(win)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
