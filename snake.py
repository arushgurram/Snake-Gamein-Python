import pygame
import random
import os
import sys
from sys import exit

#GAME VARIABLES
TILE_SIZE = 25
ROWS = 27
COLUMNS = 27
WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

#IMPORTING FILES AND ATTACHING THEM TO APPLICATION
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#LOADING IMAGES
def load_image(image_name,scale=None) :
    full_path = resource_path(image_name)
    image = pygame.image.load(full_path)

    if scale is not None :
       image = pygame.transform.scale(image,scale)

    return image 

snake_image = load_image("snake-png.png",(TILE_SIZE*5,TILE_SIZE*5))

#WINDOW INITIALZATION
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("SNAKE GAME")
pygame.display.set_icon(snake_image)
clock = pygame.time.Clock()

#GENERATING RANDOM POSITIONS
def generate_random(limit) :
    return random.randint(0,limit - 1) * TILE_SIZE

#GAME
food = pygame.Rect(generate_random(COLUMNS),generate_random(ROWS),TILE_SIZE,TILE_SIZE)
snake = []
snake.append(pygame.Rect(generate_random(COLUMNS),generate_random(ROWS),TILE_SIZE,TILE_SIZE))
snake_velocity = (0,0)
paused = False
score = 0

#DRAWING ITEMS TO WINDOW
def display() :
    window.fill("black")

    pygame.draw.rect(window,"yellow",food)

    for snake_part in snake :
        pygame.draw.rect(window,"cyan",snake_part)

        #RED SNAKE HEAD
        if snake_part == snake[0] :
            pygame.draw.rect(window,"red",snake_part)

    #MESSAGE
    if paused :
        msg_font = pygame.font.SysFont("Times New Roman",42)
        msg_surface = msg_font.render("Press 'P' to Play",True,"#ffffff")
        window.blit(msg_surface,(WINDOW_WIDTH/3.2,WINDOW_HEIGHT/3))

    #SCORE
    score_font = pygame.font.SysFont("Times New Roman",42)
    score_surface = score_font.render(f"000{str(score)}",True,"#ffffff")
    window.blit(score_surface,(TILE_SIZE*21,TILE_SIZE))

while True :
    for event in pygame.event.get() :
        #QUIT
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()

        #MOVEMENTS
        if event.type == pygame.KEYDOWN :

            if event.key in (pygame.K_UP,pygame.K_w) :
                snake_velocity = (0,-TILE_SIZE)
            elif event.key in (pygame.K_DOWN,pygame.K_s) :
                snake_velocity = (0,TILE_SIZE)
            elif event.key in (pygame.K_RIGHT,pygame.K_d) :
                snake_velocity = (TILE_SIZE,0)
            elif event.key in (pygame.K_LEFT,pygame.K_a) :
                snake_velocity = (-TILE_SIZE,0)
            if paused :
                if event.key == pygame.K_p :
                    paused = False
                    snake.clear()
                    snake.append(pygame.Rect(generate_random(COLUMNS),generate_random(ROWS),TILE_SIZE,TILE_SIZE))
                    food = pygame.Rect(generate_random(COLUMNS),generate_random(ROWS),TILE_SIZE,TILE_SIZE)
                    snake_velocity = (0,0)
                    score = 0
            
    if not paused :
        #GENERATING SNAKE BODY
        for i in range(len(snake) - 1,0,-1) :
            snake[i] = snake[i-1].copy()

        #SNAKE VELOCITY
        snake[0].move_ip(snake_velocity)

        #FOOD CONSUMPTION
        if snake[0].center == food.center :
            snake.append(food)
            food = pygame.Rect(generate_random(COLUMNS),generate_random(ROWS),TILE_SIZE,TILE_SIZE)
            score += 1

    #DEFEATING CONDITION
    if snake[0].x < 0 or snake[0].right > WINDOW_WIDTH or snake[0].y < 0 or snake[0].bottom > WINDOW_HEIGHT:
        if snake[0].x < 0 :
            for i in range(len(snake)-1,0,-1) :
                snake[i].x += TILE_SIZE
            snake[0].x = 0
        elif snake[0].right > WINDOW_WIDTH :
            for i in range(len(snake)-1,0,-1) :
                snake[i].right -= TILE_SIZE
            snake[0].right = WINDOW_WIDTH
        elif snake[0].y < 0 :
            for i in range(len(snake)-1,0,-1) :
                snake[i].y += TILE_SIZE
            snake[0].y = 0
        elif snake[0].bottom > WINDOW_HEIGHT :
            for i in range(len(snake)-1,0,-1) :
                snake[i].bottom -= TILE_SIZE
            snake[0].bottom = WINDOW_HEIGHT
        paused = True
        
    display()
    pygame.display.update()
    clock.tick(10)