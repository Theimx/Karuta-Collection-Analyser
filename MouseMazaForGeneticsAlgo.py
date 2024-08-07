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
win = pygame.display.set_mode((WIDTH, HEIGHT))
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
    "X############################X",
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
        self.has_moved = False  # Indicateur si la souris a bougé

    def update(self, accel, turn):
        # Update speed and direction
        self.speed += accel
        self.speed = max(-1, min(1, self.speed))  # Limiter la vitesse entre -1 et 1
        self.direction += turn
        rad = math.radians(self.direction)

        # Update position
        new_x = self.x + self.speed * math.cos(rad)
        new_y = self.y - self.speed * math.sin(rad)  # y-axis is inverted in pygame

        # Check if the mouse has moved
        if not self.has_moved and (new_x != self.x or new_y != self.y):
            self.has_moved = True

        if self.has_moved:
            self.x = new_x
            self.y = new_y

        # Keep mouse within window bounds
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def cast_rays(self, borders):
        if not self.has_moved:
            return []

        ray_count = 8
        ray_length = 1000
        angles = [2 * math.pi * i / ray_count for i in range(ray_count)]
        distances = []

        for angle in angles:
            end_x = self.x + ray_length * math.cos(angle)
            end_y = self.y - ray_length * math.sin(angle)
            closest_dist = ray_length

            for border in borders:
                hit_point = self.ray_intersect((self.x, self.y), (end_x, end_y), border.rect)
                if hit_point:
                    dist = math.sqrt((hit_point[0] - self.x) ** 2 + (hit_point[1] - self.y) ** 2)
                    if dist < closest_dist:
                        closest_dist = dist

            # Round the distance to 3 decimal places
            distances.append(round(closest_dist, 3))

            # Dessiner le rayon en rouge
            pygame.draw.line(win, RED, (self.x, self.y), (self.x + closest_dist * math.cos(angle), self.y - closest_dist * math.sin(angle)))

        return distances

    def ray_intersect(self, start, end, rect):
        x1, y1 = start
        x2, y2 = end
        x3, y3 = rect.topleft
        x4, y4 = rect.topright
        x5, y5 = rect.bottomright
        x6, y6 = rect.bottomleft

        intersects = []
        lines = [((x3, y3), (x4, y4)), ((x4, y4), (x5, y5)), ((x5, y5), (x6, y6)), ((x6, y6), (x3, y3))]
        for (x3, y3), (x4, y4) in lines:
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom == 0:
                continue
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
            if 0 <= t <= 1 and 0 <= u <= 1:
                intersects.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))

        if intersects:
            return min(intersects, key=lambda point: (point[0] - x1) ** 2 + (point[1] - y1) ** 2)
        return None

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
                mouse.has_moved = False

        # Raycasting
        distances = mouse.cast_rays(borders)
        print(distances)

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
