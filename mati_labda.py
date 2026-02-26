import pygame
import random

# Inicializálás
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pöttyös Labda Játék")

# Színek
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Labda beállításai
ball_radius = 30
ball_x = WIDTH // 2
ball_y = ball_radius + 20
velocity_y = 0
gravity = 0.5
bounce_factor = -0.9  # Mennyire pattanjon vissza

score = 0
font = pygame.font.SysFont("Arial", 24)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((135, 206, 235))  # Égszínkék háttér
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Távolság számítása a klikk és a labda közepe között
            dist = ((mouse_pos[0] - ball_x)**2 + (mouse_pos[1] - ball_y)**2)**0.5
            
            if dist <= ball_radius:
                score += 1
                velocity_y = 10  # Meglökjük lefelé
            else:
                # Ha mellékattintasz (vagy nem találod el a mozgó labdát)
                score -= 1

    # Fizika: Gravitáció és mozgás
    velocity_y += gravity
    ball_y += velocity_y

    # Földet érés vizsgálata
    if ball_y + ball_radius >= HEIGHT:
        ball_y = HEIGHT - ball_radius
        velocity_y *= bounce_factor
        
        # Ha a labda megállna vagy nagyon kicsit pattan, adjunk neki egy kis löketet
        if abs(velocity_y) < 2:
            velocity_y = -12
            score -= 1 # Levonunk pontot, mert leért anélkül, hogy elkaptad volna

    # Labda kirajzolása (Piros alap)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    # Fehér pöttyök
    pygame.draw.circle(screen, WHITE, (int(ball_x-10), int(ball_y-10)), 5)
    pygame.draw.circle(screen, WHITE, (int(ball_x+12), int(ball_y-5)), 4)
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y+12)), 6)
    pygame.draw.circle(screen, WHITE, (int(ball_x-5), int(ball_y+2)), 3)

    # Pontszám kiírása
    score_text = font.render(f"Pontszám: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
