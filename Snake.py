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
livesFont = pg.font.Font(None, 36)
gamePaused = False
mainMenuState = 1
playingState = 2
scoringState = 3 

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
    #end __init__

    def respawn (self):
        self.speed = 20
        self.direction = right
        self.previousDirection = right
        self.rect.topleft = (0,0)
        for i in self.bodyPosition[1:]:
            i.x = -100
        return

    def restartBody(self):
        self.bodyParts = [self.img]
        self.bodyPosition = [self.rect,pg.Rect(-20,0,20,20)]

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
    #emd __init__

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
        
        self.Fruit = Fruit()
        self.Snake = Snake()
        self.highScoreFont = pg.font.Font(None, 36)
        self.playerScores = 0

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
            newSegment = self.Snake.bodyPosition[-1].copy()
            self.Snake.bodyPosition.append(newSegment)
            self.playerScores += 10
            self.Snake.fruitEaten.play()
            
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
            gamePaused = True
            if self.keysDown[pg.K_SPACE]:
                gamePaused = False
                self.playerScores = 0
                self.Snake.lives = 4
                self.Snake.respawn()
                self.Snake.restartBody()
                self.Fruit.FruitRespawn(self.renderSize)
                self.exitCode = playingState

        return
    #end update 

    def render (self):
        self.renderBuffer.fill((0,0,0))
        self.Snake.render(self.renderBuffer)
        self.Fruit.render(self.renderBuffer)
        scoreSurf = highScoreFont.render(f"Score: {self.playerScores}", True, (100, 255, 255))
        livesSurf = livesFont.render(f"Lives: {self.Snake.lives}", True, (100, 255, 255))
        self.renderBuffer.blit(scoreSurf, (675, 10))
        self.renderBuffer.blit(livesSurf, (675, 35))
        if gamePaused:
            self.exitCode = scoringState
            self.highScoreText = self.highScoreFont.render("Current High Score: %d" %(self.playerScores), True, (255, 255, 255))
            self.renderBuffer.blit(highScoreFont.render("Current High Score: %d" %(self.playerScores), True, (255,255,255)), ((100,100), (200,300)))
            self.renderBuffer.fill((22,4,75))
            self.renderBuffer.blit(gameOverFont.render("Press SPACE to play again." , False, (255,255,255)), ((100,200), (200,300)))
            self.renderBuffer.blit(self.highScoreText, (285,300))
            pg.display.flip()
            
        return
    #end render
#end SnakeState

class MenuState (GameState):
    def __init__ (self) -> None:
        super().__init__()
        self.titleFont = pg.font.Font(None, 70)
        self.startFont = pg.font.Font(None, 40)
        self.scoreFont = pg.font.Font(None, 40)

        return
        #end __init__

    def update (self):
        if self.keysDown[pg.K_RETURN]:
            self.transitionState = SnakeState()
            self.exitCode = mainMenuState 

        return 
        #end update

    def render (self):
        self.renderBuffer.fill((20,20,50))
        self.titleText = self.titleFont.render("SNAKE", True, (255,255,255))
        self.playText = self.startFont.render("Press ENTER to play", True, (255,255,255))
        self.renderBuffer.blit(self.titleText, (285,300))
        self.renderBuffer.blit(self.playText, (250, 400))
        pg.display.flip()

        return
        #end render
#end MenuState

class highScoreState (GameState):
    def __init__ (self) -> None:
        super().__init__(pg.surface.Surface((20,20)))
        self.highScoreFont = pg.font.Font (None, 40)
        self.playerScores = 0
        self.previousScore = 0
        self.getHighScores()
                                         
        return
    #end __init__

    def getHighScores (self):
        with open('data/SnakeHighScore.txt', 'r') as highScores:
              self.playerScores = int(highScores.read().strip())

        return
    #end getHighScores

    def setNewScore (self, newScore):
        self.playerScores = newScore
        if self.playerScores > self.previousScore:
            self.previousScore = self.playerScores
            with open('data/SnakeHighScore.txt', 'w') as highScores:
                highScores.write(str(self.playerScores))
            
    def update (self):
        super().update()
        if self.keysDown[pg.K_SPACE]:
            self.exitCode = scoringState
            
        return
    #end update

    def showHighScores ():
        with open('data/SnakeHighScore.txt', 'r') as highScores:
            return int(highScores.read())
        with open("data/SnakeHighScore.txt", "w") as highScores:
            highScores.write(str(player1Score))
            highScores.write(str(player2Score))

        return
    #end showHighScores

    def render (self):
        super().render()
        self.highScoreText = self.highScoreFont.render("Current High Score: %d" %(self.playerScores), True, (255, 255, 255))
        self.renderBuffer.blit(self.highScoreText, (285,300))
        pg.display.flip()

        return
    #end render
#end highScoreState 

class SnakeGame (Game):
    def __init__ (self) -> None:
        super().__init__(name = 'Snake', displaySize = [800,600])
        self.menuState = MenuState()
        self.playState = SnakeState()
        self.switchState (self.menuState)
        self.highScoreState = highScoreState()
        

        return
    #end __init__

    def update (self):
        super().update()
        if self._state.exitCode == mainMenuState:
            self.switchState(self.playState)
            self._state.exitCode = 0
        elif self._state.exitCode == playingState:
            if isinstance(self._state, SnakeState):
                #Getting the new score from the play session
                score = self._state.Snake.highScore
                #Going from the high score screen to playing again
                self.highScoreState.setNewScore(score)
                self.switchState(self.playState)

        
        #elif self._state.exitCode == scoringState:
            #self.switchState(self.menuState)
            #self._state.exitCode = 0
            #self.highScoreState.setNewScore(score)
            #self.switchState(self.highScoreState)
    
              

        return
    #end update 

    def render (self):
        super().render()

        return
    #end render


#end SnakeGame

def main() -> None:
    myGame: Game = SnakeGame()
        
    myGame.run()

    return
#end main

if __name__ == '__main__':
        main()
#end if
