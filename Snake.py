import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Slower starting speed
FPS = 6

# Colors
BG = (20, 20, 30)
SNAKE_HEAD = (0, 255, 100)
SNAKE_BODY = (0, 180, 80)
FOOD = (255, 60, 60)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)

# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")

# Fonts
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 50)

# High score file
HS_FILE = "highscore.txt"

if not os.path.exists(HS_FILE):
    with open(HS_FILE, "w") as f:
        f.write("0")


def load_highscore():
    with open(HS_FILE, "r") as f:
        return int(f.read())


def save_highscore(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(200, 200)]
        self.direction = (CELL_SIZE, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]

        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self):
        for i, segment in enumerate(self.body):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY

            pygame.draw.rect(
                screen,
                color,
                (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
                border_radius=5
            )

    def collision(self):
        head = self.body[0]

        # Wall collision
        if (
            head[0] < 0
            or head[0] >= WIDTH
            or head[1] < 0
            or head[1] >= HEIGHT
        ):
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        return False


class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.position = (#this is used
            random.randrange(0, WIDTH, CELL_SIZE),
            
        )

    def draw(self):
        pygame.draw.rect(
            screen,
            FOOD,
            (*self.position, CELL_SIZE, CELL_SIZE),
            border_radius=8
        ) # this will tell the position and size of food

def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color) 
    img = font_obj.render(text,True,color)
    screen.blit(img, (x, y))
    
#code if the game is over
def game_over(score, highscore):

    while True:

        screen.fill(BG)

        draw_text("GAME OVER", big_font, FOOD, 240, 170)
        draw_text(f"Score: {score}", font, WHITE, 320, 270)
        draw_text(f"High Score: {highscore}", font, YELLOW, 290, 320)

        draw_text("Press R to Restart", font, WHITE, 250, 420)
        draw_text("Press Q to Quit", font, WHITE, 275, 470)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return True

                if event.key == pygame.K_q:
                    pygame.quit()
                    return False

# score and food
def main():

    clock = pygame.time.Clock()

    while True:

        snake = Snake()
        food = Food()

        score = 0
        paused = False

        highscore = load_highscore()

        running = True

        while running:

            # Slower speed progression
            speed = min(FPS + score // 10, 15)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_p:
                        paused = not paused

                    if not paused:

                        if (
                            event.key == pygame.K_UP
                            and snake.direction != (0, CELL_SIZE)
                        ):
                            snake.direction = (0, -CELL_SIZE)

                        elif (
                            event.key == pygame.K_DOWN
                            and snake.direction != (0, -CELL_SIZE)
                        ):
                            snake.direction = (0, CELL_SIZE)

                        elif (
                            event.key == pygame.K_LEFT
                            and snake.direction != (CELL_SIZE, 0)
                        ):
                            snake.direction = (-CELL_SIZE, 0)

                        elif (
                            event.key == pygame.K_RIGHT
                            and snake.direction != (-CELL_SIZE, 0)
                        ):
                            snake.direction = (CELL_SIZE, 0)
# game will continue if the game is not paused
            if not paused:

                snake.move()

                if snake.body[0] == food.position:

                    snake.grow = True
                    score += 10

                    while True:
                        food.spawn()
                        

                        if food.position not in snake.body:
                            break
# it will show the scorecard and the game will be ended if the snake collide
                if snake.collision():

                    if score > highscore:
                        highscore = score
                        save_highscore(highscore)
                        

                    running = False

            screen.fill(BG)

            food.draw() # food
            snake.draw()   #Snake
# this is used to print the current score of the game and the highest score of the game played
            draw_text(f"Score: {score}", font, WHITE, 10, 10)
            draw_text(f"High Score: {highscore}", font, YELLOW, 10, 45)

            draw_text(f"Speed: {speed}", font, WHITE, 650, 10)

            if paused:
                draw_text("PAUSED", big_font, WHITE, 280, 250)

            pygame.display.flip()

            clock.tick(speed)

        restart = game_over(score, highscore)
        restart 
        if not restart: #if the game is not restart the game will be not be continued
            break


if __name__ == "__main__":
    main()
    
def main():
    return
