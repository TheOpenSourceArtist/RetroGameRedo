from SimplerGE import *
from random import randint, choices

#-------------------------------------------------------------------------------
#   GLOBAL SETTINGS
#-------------------------------------------------------------------------------

#display Settings
RENDER_SIZE: list[int] = [200,150]
DISP_SIZE: list[int] = [800,600]

#object settings
BALL_SIZE: int = int(RENDER_SIZE[0] / 37)
BALL_SPEED: float = BALL_SIZE * 0.5

PADDLE_SIZE: tuple[int] = (BALL_SIZE,int(RENDER_SIZE[1] / 3))
PADDLE_SPEED: float = BALL_SPEED * 2.0
UP: int = 0
DOWN: int = 1
STOPPED: int = 2

#colors
TRANSPARENT: tuple[int] = (255,0,255)
WHITE: tuple[int] = (255,255,255)
BLACK: tuple[int] = (0,0,0)

#-------------------------------------------------------------------------------
#   CLASS DEFINITIONS
#-------------------------------------------------------------------------------

class Paddle(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,PADDLE_SIZE[0],PADDLE_SIZE[1]))
        self.img.fill(WHITE)
        
        return
    #end __init__
#end Paddle
    
class AIPaddle(Paddle):
    def __init__(self) -> None:
        super().__init__()
        self.moveDir: int = DOWN
        self.dirTimer: float = 100
        self.dirTimeDelta: float = 0
        self.decisionReady: bool = False
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        self.dirTimeDelta += deltaTime
        
        if self.dirTimeDelta >= self.dirTimer:
            self.dirTimeDelta = 0
            self.decisionReady = True
        #end if
        
        if self.moveDir == DOWN:
            self.rect.y += PADDLE_SPEED
        elif self.moveDir == UP:
            self.rect.y -= PADDLE_SPEED
        #end if
        
        return
    #end update
    
    def decideOnDirection(self, pos: list[int]) -> None:
        if self.decisionReady:
            upChance: float = 1.0
            stopChance: float = 1.0
            downChance: float = 1.0
            
            #paddle should be more inclined to keep its current move direction
            if self.moveDir == UP:
                upChance *= 5
                stopChance *= 0.2
                downChance *= 0.0
            elif self.moveDir == DOWN:
                upChance *= 0.0
                stopChance *= 0.2
                downChance *= 5
            #end if
            
            #influence move direction by y position of the ball
            if pos[1] <= self.rect.centery:
                upChance *= 2
                downChance = 0
            elif abs(pos[0] - self.rect.left) < PADDLE_SIZE[1]:
                stopChance *= 2
            elif pos[1] >= self.rect.centery:
                downChance *= 2
                upChance = 0
            #end if
            
            self.moveDir = choices([UP,STOPPED,DOWN], [upChance, stopChance, downChance])[0]
            
            self.decisionReady = False
        #end if
        
        return
    #end decideOnDirection
#end AIPaddle

class Ball(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,BALL_SIZE,BALL_SIZE),vel=[BALL_SPEED,BALL_SPEED])
        self.img.fill(TRANSPARENT)
        pg.draw.circle(
            self.img
            ,WHITE
            ,self.rect.center
            ,int(self.rect.w/2)
            ,0
        )
        
        return
    #end __init__
#end Ball

class PlayState(GameState):
    def __init__(self) -> None:
        super().__init__(RENDER_SIZE)
        self.ball: Ball = Ball()
        self.paddle: Paddle = Paddle()
        self.paddle.rect.x += BALL_SIZE
        self.ball.rect.left = self.paddle.rect.right + BALL_SIZE
        self.aiPaddle: AIPaddle = AIPaddle()
        self.aiPaddle.rect.right = self.rect.right - BALL_SIZE
        
        self.entities.append(self.ball)
        self.entities.append(self.paddle)
        self.entities.append(self.aiPaddle)
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        #Handle Collisions
        if self.ball.rect.right + self.ball.velocity.x >= self.rect.right:
            self.ball.rect.right = self.rect.right
            self.ball.velocity.x *= -1
        #end if
            
        if self.ball.rect.left - self.ball.velocity.x <= self.rect.left:
            self.ball.rect.left = self.rect.left
            self.ball.velocity.x *= -1
        #end if
            
        if self.ball.rect.top - self.velocity.y <= self.rect.top:
            self.ball.rect.top = self.rect.top
            self.ball.velocity.y *= -1
        #end if
            
        if self.ball.rect.bottom + self.ball.velocity.y >= self.rect.bottom:
            self.ball.rect.bottom = self.rect.bottom
            self.ball.velocity.y *= -1
        #end if
            
        if self.ball.rect.left - BALL_SPEED <= self.paddle.rect.right:
            if self.ball.rect.bottom >= self.paddle.rect.top and self.ball.rect.top <= self.paddle.rect.bottom:
                self.ball.rect.left = self.paddle.rect.right + 1
                self.ball.velocity.x *= -1
            #end if
        #end if
                
        if self.ball.rect.right + BALL_SPEED >= self.aiPaddle.rect.left:
            if self.ball.rect.bottom >= self.aiPaddle.rect.top and self.ball.rect.top <= self.aiPaddle.rect.bottom:
                self.ball.rect.right = self.aiPaddle.rect.left - 1
                self.ball.velocity.x *= -1
            #end if
        #end if
        
        #control AI
        self.aiPaddle.decideOnDirection(self.ball.rect.center)
        
        if self.aiPaddle.rect.top < self.rect.top:
            self.aiPaddle.rect.top = self.rect.top
            self.aiPaddle.moveDir = STOPPED
        elif self.aiPaddle.rect.bottom > self.rect.bottom:
            self.aiPaddle.rect.bottom = self.rect.bottom
            self.aiPaddle.moveDir = STOPPED
        #end if
        
        return
    #end update
    
    def onKeysDown(self, keys: list[bool]) -> None:
        if keys[pg.K_DOWN]:
            self.paddle.rect.y += PADDLE_SPEED
            
            if self.paddle.rect.bottom + PADDLE_SPEED >= self.rect.bottom:
                self.paddle.rect.bottom = self.rect.bottom
            #end if
        #end if
        
        if keys[pg.K_UP]:
            self.paddle.rect.y -= PADDLE_SPEED
            
            if self.paddle.rect.top - PADDLE_SPEED <= self.rect.top:
                self.paddle.rect.top = self.rect.top
            #end if
        #end if
        
        return
    #end onKeysDown
#end PlayState

class PongGame(Game):
    def __init__(self) -> None:
        super().__init__('Pong Game', DISP_SIZE)
        self.switchState(PlayState())
        
        return
    #end __init__
#end PongGame
    
#-------------------------------------------------------------------------------
#   FUNCTION DEFINITIONS
#-------------------------------------------------------------------------------

def main() -> None:
    pong: PongGame = PongGame()
    
    try:
        pong.run()
    except Exception as e:
        print(e)
        pong.active = False
    #end try
    
    return
#end main

if __name__ == '__main__':
    main()
#end if