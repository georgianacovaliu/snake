import pygame
from pygame.math import Vector2
import sys
import random

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(cell_size * self.position.x), int(cell_size * self.position.y), cell_size, cell_size) #rect
        screen.blit(apple, fruit_rect)

    def draw_bonus(self):
        fruit_rect = pygame.Rect(int(cell_size * self.position.x), int(cell_size * self.position.y), cell_size, cell_size) #rect
        screen.blit(star, fruit_rect)

    def draw_faster(self):
        faster_rect = pygame.Rect(int(cell_size * self.position.x), int(cell_size * self.position.y), cell_size, cell_size) #rect
        screen.blit(pepper, faster_rect)

    def draw_slower(self):
        slower_rect = pygame.Rect(int(cell_size * self.position.x), int(cell_size * self.position.y), cell_size, cell_size) #rect
        screen.blit(milk, slower_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] #pozitia de inceput a sarpelui
        self.direction = Vector2(0, 0)
        self.crunch_sound = pygame.mixer.Sound('Sounds/crunch.wav')

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.ellipse(screen,(34,139,34), block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]  #creeam o copie de la primul element (capul) pana la penultimul element
        body_copy.insert(0, body_copy[0] + self.direction)  #se insereaza noua pozitie a capului, dependenta de pozitia precedenta si de directia de deplasare
        self.body = body_copy[:]

    def add_block(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def play_crunch_sound(self):
        self.crunch_sound.play()

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.bonus = FRUIT()
        self.slower = FRUIT()
        self.faster = FRUIT()
        self.high_score = 0
        self.score = 0
        self.exist_bonus = False
        self.exist_slower = False
        self.exist_faster = False
        self.difficulty = 0
        self.game_speed = 150
        self.background_sound = pygame.mixer.Sound('Sounds/background.wav')
        self.lost_sound = pygame.mixer.Sound('Sounds/lost.wav')
        self.wall = []

    def update(self):
        self.snake.move_snake()
        self.check_eat()
        self.check_death()

    def add_wall_block(self):
        x = random.randint(0, cell_number - 1)
        y = random.randint(0, cell_number - 1)
        wall_block = Vector2(x, y)
        wall_copy = self.wall[:]
        wall_copy.insert(0, wall_block)
        self.wall = wall_copy[:]

    def draw_elements(self):
        self.draw_grass()
        self.draw_wall()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        if self.exist_bonus == True:
            self.bonus.draw_bonus()
        if self.exist_faster == True:
            self.faster.draw_faster()
        if self.exist_slower == True:
            self.slower.draw_slower()

    def check_eat(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

            if self.difficulty == 0:
                self.score +=1
            else:
                if self.difficulty == 1:
                    self.score +=2
                else:
                    self.score +=3

            self.exist_bonus = False
            self.exist_slower = False
            self.exist_faster = False
            self.game_speed -= 10
            pygame.time.set_timer(SCREEN_UPDATE, self.game_speed)
            chance = random.randint(0, 9)
            if chance == 1:
                self.exist_bonus = True
            else:
                if chance == 2:
                    self.exist_faster = True
                else:
                    if chance == 3:
                        self.exist_slower = True
                    else:
                        if chance == 4 or chance == 5:
                            self.add_wall_block()


        if self.exist_bonus == True:
            if self.bonus.position == self.snake.body[0]:
                self.snake.play_crunch_sound()
                self.exist_bonus = False
                if self.difficulty == 0:
                    self.score += 2
                else:
                    if self.difficulty == 1:
                        self.score += 4
                    else:
                        self.score += 6

        if self.exist_faster == True:
            if self.faster.position == self.snake.body[0]:
                self.snake.play_crunch_sound()
                self.exist_faster = False
                self.game_speed -= 30
                pygame.time.set_timer(SCREEN_UPDATE, self.game_speed)

        if self.exist_slower == True:
            if self.slower.position == self.snake.body[0]:
                self.snake.play_crunch_sound()
                self.exist_slower = False
                self.game_speed += 30
                pygame.time.set_timer(SCREEN_UPDATE, self.game_speed)

        for block in self.snake.body[1:]:   #in cazul in care fructul este pozitionat pe corpul sarpelui, se alege o noua pozitie
            if block == self.fruit.position:
                self.fruit.randomize()

        if self.exist_bonus == True:
            for block in self.snake.body[1:]:
                if block == self.bonus.position:
                    self.bonus.randomize()

        if self.exist_faster == True:
            for block in self.snake.body[1:]:
                if block == self.faster.position:
                    self.faster.randomize()

        if self.exist_slower == True:
            for block in self.snake.body[1:]:
                if block == self.slower.position:
                    self.slower.randomize()

    def check_death(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:   #verifica coliziunea cu marginile
            self.reset_snake()
            self.lost_sound.play()

        for block in self.wall:
            if block == self.snake.body[0]:
                self.reset_snake()
                self.lost_sound.play()

        for block in self.snake.body[1:]:     #verifica coliziunea cu propriul corp al sarpelui
            if block == self.snake.body[0]:
                #self.lost_sound.play()
                self.reset_snake()

    def reset_snake(self):
        self.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.snake.direction = Vector2(0, 0)
        if (self.high_score < self.score):
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.game_speed = 240 - self.difficulty * 100
        pygame.time.set_timer(SCREEN_UPDATE, self.game_speed)
        self.wall = []
        self.exist_bonus = False
        self.exist_slower = False
        self.exist_faster = False

    def draw_wall(self):
        for block in self.wall:
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen,(110, 38, 14), block_rect)

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * 1)
        score_y = int(cell_size * 1)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

    def get_high_score(self):
        high_score = 0
        try:
            high_score_file = open("high_score.txt", "r")
            high_score = int(high_score_file.read())
            high_score_file.close()
            print("Scorul maxim este: ", high_score)
        except IOError:
            print("Nu exista scor maxim")
        except ValueError:
            print("Nu exista scor maxim")
        self.high_score = high_score

    def save_high_score(self):
        try:
            high_score_file = open("high_score.txt", "w")
            high_score_file.write(str(self.high_score))
            high_score_file.close()
        except IOError:
            print("Nu se poate salva scorul maxim.")

    def game_loop(self):
        running = True
        self.game_speed = 240 - self.difficulty * 100
        pygame.time.set_timer(SCREEN_UPDATE, self.game_speed)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    main.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main.snake.direction.y != 1:
                            main.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_RIGHT:
                        if main.snake.direction.x != -1:
                            main.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_DOWN:
                        if main.snake.direction.y != -1:
                            main.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main.snake.direction.x != 1:
                            main.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_SPACE:
                        self.reset_snake()
                        running = False

            screen.fill((170, 220, 70))
            main.draw_elements()
            pygame.display.update()
            clock.tick(60)  # framerate maxim ales

    def menu(self):
        click = False
        game_mode = ['Easy', 'Normal', 'Hard']
        self.get_high_score()
        self.background_sound.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    main.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            screen.fill((170, 220, 70))

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(200,220,200,50)
            button_2 = pygame.Rect(200, 300, 200, 50)
            arrow_rect = pygame.Rect(410, 305, 40, 40)

            if button_1.collidepoint((mx, my)):
                if click:
                    self.game_loop()
            if button_2.collidepoint((mx, my)):
                if click:
                    self.game_loop()
            if arrow_rect.collidepoint((mx, my)):
                if click:
                    if self.difficulty < 2:
                        self.difficulty +=1
                    else:
                        self.difficulty = 0


            pygame.draw.rect(screen, (255,140,0), button_1)
            pygame.draw.rect(screen, (255,140,0), button_2)
            screen.blit(arrow, arrow_rect)

            click = False

            textobj = game_menu_font.render('Main menu', True, (100, 30, 12))     #Main menu text
            textrect = textobj.get_rect(center=(300, 120))
            screen.blit(textobj, textrect)

            text_hscore = game_font.render('Highscore: ' + str(self.high_score), True, (100, 30, 12))    #Highscore text
            textrect_hscore = text_hscore.get_rect(center=(300, 165))
            screen.blit(text_hscore, textrect_hscore)

            textobj = game_font.render('Play', True, (100, 30, 12))   #Play text
            screen.blit(textobj, (280,230))

            textobj = game_font.render(game_mode[self.difficulty], True, (100, 30, 12))  # Play text
            screen.blit(textobj, (270, 310))

            image_rect = pygame.Rect(210, 400 , 200, 143)  # rect
            screen.blit(image, image_rect)

            pygame.display.update()
            clock.tick(60)



pygame.init()
pygame.display.set_caption('Snake')
cell_size = 20
cell_number = 30
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 20)
game_menu_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)

apple = pygame.image.load('Images/apple.png').convert_alpha()
star = pygame.image.load('Images/star.png').convert_alpha()
image = pygame.image.load('Images/snake.png').convert_alpha()
arrow = pygame.image.load('Images/arrow.png').convert_alpha()
pepper = pygame.image.load('Images/pepper.png').convert_alpha()
milk = pygame.image.load('Images/milk.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  #150 mls

main = MAIN()

main.menu()


    