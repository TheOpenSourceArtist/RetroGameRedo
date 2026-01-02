from SimpleGE import *
from random import randint, random
right = 0
down = 1
up = 2
left = 3

#Creating a Snake
class Snake (RGBSurface):
    def __init__(self):
        super().__init__(pg.surface.Surface((20,20)))
        self.name = "snake"
        self.rect = pg.Rect((0,0), (20,20))
        #Snake Image/Creation
        self.img.fill((0,255,0))
        self.bodyParts = [self.img]
        self.bodyPosition = [self.rect, pg.Rect(-20,0,20,20)]
        self.delay = 200
        self.curTick = 0
        self.prevTick = 0
        self.direction = right
        self.moveTimer = 100
        self.moveTimePast = 0
        self.lives = 3

        return

    def respawn (self):
        self.speed = 20
        self.direction = 0
        self.rect.topleft = (0,0)
        for i in self.bodyPosition:
            i.x = -100

        self.lives = self.lives -1

    def update(self, deltaTime):
        self.moveTimePast += deltaTime

        if self.moveTimePast >= self.moveTimer:
            self.moveTimePast = 0
            for positionIndex in range(len(self.bodyPosition) -1,0,-1):
                self.bodyPosition[positionIndex].x = self.bodyPosition[positionIndex-1].x
                self.bodyPosition[positionIndex].y = self.bodyPosition[positionIndex-1].y

            if self.direction == right:
                self.bodyPosition[0].x += self.rect.w
            if self.direction == left:
                self.bodyPosition[0].x -= self.rect.w
            if self.direction == up:
                self.bodyPosition[0].y -= self.rect.w
            if self.direction == down:
                self.bodyPosition[0].y += self.rect.w

            


        return  

    def render(self, renderBuffer) -> None:
        for position in self.bodyPosition:
            renderBuffer.blit(self.img, position)

            
        
        return
    #end render
    
#end Snake class

class Fruit (RGBSurface):
    def __init__(self):
        super().__init__(pg.surface.Surface((20,20)))
        self.name = "fruit"
        self.rect = pg.Rect((400,400), (20,20))
        #Fruit Image/Creation 
        self.img.fill((238,75,43))
        return

    def FruitRespawn (self, screen_size):
        random_x = randint(0, screen_size[0] - self.rect.w)
        random_y = randint(0, screen_size[1] - self.rect.h)
        self.rect.x = random_x
        self.rect.y = random_y 
        return
#end Fruit class 

class SnakeState(GameState):
    def __init__(self) -> None:
        super().__init__()
        
        #self.bodyParts: list[Snake] = list([Snake()])
        self.Fruit = Fruit()
        self.Snake = Snake()

        livesFont = pg.font.Font(None, 40)
        gameOverFont = pg.font.Font(None, 120)
        gamePaused = False

        return
    #end __init__

    def update(self):
        if self.keysDown [pg.K_RIGHT]:
            self.Snake.direction = right
        if self.keysDown [pg.K_UP]:
            self.Snake.direction = up
        if self.keysDown [pg.K_DOWN]:
            self.Snake.direction = down
        if self.keysDown [pg.K_LEFT]:
            self.Snake.direction = left
        self.Snake.update(self.deltaTime)
        self.Fruit.update(self.deltaTime)

        #Setting Snake Growth
        if self.Snake.rect.colliderect(self.Fruit.rect):
            self.Fruit.FruitRespawn(self.renderSize)
    
            #self.Snake.bodyParts.append(pg.surface.Surface([self.Snake.rect.w, self.Snake.rect.h]))
            #self.Snake.bodyParts[-1].fill((0,255,0))
            self.Snake.bodyPosition.append(self.Snake.bodyPosition[-1].move(0,0))
        
            print(self.Snake.bodyParts)

            
        return

    def render (self):
        self.renderBuffer.fill((0,0,0))
        self.Snake.render(self.renderBuffer)
        self.Fruit.render(self.renderBuffer)

        return 
#end SnakeState
    	
def main() -> None:
        myGame: Game = Game(
                name = 'Snake'
                ,displaySize = [800,600]
                ,initialState = SnakeState()
        )
        
        myGame.run()
        

        return
#end main

if __name__ == '__main__':
        main()
#end if
