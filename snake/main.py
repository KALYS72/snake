import pygame as pg
from pygame.math import Vector2
import sys, random

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):  
        x_pos = (self.x * cell_size)    # we are multiplying position to get random place on the field
        y_pos = (self.y * cell_size)
        fruit_rect = pg.Rect(x_pos, y_pos, cell_size,cell_size)   # defining a fruit view  (position and size)
        # also the video told me to put values into integers because every value from Vector2 is going to be a float while pygame requires everything to be int, but everything seems okay so i quess it has been fixed
        screen.blit(apple2,fruit_rect)
        # pg.draw.rect(screen, (126, 166, 114), fruit_rect)         # drawing the fruit on screen 

    def randomize(self):      # when snake eats our fruit it repositions our fruit
        self.x = random.randint(0, cell_number-1)                       # defining the position of an object
        self.y = random.randint(0, cell_number-1)               
        self.pos = Vector2(self.x, self.y) # Vector unlike an ordinary list can get values by their names, not just by their index

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6, 10), Vector2(5, 10)]    # defining the length of a snake
        self.direction = Vector2(1,0)                # direction of a snake (right by default)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = (block.x * cell_size)
            y_pos = (block.y * cell_size)
            block_rect = pg.Rect(x_pos,y_pos,cell_size,cell_size)
            pg.draw.rect(screen, (255, 192, 192), block_rect)

    def reverse(self, direction, coordinate):                # this part of the code was not in the video
        body_copy = self.body[:-1]                            # I wrote it by myself
        if direction == "y" and coordinate == -1:
            body_copy.insert(0,body_copy[0] + Vector2(0,cell_number))
        if direction == "y" and coordinate == 1:
            body_copy.insert(0,body_copy[0] + Vector2(0,-cell_number))
        if direction == "x" and coordinate == -1:
            body_copy.insert(0,body_copy[0] + Vector2(cell_number,0))
        if direction == "x" and coordinate == 1:
            body_copy.insert(0,body_copy[0] + Vector2(-cell_number,0))
        self.body = body_copy[:]

    def move_snake(self):
        if not self.new_block:
            head = self.body[0]
            x = self.direction.x
            y = self.direction.y
            if y == -1 and head.y == 0:
                self.reverse('y', -1)
            if y == 1 and head.y == cell_number:
                self.reverse('y', 1)
            if x == -1 and head.x == 0:
                self.reverse('x', -1)
            if x == 1 and head.x == cell_number:
                self.reverse('x', 1)
            else:
                body_copy = self.body[:-1]           # copiyng each element up to the last
                body_copy.insert(0,body_copy[0] + self.direction)   # adding a position(x,y) on top of the head
                self.body = body_copy[:]            # recording new body to the main one
        else:
            body_copy = self.body[:]           # instead of getting all elements except for the last one like we do in other case, we are getting an entire body instead
            body_copy.insert(0,body_copy[0] + self.direction)    # or in other words we are just getting an entire body and it grows 1 block
            self.body = body_copy[:]
            self.new_block = False

    def add_tail(self): 
        self.new_block = True     

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):           # checks
        self.snake.move_snake()    # direction to move
        self.check_collision()    # if it eats the fruit
        self.check_lose()         # if it eats itself or touches the border

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):          # when snake eats the fruit
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()      # reposition the fruit
            self.snake.add_tail()       # growing a block

    def check_lose(self):
        # if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:  # border check
        #     self.game_over()
        for block in self.snake.body[1:]:        # checking each part of the body except for the head
            if block == self.snake.body[0]:      # if head touches any body part
                self.game_over()

    def game_over(self):
        pg.quit()
        sys.exit()


pg.init()                                  # initializing pygame
cell_size = 40                             # creating a block to fill
cell_number = 20
screen = pg.display.set_mode((cell_size * cell_number, cell_size * cell_number))   # creating a screen
clock = pg.time.Clock()                    # setting up an FPS counter
apple = pg.image.load('assets/apple.jpg').convert_alpha()    # importing an image
apple2 = pg.transform.scale(apple, (cell_size, cell_size))   # resizing it bcs it is huge

main_game = MAIN()

SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)      # creating a gap to move per 150 milliseconds

while True:
    for event in pg.event.get():           # getting every possible keyword
        if event.type == pg.QUIT:          # quitting the game
            pg.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()             
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                if main_game.snake.direction.y != 1:             # if you go reverse immediatly it wont work
                    main_game.snake.direction = Vector2(0,-1)    # for some wierd reason -1 is upwards
            if event.key == pg.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)    
            if event.key == pg.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)    
            if event.key == pg.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)    
    screen.fill((144, 238, 144))                 # painting the display (by RGB standart)
    main_game.draw_elements()
    pg.display.update()                    # just updating the display after the changes
    clock.tick(30)                         # ticks per 30 milliseconds
                                           # reason why i changed it because when you wanted to immediatly press 2 buttons then it would crush 