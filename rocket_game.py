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

    menu = True
    background_img=pygame.image.load("/Users/lp1/Desktop/project/rocket-game/images/background.jpeg")
    background_img=pygame.transform.scale( background_img , (width_screen , height_screen))

    Game_title_font = pygame.font.SysFont("impact", 60)
    menu_font = pygame.font.SysFont("impact", 40)
    select_options = ["Start New Game", "Settings", "Quit Game"]
    selected_index = 0
    
    while menu:
        # screen.fill((0, 0, 0))
        screen.blit(background_img , (0,0))
        # Render title - we keep it fixed and white

        game_title = Game_title_font.render("SPACE WAR", True, (255, 255, 255))
        game_title_rect = game_title.get_rect(center=(width_screen // 2, 100))
        screen.blit(game_title, game_title_rect)

        # Render options with highlighting
        for i, option_text in enumerate(select_options):
            if i == selected_index:
                color = (255, 255, 0)  # Yellow for selected
            else:
                color = (255, 255, 255)

            option_rendered = menu_font.render(option_text, True, color)
            option_rect = option_rendered.get_rect(center=(width_screen // 2, 200 + i * 60))
            screen.blit(option_rendered, option_rect)

        pygame.display.flip()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(select_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(select_options)
                elif event.key == pygame.K_RETURN:
                    return select_options[selected_index].lower()

def display_score(screen , font , score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over(screen , score):

    Game_over_font = pygame.font.SysFont("impact" , 60)
    screen.fill((0, 0, 0))

    Game_over_title=Game_over_font.render(f"GAME OVER", True , (255, 0 , 0))
    final_score_title=Game_over_font.render(f"FINAL SCORE: {score}" , True , (255, 255, 255))

    game_over_title_rect=Game_over_title.get_rect(center=(width_screen//2 , height_screen//2-50))
    final_score_title_rect=final_score_title.get_rect(center=(width_screen//2 , height_screen//2 + 10))
    screen.blit(final_score_title, final_score_title_rect)
    screen.blit(Game_over_title , game_over_title_rect )
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

def manage_enemy_collision(screen , Total_enemies , score , enemy_speed , enemy_rocket_img , bullets , rocket , running):
     
    for enemy in Total_enemies[:]:  # iterate safely
        rect = enemy["rect"]
        if enemy["type"] == "unpredictable":
            rect.x += enemy.get("dx", 0)
            rect.y += enemy_speed
            if random.randint(1, 10) == 5:
                enemy["dx"] = random.choice([-2, -1, 0, 1, 2])
            # Ensure it stays in bounds
            rect.x = max(0, min(width_screen - rect.width, rect.x))
        else:
            rect.y += enemy_speed

        screen.blit(enemy_rocket_img, rect)

        if rect.y >= height_screen:
            Total_enemies.remove(enemy)
            continue

        for bullet in bullets:
            if bullet.colliderect(rect):
                bullets.remove(bullet)
                Total_enemies.remove(enemy)
                score += 5
                break

        if rect.colliderect(rocket):
            running = False
            game_over(screen, score)

    return screen, Total_enemies, bullets, score, running

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

    background_img=pygame.image.load(os.path.join(file , "images" , "background.jpeg"))
    background_img=pygame.transform.scale(background_img , (width_screen , height_screen))

    rocket_img = pygame.image.load(os.path.join(file, "images", "spaceship.png"))
    rocket_img = pygame.transform.scale(rocket_img, (rocket_size, rocket_size))             # resize if needed

    enemy_rocket_img = pygame.image.load(os.path.join(file , "images", "enemy_rocket.png"))  # load image
    enemy_rocket_img = pygame.transform.scale(enemy_rocket_img, (enemy_size, enemy_size))  # resize if needed

    special_enemy_rocket_img=pygame.image.load(os.path.join(file , "images", "special_enemy.png"))
    special_enemy_rocket_img=pygame.transform.scale(special_enemy_rocket_img, (40,40) )

    while running:

        screen.blit(background_img , (0,0))
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
            enemy_rocket_x = random.randint(0, width_screen - rocket_size)
            enemy_rocket_y = 0
            enemy_rect = pygame.Rect(enemy_rocket_x, enemy_rocket_y, enemy_size, enemy_size)
            enemy_type = random.choice(["normal", "unpredictable"])
            
            if enemy_type == "unpredictable":
                enemy = {"rect": enemy_rect, "type": enemy_type, "dx": random.choice([-2, -1, 1, 2])}
            else:
                enemy = {"rect": enemy_rect, "type": enemy_type}
            Total_enemies.append(enemy)
  
        if random.randint(1,50) == 5 and score > 20 :

            special_enemy_rocket_x=random.randint( 0, width_screen-40)
            special_enemy_rocket_y=0
            special_enemy_rocket=pygame.Rect(special_enemy_rocket_x, special_enemy_rocket_y, 40,40)
            Total_special_enemies.append({"rect": special_enemy_rocket, "type": "special"})

        for special_enemy_rocket in Total_special_enemies[:]:

            if random.randint(1,100)== 10:
                enemy_bullet = pygame.Rect(special_enemy_rocket["rect"].centerx, special_enemy_rocket["rect"].bottom, 4, 5)
                Total_S_enemy_bullets.append(enemy_bullet)

            if  special_enemy_rocket["rect"].y >= height_screen:
                Total_special_enemies.remove(special_enemy_rocket)

        for enemy_bullets in Total_S_enemy_bullets[:] :
            enemy_bullets.y+=5.5
            pygame.draw.rect( screen , (255, 255, 255), enemy_bullets)
            
            if enemy_bullets.y >= height_screen :
                Total_S_enemy_bullets.remove(enemy_bullets)

            if enemy_bullets.colliderect(rocket):
                running=False
                game_over(screen , score)
        screen, Total_enemies, bullets, score, running = manage_enemy_collision(screen, Total_enemies, score, enemy_speed, enemy_rocket_img, bullets, rocket, running)
        # screen , Total_enemies , bullets , score , running  =manage_enemy_collision(screen , Total_enemies ,score, enemy_speed , enemy_rocket_img, bullets , rocket, running)
        screen , Total_special_enemies , bullets , score, running= manage_enemy_collision(screen , Total_special_enemies ,score, enemy_speed , special_enemy_rocket_img, bullets , rocket, running)
        
    
        #display score
        display_score(screen , font , score)
        pygame.display.flip()
        
def control(screen , font):
    control_menu=True
    selected_control_option=0
    title_font=pygame.font.SysFont("impact" , 60)
    while control_menu:

        screen.fill((0,0,0))
        rokcet_control_title=title_font.render("Rocket control" , True , (255, 0, 0))
        rokcet_control_title_rect=rokcet_control_title.get_rect(center=(width_screen//2 , 50))
        screen.blit(rokcet_control_title , rokcet_control_title_rect)

        controls=[ "ARROW KEY UP : MOVE UP" ,  "ARROW KEY DOWN : MOVE DOWN" ,
                   "ARROW KEY LEFT : MOVE LEFT" ,  "ARROW KEY RIGHT : MOVE RIGHT" , 
                   "SHOOT BULLET : SPACE" ,
                   "PAUSE : PRESS P" , 
                   "EXIT : ESCAPE" , 
                   "BACK TO SETTING"
                   ]

        for i , option in enumerate(controls):

            if i== selected_control_option:
                color = (255, 255 ,0)
            else :
                color = (255, 255 ,255)
            
            option_title= font.render( option , True , color)
            option_title_rect=option_title.get_rect(center=(width_screen//2 , 150+ i*50))
            screen.blit(option_title , option_title_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    selected_control_option= (selected_control_option-1) % len(controls)
                elif event.key == pygame.K_DOWN:
                    selected_control_option= (selected_control_option+1) % len(controls)
            
                elif event.key == pygame.K_RETURN:
                    
                    if selected_control_option==7:
                        return controls[selected_control_option]
                    
def setting(screen , font):

    setting_menu=True
    menu_font=pygame.font.SysFont("impact" , 40)
    Title_font=pygame.font.SysFont("impact" , 60)
    setting_list=["Sound Effects : ON" , "Controls" , "Back to main menu"]
    setting_selected_index=0
    Music_on=True

    while setting_menu:

        screen.fill((0, 0, 0))
        setting_title=Title_font.render("Setting" , True , (255,255, 255))
        setting_title_rect=setting_title.get_rect(center=(width_screen//2 , 100))
        screen.blit(setting_title , setting_title_rect)

        for i , option_selected in enumerate(setting_list):
            if i== setting_selected_index:
                color =(255, 255 ,0)  #yellow color 
            else:
                color = (255, 255, 255)
            
            option_title=menu_font.render(option_selected , True , color)
            option_title_rect=option_title.get_rect(center=(width_screen//2 , 200+ i*60))
            screen.blit(option_title , option_title_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE :
                    pygame.quit()
                    sys.exit()
                     
                if event.key == pygame.K_UP:
                    setting_selected_index=(setting_selected_index-1) % len(setting_list)
                elif event.key ==pygame.K_DOWN:
                    setting_selected_index= (setting_selected_index+1) % len(setting_list)

                elif event.key == pygame.K_RETURN :
                    Music_on = not Music_on
                    if setting_selected_index==0:
                        if Music_on:
                           setting_list[0]="Sound Effects : ON"
                        else:
                           setting_list[0]="Sound Effects : OFF"

                    elif setting_selected_index==1:
                        control(screen , font)

                    elif setting_selected_index==2:
                        
                        return setting_list[setting_selected_index]

    
def main():
    
    screen = screen_setup()
    font = pygame.font.SysFont("impact" , 30)

    while True:

        option=main_menu(screen , font)
        if option=="start new game":
            start_game()
        elif option=="quit game" :
            pygame.quit()

        elif option == "settings" :
            setting(screen , font)
            
            
main()