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

def display_score(screen , font , score):
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
def game_over(screen , font , score):
    
    screen.fill((0, 0, 0))
    final_score=font.render(f"FINAL SCORE: {score}", True , (255, 255, 255))
    screen.blit(final_score, ( width_screen//2 -100 ,height_screen//2 ))
    pygame.display.flip()
    pygame.time.wait(3000)
    

def main():

    
    clock = pygame.time.Clock()
    screen = screen_setup()
    rocket_size = 75
    rocket_x_cordinate = width_screen // 2
    rocket_y_cordinate = height_screen // 2

    move = 7
    pause=False
    running = True
    enemy_size = 40
    Total_enemies = []
    bullets = []

    # Initialize font and score
    font = pygame.font.SysFont("impact" , 30)
    score = 0

    rocket_img = pygame.image.load("//Users/lp1/Desktop/project/rocket-game/space_rocket/images/spaceship.png")  # load image
    rocket_img = pygame.transform.scale(rocket_img, (rocket_size, rocket_size))  # resize if needed

    enemy_rocket_img = pygame.image.load("/Users/lp1/Desktop/project/rocket-game/enemy_rocket.png")  # load image
    enemy_rocket_img = pygame.transform.scale(enemy_rocket_img, (enemy_size, enemy_size))  # resize if needed

    while running:

        screen.fill((0, 0, 0))
        clock.tick(60)
    
        events = pygame.event.get()
        for event in events:
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key ==pygame.K_p:
                    pause= not pause

        if pause:
            pause_text= font.render("Game Paused - Press P To Resume Game", True , (255, 255, 255))
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(pause_text, (200,300))
            screen.blit(score_text, (10, 10))
            pygame.display.flip()
            continue

        rocket=screen.blit(rocket_img, (rocket_x_cordinate, rocket_y_cordinate))  # draw on screen

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
        if random.randint(1, 50) == 1:
            enemy_rocket_x=random.randint(0, width_screen - rocket_size)
            enemy_rocket_y=0
            enemy_rocket=pygame.Rect(enemy_rocket_x, enemy_rocket_y, enemy_size, enemy_size)
            Total_enemies.append(enemy_rocket)
            


        for enemy_rocket in Total_enemies:
            enemy_rocket.y += 1.5
            screen.blit(enemy_rocket_img, enemy_rocket)


            if enemy_rocket_y >= height_screen:
                Total_enemies.remove(enemy_rocket)
                continue

            for bullet in bullets:
                if bullet.colliderect(enemy_rocket):
                    bullets.remove(bullet)
                    Total_enemies.remove(enemy_rocket)
                    score += 1
                    break
            
            for enemy_rock in Total_enemies:
                if enemy_rock.colliderect(rocket) :
                    running = False
                   
        #display score
        display_score(screen , font , score)
        pygame.display.flip()

    game_over(screen , font , score)
    pygame.quit()

main()
