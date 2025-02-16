import pygame
import random
import os
pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
bgimg = pygame.image.load("SnakeGame/gallery/images/snake game.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Function to display text
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to plot the snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        text_screen("welcome to game", black, 270, 250)
        text_screen("Press Space Bar to Play", red, 220, 300)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.load('SnakeGame/gallery/images/kids-music-286663.mp3')
                        pygame.mixer.music.play()
                        gameloop()
        pygame.display.update()
        clock.tick(60)
# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Food position
    food_x = random.randint(20, screen_width - 40)
    food_y = random.randint(20, screen_height - 40)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60

    # High score handling
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)
            text_screen(f"High Score: {highscore}", black, 250, 300)
            pygame.display.update()

            # Save high score
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
                        return

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT :
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT :
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP :
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN :
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score+=5
                    

            snake_x += velocity_x
            snake_y += velocity_y

            # Collision with food
            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20 :
                score += 10
                food_x = random.randint(20, screen_width - 40)
                food_y = random.randint(20, screen_height - 40)
                snk_length += 5
                if score > highscore:
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen(f"Score: {score}", red, 5, 5)
            text_screen(f"High Score: {highscore}", black, 600, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Snake collision with itself
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('SnakeGame/gallery/images/explosion-sound-effect-2-241820.mp3')
                pygame.mixer.music.play()

            # Snake collision with boundaries
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.load('SnakeGame/gallery/images/explosion-sound-effect-2-241820.mp3')
                pygame.mixer.music.play()
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)
            pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
