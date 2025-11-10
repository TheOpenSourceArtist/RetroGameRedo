from SimpleGE import *

class Paddle(RGBSurface):
    def __init__(self) -> None:
        super().__init__(pg.surface.Surface([15,75]),[10,0])
        self.img.fill((255,255,255))
        
        return
    #end __init__
    
    def update(self, dt: int) -> None:
        
        return
    #end update
#end Ball

class Ball(RGBSurface):
    def __init__(self) -> None:
        super().__init__(pg.surface.Surface([10,10]))
        pg.draw.circle(self.img,(255,255,255),[5,5],5)
        self.velocity: pg.math.Vector2 = pg.math.Vector2(5,5)
        
        return
    #end __init__
    
    def update(self, dt: int) -> None:
        self.rect.center += self.velocity
        
        return
    #end update
#end Ball

class PongState(GameState):
    def __init__(self) -> None:
        super().__init__()
        self.ball: Ball = Ball()
        self.playerPaddle: Paddle = Paddle()
        self.compPaddle: Paddle = Paddle()
        self.compPaddle.rect.right = self.renderSize[0] - 15
        
        self.entities.append(self.ball)
        self.entities.append(self.playerPaddle)
        self.entities.append(self.compPaddle)
        
        return
    #end __init__
    
    def update(self) -> None:
        super().update()
        
        if self.ball.rect.right >= self.renderSize[0]:
            self.ball.velocity.x *= -1
        elif self.ball.rect.left < 0:
            self.ball.velocity.x *= -1
        #end if
            
        if self.ball.rect.top < 0:
            self.ball.velocity.y *= -1
        elif self.ball.rect.bottom >= self.renderSize[1]:
            self.ball.velocity.y *= -1
        #end if
            
        if self.keysDown[pg.K_DOWN]:
            self.playerPaddle.rect.bottom += 10
            
            if self.playerPaddle.rect.bottom >= self.renderSize[1]:
                self.playerPaddle.rect.bottom = self.renderSize[1]
            #end if
        #end if
        
        if self.keysDown[pg.K_UP]:
            self.playerPaddle.rect.bottom -= 10
            
            if self.playerPaddle.rect.top < 0:
                self.playerPaddle.rect.top = 0
            #end if
        #end if
                
        self.compPaddle.rect.y = self.ball.rect.y
                
        if self.ball.rect.colliderect(self.playerPaddle.rect) or self.ball.rect.colliderect(self.compPaddle.rect):
            self.ball.velocity.x *= -1
        
        return
    #end update
#end PongState

def main() -> None:
    pong: Game = Game('Pong',[800,600],PongState())
    pong.run()    

    return
#end main

if __name__ == '__main__':
    main()
#end if
