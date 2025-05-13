import pygame
import sys
import random
pygame.init()
pygame.font.init()


def screen_setup():
    global width_screen , height_screen
    width_screen , height_screen = 800 , 600
    screen = pygame.display.set_mode((width_screen, height_screen))
    return screen 



def main():
    Time_IN=pygame.time.get_ticks()
    clock = pygame.time.Clock()
    screen = screen_setup()
    rocket_color = (255, 0, 0)
    rocket_size = 50
    rocket_x_cordinate = width_screen // 2
    rocket_y_cordinate = height_screen // 2

    move = 10
    running = True
    enemy_size = 40
    Total_enemies = []
    bullets = []

    # Initialize font and score
    font = pygame.font.SysFont(None , 30)
    score = 0

    while running:
        screen.fill((0, 0, 0))
        clock.tick(60)
        Time_out=pygame.time.get_ticks()
        Time_difference=Time_out - Time_IN
        rocket = pygame.draw.rect(screen, rocket_color, (rocket_x_cordinate, rocket_y_cordinate, rocket_size, rocket_size))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (Time_difference//1000 >= 10) :
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and rocket_x_cordinate >= 0:
            rocket_x_cordinate -= move
        if keys[pygame.K_RIGHT] and rocket_x_cordinate < (width_screen - rocket_size):
            rocket_x_cordinate += move
        if keys[pygame.K_UP] and rocket_y_cordinate > 0:
            rocket_y_cordinate -= move
        if keys[pygame.K_DOWN] and rocket_y_cordinate < height_screen - rocket_size:
            rocket_y_cordinate += move
        if keys[pygame.K_SPACE]:
            if len(bullets) < 10:
                bullet = pygame.Rect(rocket.centerx, rocket.top, 4, 5)
                bullets.append(bullet)

        for bullet in bullets[:]:  # Use a slice copy to avoid iteration issues
            bullet.y -= 10
            pygame.draw.rect(screen, (255, 255, 255), bullet)

            if bullet.y <= 0:
                bullets.remove(bullet)

        # Generate enemy rocks
        if random.randint(1, 30) == 1:
            enemy_rock_x = random.randint(0, width_screen - rocket_size)
            enemy_rock = pygame.Rect(enemy_rock_x, 0, enemy_size, enemy_size)
            Total_enemies.append(enemy_rock)

        for enemy_rock in Total_enemies[:]:
            enemy_rock.y += 1.5
            pygame.draw.rect(screen, (0, 255, 0), enemy_rock)

            if enemy_rock.y >= height_screen:
                Total_enemies.remove(enemy_rock)
                continue

            for bullet in bullets[:]:
                if bullet.colliderect(enemy_rock):
                    bullets.remove(bullet)
                    Total_enemies.remove(enemy_rock)
                    score += 1
                    break

        # Render and display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


main()
