from SimpleGE import *
from random import randint, random
#Initiate Pygame
pg.init()

right = 0
down = 1
up = 2
left = 3
gameOverFont = pg.font.Font(None, 36)
highScoreFont = pg.font.Font(None, 36)
gamePaused = False

#Creating a Snake
class Snake (RGBSurface):
    def __init__(self):
        super().__init__(pg.surface.Surface((20,20)))
        self.name = "snake"
        self.rect = pg.Rect((0,0), (20,20))
        #Snake Image/Creation
        self.img.fill((0,255,0))
        self.bodyParts = [self.img]
        self.bodyPosition = [self.rect,pg.Rect(-20,0,20,20)]
        self.delay = 200
        self.curTick = 0
        self.prevTick = 0
        self.direction = right
        self.moveTimer = 100
        self.moveTimePast = 0
        self.lives = 4
        self.previousDirection = right
        self.highScore = 0
        self.fruitEaten = pg.mixer.Sound(file='sfx/eatingFruit.wav')
        self.soundPlaying = False 
        return

    def respawn (self):
        self.speed = 20
        self.direction = right
        self.previousDirection = right
        self.rect.topleft = (0,0)
        for i in self.bodyPosition[1:]:
            i.x = -100

        #self.lives = self.lives -1

        return 

    def update (self, deltaTime):
        self.moveTimePast += deltaTime

        if self.moveTimePast >= self.moveTimer:
            self.previousDirection = self.direction
            self.moveTimePast = 0
            for positionIndex in range(len(self.bodyPosition) -1,0,-1):
                self.bodyPosition[positionIndex].x = self.bodyPosition[positionIndex-1].x
                self.bodyPosition[positionIndex].y = self.bodyPosition[positionIndex-1].y
            if self.direction == right:
                self.rect.x += self.rect.w
            if self.direction == left:
                self.rect.x -= self.rect.w
            if self.direction == up:
                self.rect.y -= self.rect.w
            if self.direction == down:
                self.rect.y += self.rect.w
        return
    #end update 

    def render (self, renderBuffer) -> None:
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
        random_x = 20 * randint(0, int(800/20)-20)
        random_y = 20 * randint(0, int(600/20)-20)
        self.rect.x = random_x
        self.rect.y = random_y 
        return
#end Fruit class 

class SnakeState (GameState):
    def __init__(self) -> None:
        super().__init__()
        
        #self.bodyParts: list[Snake] = list([Snake()])
        self.Fruit = Fruit()
        self.Snake = Snake()
        return
    #end __init__

    def update (self):
        #Snake Movements
        if self.keysDown [pg.K_RIGHT]:
            if self.Snake.previousDirection != left:
                self.Snake.direction = right
        if self.keysDown [pg.K_UP]:
            if self.Snake.previousDirection != down:
                self.Snake.direction = up
        if self.keysDown [pg.K_DOWN]:
            if self.Snake.previousDirection != up:
                self.Snake.direction = down
        if self.keysDown [pg.K_LEFT]:
            if self.Snake.previousDirection != right:
                self.Snake.direction = left

        self.Snake.update(self.deltaTime)
        self.Fruit.update(self.deltaTime)

        #Setting Snake Growth
        if self.Snake.rect.colliderect(self.Fruit.rect):
            self.Fruit.FruitRespawn(self.renderSize)
            #self.Snake.bodyPosition.append(self.Snake.bodyPosition[-1].move(0,0))
            new_segment = self.Snake.bodyPosition[-1].copy()
            self.Snake.bodyPosition.append(new_segment)
            self.Snake.highScore += 10
            #if self.Snake.soundPlaying == False:
                #self.Snake.soundPlaying = True
            self.Snake.fruitEaten.play()
                 #self.Snake.fruitEaten.stop()
            #Increasing Snake Speed when fruit is eaten
            if self.Snake.moveTimer > 40:
                self.Snake.moveTimer -= 2

        #Snake Collision With itself
        for i in self.Snake.bodyPosition[1:]:
            if self.Snake.rect.colliderect(i):
                self.Snake.respawn()
                self.Snake.lives -=1
        if self.Snake.rect.top < 0:
            self.Snake.respawn()
            self.Snake.lives -=1
        elif self.Snake.rect.right > self.renderSize[0]:
            self.Snake.respawn()
            self.Snake.lives -=1
        elif self.Snake.rect.left < 0:
            self.Snake.respawn()
            self.Snake.lives -=1
        elif self.Snake.rect.bottom > self.renderSize[1]:
            self.Snake.respawn()
            self.Snake.lives -=1

        #Win/Lose Conditions and Game Font
        if self.Snake.lives <= 0:
            global gamePaused
            self.Snake.highScore = 0
            gamePaused = True
            if self.keysDown[pg.K_SPACE]:
                gamePaused = False
                self.Snake.lives = 4
                self.Snake.respawn()
                self.Fruit.FruitRespawn(self.renderSize)

        return

    def render (self):
        self.renderBuffer.fill((0,0,0))
        self.Snake.render(self.renderBuffer)
        self.Fruit.render(self.renderBuffer)
        score_surf = highScoreFont.render(f"Score: {self.Snake.highScore}", True, (100, 255, 255))
        self.renderBuffer.blit(score_surf, (675, 10))
        if gamePaused:
            self.renderBuffer.fill((22,4,75))
            self.renderBuffer.blit(gameOverFont.render("Game Over!" , False, (255,255,255)), ((100,100), (200,300)))
            self.renderBuffer.blit(gameOverFont.render("Press SPACE to play again." , False, (255,255,255)), ((100,200), (200,300)))
        #pg.display.flip()
        return 
#end SnakeState

class MenuState (GameState):
    def __init__ (self) -> None:
        super().__init__()
        self.titleFont = pg.font.Font(None, 70)
        self.startFont = pg.font.Font(None, 40)

        return
        #end __init__

    def update (self):
        if self.keysDown[pg.K_RETURN]:
            self.transitionState = SnakeState()
            self.exitCode = 1

        return 
        #end update

    def render (self):
        self.renderBuffer.fill((20,20,50))
        self.titleText = self.titleFont.render("SNAKE", True, (255,255,255))
        self.playText = self.startFont.render("Press ENTER to play", True, (255,255,255))
        self.renderBuffer.blit(self.titleText, (250,250))
        #self.renderBuffer.blit(self.titleFont, (230, 200))
        self.renderBuffer.blit(self.playText, (270, 350))

        pg.display.flip()

        return
        #end render

#end MenuState

class SnakeGame (Game):

    def __init__ (self) -> None:
        super().__init__(name = 'Snake', displaySize = [800,600])
        self.menuState = MenuState()
        self.playState = SnakeState()
        self.switchState (self.menuState)
        

        return

    def update (self):
        super().update()
        if self._state.exitCode == 1:
            self.switchState(self.playState)

        return

    def render (self):
        super().render()

        return 


    #end SnakeGame

def main() -> None:
    myGame: Game = SnakeGame()
        
    myGame.run()

    return
#end main

if __name__ == '__main__':
        main()
#end if
