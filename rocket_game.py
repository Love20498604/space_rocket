import pygame
import sys
import random
import os

def screen_setup():

    pygame.init()
    pygame.font.init()
    global width_screen , height_screen
    width_screen , height_screen = 800 , 600
    screen = pygame.display.set_mode((width_screen, height_screen))
    pygame.display.set_caption("SPACE WAR")
    return screen 

def main_menu(screen, font):
    menu=True
    Game_title_font=pygame.font.SysFont("impact" , 60)
    menu_font=pygame.font.SysFont("impact", 40)
    select_option=["start new game" , "quit game"]
    while menu :

        screen.fill((0, 0, 0))
        
        Game_title=Game_title_font.render("SPACE WAR" , True , (255, 255, 255))
        start_new_game=menu_font.render("Start New Game" , True , (255, 255, 255))
        quit_game=menu_font.render("Quit", True , (255, 255, 255))

        game_title_rect=Game_title.get_rect(center=(width_screen // 2, 30  ))
        start_new_game_rect=start_new_game.get_rect(center=(width_screen//2 , 200))
        quit_game_rect=quit_game.get_rect(center=(width_screen//2 , 300))
        screen.blit(Game_title , game_title_rect) 
        screen.blit(start_new_game , start_new_game_rect)
        screen.blit(quit_game , quit_game_rect)
        pygame.display.flip()

        events=pygame.event.get()
        for event in events:
            if event.type== pygame.QUIT :
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RETURN :
                    option=select_option[0]
                    return option
                
                elif event.key == pygame.K_q :
                    option=select_option[1]
            
                    return option

def display_score(screen , font , score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    

def game_over(screen , score):

    font = pygame.font.SysFont("impact" , 30)
    screen.fill((0, 0, 0))
    Game_over=font.render(f"GAME OVER", True , (255, 255, 255))
    final_score=font.render(f"FINAL SCORE: {score}", True , (255, 255, 255))
    screen.blit(final_score, ( width_screen//2 -100 ,height_screen//2 ))
    screen.blit(Game_over ,( (width_screen//2 -100) , height_screen//2-40 ) )
    pygame.display.flip()
    pygame.time.wait(5000)
    

def update_speed_enemy(score , enemy_speed):

    if score > 40 :
        enemy_speed = 2.5
    if score> 90:
        enemy_speed = 3.5
    if score > 140:
        enemy_speed = 4
    return enemy_speed

def manage_enemy_collision(screen , Total_enemies ,score, enemy_speed , enemy_rocket_img, bullets , rocket , running):
     
    for enemy_rocket in Total_enemies:

        enemy_rocket.y += enemy_speed
        screen.blit(enemy_rocket_img, enemy_rocket)

        if enemy_rocket.y >= height_screen:
            Total_enemies.remove(enemy_rocket)
            continue

        for bullet in bullets:
            if bullet.colliderect(enemy_rocket) :
                bullets.remove(bullet)
                Total_enemies.remove(enemy_rocket)
                score += 5
                break
        
        # for enemy_rock in Total_enemies:
        if enemy_rocket.colliderect(rocket) :
                running=False
                game_over(screen, score)
                    
    return screen , Total_enemies , bullets , score , running


def start_game():

    clock = pygame.time.Clock()
    screen = screen_setup()
    font = pygame.font.SysFont("impact" , 30)
    score = 0
    
    rocket_x_cordinate = width_screen // 2
    rocket_y_cordinate = height_screen // 2

    
    pause=False
    running = True
    enemy_size , rocket_size = 40 , 60 
    Total_enemies , Total_special_enemies ,  bullets , Total_S_enemy_bullets = [] , [] , [] , []
    enemy_speed , move = 1.5 , 7
   
    file_path="/Users/lp1/Desktop/project/rocket-game/rocket_game.py"
    file=os.path.dirname(file_path)

    rocket_img = pygame.image.load(os.path.join(file, "images", "spaceship.png"))
    rocket_img = pygame.transform.scale(rocket_img, (rocket_size, rocket_size))             # resize if needed

    enemy_rocket_img = pygame.image.load(os.path.join(file , "images", "enemy_rocket.png"))  # load image
    enemy_rocket_img = pygame.transform.scale(enemy_rocket_img, (enemy_size, enemy_size))  # resize if needed

    special_enemy_rocket_img=pygame.image.load(os.path.join(file , "images", "special_enemy.png"))
    special_enemy_rocket_img=pygame.transform.scale(special_enemy_rocket_img, (40,40) )

    while running:

        screen.fill((0, 0, 0))
        clock.tick(60)
    
        events = pygame.event.get()
        for event in events:
            if event.type== pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key ==pygame.K_p:
                    pause= True

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
    

        for bullet in bullets:  # Use a slice copy to avoid iteration issues
            bullet.y -= 10
            pygame.draw.rect(screen , (255, 255, 255), bullet)

            if bullet.y <= 0:
                bullets.remove(bullet)

        enemy_speed=update_speed_enemy(score, enemy_speed)

        if random.randint(1, 50) == 5:

            enemy_rocket_x=random.randint(0, width_screen - rocket_size)
            enemy_rocket_y=0
            enemy_rocket=pygame.Rect(enemy_rocket_x, enemy_rocket_y, enemy_size, enemy_size)
            Total_enemies.append(enemy_rocket)
        
        if random.randint(1,50) == 5 and score > 20 :

            special_enemy_rocket_x=random.randint( 0, width_screen-40)
            special_enemy_rocket_y=0
            special_enemy_rocket=pygame.Rect(special_enemy_rocket_x, special_enemy_rocket_y, 40,40)
            Total_special_enemies.append(special_enemy_rocket)

        for special_enemy_rocket in Total_special_enemies[:]:

            if random.randint(1,100)== 10:
                enemy_bullet=pygame.Rect(special_enemy_rocket.centerx , special_enemy_rocket.bottom , 4 , 5)
                Total_S_enemy_bullets.append(enemy_bullet)

            if special_enemy_rocket.y >= height_screen:
                Total_special_enemies.remove(special_enemy_rocket)

        for enemy_bullets in Total_S_enemy_bullets[:] :
            enemy_bullets.y+=5.5
            pygame.draw.rect( screen , (255, 255, 255), enemy_bullets)
            
            if enemy_bullets.y >= height_screen :
                Total_S_enemy_bullets.remove(enemy_bullets)

            if enemy_bullets.colliderect(rocket):
                running=False
                game_over(screen , score)

        screen , Total_enemies , bullets , score , running  =manage_enemy_collision(screen , Total_enemies ,score, enemy_speed , enemy_rocket_img, bullets , rocket, running)
        screen , Total_special_enemies , bullets , score, running= manage_enemy_collision(screen , Total_special_enemies ,score, enemy_speed , special_enemy_rocket_img, bullets , rocket, running)
        
    
        #display score
        display_score(screen , font , score)
        pygame.display.flip()
        
    

def main():
    
    screen = screen_setup()
    font = pygame.font.SysFont("impact" , 30)
    
    
    while True:
        
        option=main_menu(screen , font)
        if option=="start new game":
            start_game()
        elif option=="quit game" :
            pygame.quit()

        
main()