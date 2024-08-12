import pygame
import sys
import math
import random

# Dimensions de la fenêtre et de la grille
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
CUBE_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Classe pour gérer les bordures
class Border:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CUBE_SIZE, CUBE_SIZE)

    def draw(self, win):
        pygame.draw.rect(win, BLACK, self.rect)

# Classe pour gérer les objets Mouse
class Mouse:
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.max_speed = random.uniform(-1.7, 1.7)
        self.current_speed = 0.0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.direction = 0  # -1 pour gauche, 1 pour droite
        self.radius = 5
        self.ID = ID

    def update(self, accel, turn):
        # Mise à jour de la vitesse et de la direction
        self.current_speed += accel
        self.current_speed = max(-1.7, min(1.7, self.current_speed))
        self.direction += turn
        rad = math.radians(self.direction)

        # Mise à jour de la position
        self.x += self.current_speed * math.cos(rad)
        self.y -= self.current_speed * math.sin(rad)

        # Garder la souris dans les limites de la fenêtre
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def cast_rays(self, borders, win):
        ray_count = 5  # Nombre de rayons
        ray_length = 1000  # Longueur maximale du rayon
        angles = [self.direction + i * (360 / ray_count) for i in range(ray_count)]  # Angles des rayons
        distances = []

        for angle in angles:
            rad = math.radians(angle)
            end_x = self.x + ray_length * math.cos(rad)
            end_y = self.y - ray_length * math.sin(rad)
            closest_dist = ray_length

            for border in borders:
                hit_point = self.ray_intersect((self.x, self.y), (end_x, end_y), border.rect)
                if hit_point:
                    dist = math.sqrt((hit_point[0] - self.x) ** 2 + (hit_point[1] - self.y) ** 2)
                    if dist < closest_dist:
                        closest_dist = dist

            distances.append(int(closest_dist))  # Arrondir la distance à un entier

            # Dessiner le rayon en rouge
            pygame.draw.line(win, RED, (self.x, self.y), (self.x + closest_dist * math.cos(rad), self.y - closest_dist * math.sin(rad)))

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

# Fonction pour dessiner la grille
def draw_grid(win, text_grid):
    for row in range(ROWS):
        for col in range(COLS):
            if text_grid[row][col] == 'X':
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(win, color, (col * CUBE_SIZE, row * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
            pygame.draw.rect(win, BLACK, (col * CUBE_SIZE, row * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), 1)

# Fonction pour créer le monde Pygame à partir d'une grille textuelle
def createWorld(text_grid):
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("World Simulation")

    borders = []
    for row in range(ROWS):
        for col in range(COLS):
            if text_grid[row][col] == 'X':
                borders.append(Border(col * CUBE_SIZE, row * CUBE_SIZE))

    return win, borders

# Boucle principale pour l'exécution du programme
def main():
    text_grid = [
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X      XXXXXXXXXXXXXXXX      X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X      XXXXXXXXXXXXXXXX      X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "X                            X",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ]

    win, borders = createWorld(text_grid)
    mouse = Mouse(WIDTH // 2, HEIGHT // 2, ID=1)
    clock = pygame.time.Clock()

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

        # Mise à jour de la souris
        mouse.update(accel, turn)

        # Vérification des collisions
        mouse_rect = mouse.get_rect()
        for border in borders:
            if mouse_rect.colliderect(border.rect):
                print("Collision detected!")
                # Réinitialiser la position de la souris
                mouse.x, mouse.y = WIDTH // 2, HEIGHT // 2
                mouse.current_speed = 0
                mouse.direction = 0

        # Ray tracing pour détecter les murs
        distances = mouse.cast_rays(borders, win)
        print("Distances des murs:", distances)

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

