import pygame
import random
import time
pygame.init()
CELL_SIZE = 20
CELL_HEIGHT = 20
CELL_WIDTH = 20
screen = pygame.display.set_mode((30*CELL_WIDTH,30*CELL_HEIGHT))


class Snake:
    def __init__(self,width,height,x,y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.direction = [0,0]
        self.snake = [[self.x*CELL_SIZE,self.y*CELL_SIZE]]
        self.rects = []
        self.new  = []
        
        
    def create_rect(self):
        for segment in self.snake:
            rect = pygame.Rect(segment[0],segment[1],self.width,self.height)
            self.rects.append(rect)
    def draw(self):
        self.rects = []
        self.create_rect()
        for rect in self.rects:
            pygame.draw.rect(screen,(0,255,0),rect)
    
    def move(self,rect):
        self.create_rect()
        dx = self.snake[0][0]+(self.direction[0]*CELL_SIZE)
        dy = self.snake[0][1]+(self.direction[1]*CELL_SIZE)
        new = [dx,dy]
        self.snake.insert(0,new)
        self.collide(rect)
        #self.snake.pop()
    def collide(self,rect):
        if self.rects[0].colliderect(rect):
            return True
        else:
            self.snake.pop()
        
    def hit_wall(self):
        if self.snake[0][0] >=600 or self.snake[0][0] <=0 or self.snake[0][1] >= 600 or self.snake[0][1] <= 0:
            self.direction = [0,0]
            return True
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
    def __init__(self,radius,x,y):
        self.radius = radius
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.circle(screen,center=(self.x,self.y),radius = self.radius,color = (125,125,255))
    def invisa_rect(self):
        rect = pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
        return rect
    def collide(self,snake):
        rect = pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
        if snake.colliderect(rect):
            self.x = random.randint(20,600-30)
            self.y = random.randint(20,600-30)
            
    

snake = Snake(CELL_WIDTH,CELL_HEIGHT,6,12)
food = Food(10,random.randint(20,600-30),random.randint(20,600-30))
while True:
    screen.fill((200,255,200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                snake.left()
            if event.key == pygame.K_RIGHT:
                snake.right()
            if event.key == pygame.K_UP:
                snake.up()
            if event.key == pygame.K_DOWN:
                snake.down()
            
            
    
    
    snake.move(food.invisa_rect())
    food.collide(snake.rects[0])
    snake.draw()
    food.draw()
    if snake.hit_wall():
        screen.fill((0,0,0))
       
    #print(len(snake.rects))
    
   
    time.sleep(0.15)
    pygame.display.update()