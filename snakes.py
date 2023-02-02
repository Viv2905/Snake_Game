import pygame
import random
import os

pygame.init()
# print(x)  -> show (a, b) where a = number of modules imported, & b = no. of errors while importing those modules

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
x = (255, 200, 255)

screen_width = 800
screen_height = 400

# Creating game-window
gameWindow = pygame.display.set_mode((screen_width, screen_height))   # (width, height)
pygame.display.set_caption("Snake Game")
pygame.display.flip()  # To update the content of entire display surface of the screen
# pygame.display.update()  # Same as above

bgimg = pygame.image.load("gameBG.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])   
        # rect( SURFACE, COLOR, RECT_OBJECT, BORDER_WIDTH, BORDER_RADIUS)

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 210, 229))
        text_screen("Welcome to Snakes", blue, 220, 150)
        text_screen("( press 'SPACEBAR' to play )", black, 140, 190)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game loop
def gameloop():
    # Creating game specific variables
    k = 0
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    add_vel = 6

    food_x = random.randint(20, screen_width-20)
    food_y = random.randint(20, screen_height-20)
    score = 0
    # init_velocity = 5
    snake_size = 10
    snk_length = 1
    snk_list = []
    fps = 20

    # Check if hiscore file exists
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            
            gameWindow.fill((233, 210, 229))
            text_screen("GAME OVER!! 😫", red, 280, 150)
            text_screen("(press 'ENTER' to continue)", black, 170, 190)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # gameloop()
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if k == 0:
                    prevKeyPressed = pygame.K_RIGHT
                    velocity_x = add_vel
                    k += 1
                    # clock.tick(60)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and prevKeyPressed != pygame.K_LEFT:
                        velocity_x = add_vel
                        velocity_y = 0
                        prevKeyPressed = pygame.K_RIGHT
                    
                    if event.key == pygame.K_LEFT and prevKeyPressed != pygame.K_RIGHT:
                        velocity_x = -add_vel
                        velocity_y = 0
                        prevKeyPressed = pygame.K_LEFT

                    if event.key == pygame.K_DOWN and prevKeyPressed != pygame.K_UP:
                        velocity_x = 0
                        velocity_y = add_vel
                        prevKeyPressed = pygame.K_DOWN

                    if event.key == pygame.K_UP and prevKeyPressed != pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = -add_vel
                        prevKeyPressed = pygame.K_UP

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 7 and abs(snake_y - food_y) < 7:
                score += 1
                # print("Score: ", score)
                food_x = random.randint(20, screen_width-20)
                food_y = random.randint(20, screen_height-20)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "        Hi-Score: " + str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, x, [food_x, food_y, 7, 7],7,3)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("lullaby_of_death2.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("lullaby_of_death2.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow, white, snk_list, snake_size)
            
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()