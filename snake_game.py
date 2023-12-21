import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0

    def move(self, food):
        head = ((self.body[0][0] + self.direction[0]) % GRID_WIDTH, (self.body[0][1] + self.direction[1]) % GRID_HEIGHT)
        if head == food.position:
            self.body.insert(0, head)
            self.score += 10
            return True
        else:
            self.body.insert(0, head)
            if len(self.body) > 1 and self.body[0] in self.body[1:]:
                game_over()
            else:
                self.body.pop()
            return False

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def reposition(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        pygame.draw.rect(screen, FOOD_COLOR, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("You Died!", True, (255, 255, 255))
        restart_text = font.render("Press 'R' to Restart", True, (255, 255, 255))
        quit_text = font.render("Press 'Q' to Quit", True, (255, 255, 255))
        score_text = font.render(f"Final Score: {snake.score}", True, (255, 255, 255))

        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        screen.blit(score_text, (10, 10))
        pygame.display.update()


def restart_game():
    global high_score
    snake.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake.direction = (1, 0)
    snake.score = 0
    high_score = load_high_score()
    food.reposition()


def save_high_score(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))


def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


snake = Snake()
food = Food()

high_score = load_high_score()

while True:
    ate_food = snake.move(food)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_s:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_a:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_d:
                snake.change_direction((1, 0))

    if (
        snake.body[0][0] < 0
        or snake.body[0][0] >= GRID_WIDTH
        or snake.body[0][1] < 0
        or snake.body[0][1] >= GRID_HEIGHT
    ):
        game_over()

    if ate_food:
        food.reposition()

    screen.fill((255, 192, 203))
    snake.draw()
    food.draw()

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {snake.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 0))

    pygame.display.update()
    clock.tick(01)
