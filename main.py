import pygame
import random
import time

import pygame.time

from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_p

pygame.init()


FPS = pygame.time.Clock()

#розміри вікна
HEIGHT = 800
WIDHT = 1200

FONT = pygame.font.SysFont('Verdana', 20)
FONT_TEXT = pygame.font.SysFont('Verdana', 20)
EXIT = pygame.font.SysFont('Verdana', 60)
LIFE = pygame.font.SysFont('Verdana', 20)
HEART = pygame.transform.scale(pygame.image.load('d:/Python_Game/hear.png'), (40, 40))



#кольори
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

main_display = pygame.display.set_mode((WIDHT, HEIGHT))


bg = pygame.transform.scale(pygame.image.load('d:/Python_Game/background.png'), (WIDHT, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

#налаштування гравця
player_size = (120, 60)   #розміри
player = pygame.transform.scale(pygame.image.load('d:/Python_Game/player.png').convert_alpha(), player_size)
player_rect = player.get_rect()  # розміщення

#рух гравця
player_move_down = [0, 2]  
player_move_up = [0, -2]
player_move_left = [-1, 0]
player_move_right = [4, 0]


#функція ворог
def create_enemy():
    enemy_size = (100, 50)
    enemy = pygame.transform.scale(pygame.image.load('d:/Python_Game/enemy.png').convert_alpha(), enemy_size)
    enemy_rect = pygame.Rect(WIDHT, random.randint(100, HEIGHT - 100), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


#періодичність надходження ворогів
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)


#функція бонуси
def create_bonus():
    bonus_size = (100, 180)
    bonus = pygame.transform.scale(pygame.image.load('d:/Python_Game/bonus.png').convert_alpha(), bonus_size)
    bonus_rect = pygame.Rect(random.randint(300, WIDHT - 200), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 4)]
    return [bonus, bonus_rect, bonus_move]


#періодичність надходження бонусів
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

def create_bonus_medicine():
    bonus_medicine_size = (80, 80)
    bonus_medicine = pygame.transform.scale(pygame.image.load('d:/Python_Game/medical.png').convert_alpha(), bonus_medicine_size)
    bonus_medicine_rect = pygame.Rect(random.randint(300, WIDHT - 200), 0, *bonus_medicine_size)
    bonus_medicine_move = [0, random.randint(1, 4)]
    return [bonus_medicine, bonus_medicine_rect, bonus_medicine_move]

#періодичність надходження бонусів
CREATE_BONUS_MEDICINE = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_BONUS_MEDICINE, 9000)




GAME_EVENT = pygame.USEREVENT + 4





exit = 0
enemies = []
bonuses = []
bonuses_medicine = []
menu = []
score = 0
player_lives = 3


playing = True


while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_BONUS_MEDICINE:
            bonuses_medicine.append(create_bonus_medicine())
        if event.type == GAME_EVENT:
            playing = False


    bg_X1 -= bg_move
    bg_X2 -= bg_move


    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))


    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDHT:
        player_rect = player_rect.move(player_move_right)



    #показ елементів гри
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            player_lives -= 1
            enemies.pop(enemies.index(enemy)) 

            if player_lives == 0:
                pygame.time.set_timer(GAME_EVENT, 2000)
                main_display.blit(EXIT.render("GAME OVER", True, COLOR_BLACK), (WIDHT/2 - 170, HEIGHT/2 - 30))
                main_display.blit(EXIT.render(str("Score"), True, COLOR_BLACK), (WIDHT/2 - 100, HEIGHT/2 + 30))
                main_display.blit(EXIT.render(str(score), True, COLOR_BLACK), (WIDHT/2 + 100, HEIGHT/2 + 30))
                pygame.display.flip()
                time.sleep(5)
                break



    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus)) 

    for bonus_medicine in bonuses_medicine:
        bonus_medicine[1] = bonus_medicine[1].move(bonus_medicine[2])
        main_display.blit(bonus_medicine[0], bonus_medicine[1])

        if player_rect.colliderect(bonus_medicine[1]):
            if (player_lives == 3):
                player_lives += 0
            else:
                player_lives += 1
            bonuses_medicine.pop(bonuses_medicine.index(bonus_medicine))        


    main_display.blit(FONT_TEXT.render(str("Score"), True, COLOR_BLACK), (WIDHT-120, 20))
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDHT-50, 20))
    
    for i in range(1, player_lives + 1):
        main_display.blit(HEART, (WIDHT - (i * 50), 50))





    main_display.blit(player, player_rect)

    pygame.display.flip()
    
    #видалення елементів
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

    for bonus_medicine in bonuses_medicine:
        if bonus_medicine[1].top > HEIGHT:
            bonuses_medicine.pop(bonuses_medicine.index(bonus_medicine))




