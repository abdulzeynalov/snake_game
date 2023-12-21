import pygame
import sys 
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE 
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_COLOR = (0,255,0)
FOOD_COLOR = (255,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


class snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1,0)
    
    def move(self, food):
        head = ((self.body[0][0] + self.direction[0]) % GRID_WIDTH, (self.body[0][1] + self.direction[1]) % GRID_HEIGHT)
        if head == food:
            self.body.insert(0,head)
            return True
        else:
            self.body.insert(0,head)
            self.body.pop()
            return False 
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

class food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    def reposition(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

snake = snake()
food = food()

ate_food = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0,-1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0,1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1,0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1,0))
    
    if ate_food:
        food.reposition()
    
    screen.fill((0,0,0))
    for segment in snake.body:
        pygame.draw.rect(screen,SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen,FOOD_COLOR, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))   
    pygame.display.update()

    clock.tick(10)
