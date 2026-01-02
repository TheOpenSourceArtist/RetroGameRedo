from SimplerGE import *

RENDER_SIZE: list[int] = [800,600]
DISP_SIZE: list[int] = [800,600]

WHITE: list[int] = [255,255,255]

class Ball(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,20,20))
        self.img.fill((255,0,255))
        pg.draw.circle(
            self.img
            ,(255,255,255)
            ,self.rect.center
            ,int(self.rect.w / 2)
            ,0
        )
        self.speed: float = 4.0
        self.velocity = pg.math.Vector2(
            (self.speed,self.speed)
        )

        return
    #end __init__

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

        return
    #end update
#end Ball

class Paddle(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,20,200))
        self.img.fill(WHITE)
        self.speed: float = 7.0

        return
    #end __init__
#end Paddle

class PlayState(GameState):
    def __init__(self) -> None:
        super().__init__(RENDER_SIZE)
        self.ball: Ball = Ball()
        self.paddle: Paddle = Paddle()
        self.ball.rect.x += self.paddle.rect.w
        self.otherPaddle: Paddle = Paddle()
        self.otherPaddle.rect.right = self.rect.right

        self.entities.append(self.ball)
        self.entities.append(self.paddle)
        self.entities.append(self.otherPaddle)

        return
    #end __init__

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

        if self.ball.rect.bottom >= self.rect.bottom:
            self.ball.velocity.y *= -1
        #end if

        if self.ball.rect.top <= self.rect.top:
            self.ball.velocity.y *= -1
        #end if

        if self.ball.rect.right >= self.rect.right:
            self.ball.velocity.x *= -1
        #end if

        if self.ball.rect.left <= self.rect.left:
            self.ball.velocity.x *= -1
        #end if

        return
    #end update

    def onKeysDown(self, keys: list[bool]) -> None:
        if keys[pg.K_DOWN]:
            self.paddle.rect.y += self.paddle.speed

            if self.paddle.rect.bottom > self.rect.bottom:
                self.paddle.rect.bottom = self.rect.bottom
            #end if
        #end if

        if keys[pg.K_UP]:
            self.paddle.rect.y -= self.paddle.speed

            if self.paddle.rect.top < self.rect.top:
                self.paddle.rect.top = self.rect.top
            #end if
        #end if
        
        return
    #end onKeysDown
#end PlayState

def main() -> None:
    pong: Game = Game("Pong", DISP_SIZE)
    pong.switchState(PlayState())

    try:
        pong.run()
    except Exception as e:
        print('Something went wrong:\n%s' % e)
        pong.active = False
    #end try

    return
#end main

if __name__ == '__main__':
    main()
#end if
