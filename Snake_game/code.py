import board
import busio
import displayio
import adafruit_st7789
import random
import time

displayio.release_displays()

spi = busio.SPI(
    clock = board.GP18,#SCL
    MOSI = board.GP19#SDA
)

wires = displayio.FourWire(
    spi,
    command = board.GP20,#DS
    chip_select = board.GP17,#CS
    reset = board.GP16#RES
)

display = adafruit_st7789.ST7789(
    wires,
    width = 240,
    height = 240
)

CELL_SIZE = 20
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240
GRID_W = SCREEN_WIDTH//CELL_SIZE
GRID_H = SCREEN_HEIGHT//CELL_SIZE

background = displayio.Bitmap(SCREEN_WIDTH,SCREEN_HEIGHT,3)

palette = displayio.Palette(3)
palette[0] = 0x000000
palette[1] = 0x008000
palette[2] = 0xFF0000

background_grid = displayio.TileGrid(
    background,
    pixel_shader = palette
)

group = displayio.Group()
group.append(background_grid)

display.root_group = group#show 



class Snake:
    def __init__(self,x,y):
        self.width = CELL_SIZE
        self.height = CELL_SIZE
        self.x = x
        self.y = y
        self.direction = [1,0]
        self.snake = [[self.x*CELL_SIZE,self.y*CELL_SIZE]]
        self.new  = []
        
        
    def draw(self):
        for segment in self.snake:
            x = segment[0]
            y = segment[1]
            for py in range(self.height):
                for px in range( self.width):
                    background[x + px, y + py] = 1

    def move(self,food):

        dx = self.snake[0][0]+(self.direction[0]*CELL_SIZE)
        dy = self.snake[0][1]+(self.direction[1]*CELL_SIZE)
        new = [dx,dy]
        self.snake.insert(0,new)
        ate = self.collide(food)
        if not ate:
            self.snake.pop()
        else:
            food.respawn(self.snake)

    def collide(self,food):
        return self.snake[0] == [food.x,food.y]
           
       
        
    def hit_wall(self):
        if self.snake[0][0] >= SCREEN_WIDTH or self.snake[0][0] < 0 or self.snake[0][1] >= SCREEN_HEIGHT or self.snake[0][1] < 0:
            self.direction = [0,0]
            return True
        for i in range(1,len(self.snake)):
            if self.snake[0] == self.snake[i]:
                return True
        return False
    def up(self):
         if self.direction != (0,1):
            self.direction = (0,-1)
    def down(self):
        if self.direction != (0,-1):
            self.direction = (0,1)
        

    def left(self):
        if  self.direction != (1,0):
            self.direction = (-1,0)
    def right(self):
        if  self.direction != (-1,0):
            self.direction = (1,0)

class Food:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self):
        for px in range(CELL_SIZE):
            for py in range(CELL_SIZE):
                background[self.x+px,self.y+py] = 2
    def respawn(self,snake):
        while True:
            x = random.randint(0,GRID_W-1)*CELL_SIZE
            y = random.randint(0,GRID_H-1)*CELL_SIZE

            if [x,y] not in snake:
                self.x = x
                self.y = y
                return
        

snake = Snake(2,2)
food = Food(random.randint(0,GRID_W-1)*CELL_SIZE,random.randint(0,GRID_H-1)*CELL_SIZE)
food.respawn(snake.snake)
while True:
    snake.move(food)

    if snake.hit_wall():
        background.fill(0)
        time.sleep(5)
        snake.direction = [1,0]
        snake.snake = [[snake.x*CELL_SIZE,snake.y*CELL_SIZE]]
        food.respawn(snake.snake)


    

    background.fill(0)

    snake.draw()
    food.draw()
    time.sleep(0.2)
    