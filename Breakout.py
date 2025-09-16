from SimpleGE import *

class Block(RGBSurface):
    def __init__(self, topleft: list[int] = [0,0], size: list[int] = [40,10]) -> None:
        super().__init__(pg.surface.Surface(size),topleft)
        self.name = 'block'
        self.img.fill((255,0,0))
        pg.draw.rect(self.img,(0,0,0),[0,0,size[0],size[1]],1)
        
        return
    #end __init__
    
    def render(self, buffer: pg.surface.Surface) -> None:
        if self.visible:
            super().render(buffer)
        #end if
        
        return
    #end render
#end Block
    
class Ball(RGBSurface):
    def __init__(self, topleft: list[int] = [0,0], size: int = 1) -> None:
        super().__init__(pg.surface.Surface((size,size)),topleft)
        self.name = 'ball'
        self.img.fill((255,0,255))
        pg.draw.circle(self.img,(255,255,255),[size / 2, size / 2],size / 2,0)
        self.img.set_colorkey((255,0,255))
        self.speed = 5
        self.vel: pg.math.Vector2 = pg.math.Vector2(self.speed,-self.speed)
        self.numLives: int = 5
        self.spawnPoint: list[int] = [0,0]
        self.readyToLaunch: bool = True
        
        return
    #end __init__
    
    def update(self, dt: float) -> None:
        if self.readyToLaunch:
            self.rect.center = self.spawnPoint
        else:
            self.rect.center += self.vel
        #end if
        
        return
    #end update
    
    def handleCollision(self, other: Block) -> bool:
        collision: bool = False
        
        if other.visible:
            if other.rect.collidepoint(self.rect.center + self.vel):
                collision = True
                
                if other.name == 'block':
                    other.visible = False
                #end if
                    
                self.vel.y *= -1
            #end if
        #end if
        
        return collision
    #end handleCollision
    
    def handleBounds(self, bounds: list[int]) -> None:
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vel.x *= -1
        elif self.rect.right >= bounds[0]:
            self.right = bounds[0] - 1
            self.vel.x *= -1
        
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vel.y *= -1
        elif self.rect.top > bounds[1]:
            self.numLives -= 1
            self.rect.center = self.spawnPoint
            self.readyToLaunch = True
            
            if self.vel.y > 0:
                self.vel.y *= -1
            #end if
        #end if
        
        return
    #end handleBounds
    
    def handleKeyboard(self, keysDown: list[bool]) -> None:
        if keysDown[pg.K_SPACE]:
            self.readyToLaunch = False
        #end if
        
        return
    #end handleKeyboard
#end Ball
    
class Paddle(Block):
    def __init__(self, topleft: list[int], size: list[int] = [100,50]) -> None:
        super().__init__(topleft, size)
        self.name = 'paddle'
        self.img.fill((0,0,255))
        self.speed: int = 5
        
        return
    #end __init__
    
    def handleKeyboard(self, keysDown: list[bool]) -> None:
        if keysDown[pg.K_RIGHT]:
            self.rect.x += self.speed
        #end if
            
        if keysDown[pg.K_LEFT]:
            self.rect.x -= self.speed
        #end if
        
        return
    #end handleKeyboard
    
    def handleBounds(self, bounds: list[bool]) -> None:
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= bounds[0]:
            self.rect.right = bounds[0]
        #end if
        
        return
    #end handleBounds
#end Paddle
    
class BreakoutState(GameState):
    def __init__(self) -> None:
        super().__init__('breakout', [800,600])
        
        #set up blocks
        self.entities = list()
        
        self.numBlocks: list[int] = [10,4]
        self.remainingBlocks: int = self.numBlocks[0] * self.numBlocks[1]
        self.blockSize: list[int] = [int(self.renderSize[0] / self.numBlocks[0]), int((self.renderSize[1] * 0.2) / self.numBlocks[1])]
        
        for blockY in range(self.numBlocks[1]):
            for blockX in range(self.numBlocks[0]):
                self.entities.append(Block([blockX * self.blockSize[0],blockY * self.blockSize[1] + self.blockSize[1]],self.blockSize))
            #end for
        #end for
                
        #set up paddle
        self.entities.append(Paddle(
            [self.renderSize[0] / 4, self.renderSize[1] - (self.blockSize[1] * 2)]
            ,[self.blockSize[0] * 2, self.blockSize[1]]
        ))
        self.entities[-1].speed = self.blockSize[1] * 0.5
        
        #set up ball
        self.entities.append(Ball(self.renderBuffer.get_rect().center, self.blockSize[1] / 2))
        self.entities[-1].vel.scale_to_length(self.entities[-1].rect.w)
        self.ballIndex: int = len(self.entities) - 1
        
        #set up GUI
        self.entities.append(Text('Lives: %d' % self.entities[self.ballIndex].numLives, self.blockSize[1], name='txtLives'))
        self.entities.append(Text('Blocks: %d' % self.remainingBlocks, self.blockSize[1], name='txtBlocks'))
        self.entities[-1].rect.right = self.renderBuffer.get_rect().right
        
        return
    #end __init__
    
    def render(self) -> None:
        self.renderBuffer.fill((0,0,0))
        
        for entity in self.entities:
            if isinstance(entity,Entity):
                entity.render(self.renderBuffer)
            #end if
        #end for
        
        return
    #end render
    
    def update(self) -> None:            
        for entity in self.entities:
            if isinstance(entity, Paddle):
                entity.handleKeyboard(self.keysDown)
                entity.handleBounds(self.renderSize)
                entity.update(self.deltaTime)
                self.entities[self.ballIndex].handleCollision(entity)
                self.entities[self.ballIndex].spawnPoint = [entity.rect.midtop[0], entity.rect.midtop[1] - self.blockSize[1]]
            elif isinstance(entity,Block):
                entity.update(self.deltaTime)
                collision: bool = False
                collision = self.entities[self.ballIndex].handleCollision(entity)
                
                if collision:
                    self.remainingBlocks -= 1
                #end if
            elif isinstance(entity,Ball):
                entity.update(self.deltaTime)
                entity.handleBounds(self.renderSize)
                entity.handleKeyboard(self.keysDown)
            elif entity.name == 'txtLives':
                entity.updateText('Lives: %d' % self.entities[self.ballIndex].numLives)
            elif entity.name == 'txtBlocks':
                entity.updateText('Blocks: %d' % self.remainingBlocks)
            #end if
        #end for
                
        if self.entities[self.ballIndex].numLives < 0:
            self.exitCode = 1
        elif self.remainingBlocks == 0:
            self.exitCode = 2
        #end if
        
        return
    #end update
#end BreakoutState
    
class EndGame(GameState):
    def __init__(self) -> None:
        super().__init__('endGame', [800,600])
        self.entities = list()
        
        self.entities.append(Text('End Game State', int(self.renderSize[1] / 10)))
        
        return
    #end __init__
    
    def render(self) -> None:
        self.renderBuffer.fill((0,0,0))
        
        for entity in self.entities:
            if isinstance(entity,Entity):
                entity.render(self.renderBuffer)
            #end if
        #end for
        
        return
    #end render
#end BreakoutEndGame
    
class Menu(GameState):
    def __init__(self) -> None:
        super().__init__('menu', [800,600])
        self.entities = list()
        
        self.entities.append(Text('Menu State', int(self.renderSize[1] / 10)))
        
        return
    #end __init__
    
    def render(self) -> None:
        self.renderBuffer.fill((0,0,0))
        
        for entity in self.entities:
            if isinstance(entity,Entity):
                entity.render(self.renderBuffer)
            #end if
        #end for
        
        return
    #end render
#end BreakoutEndGame

def main() -> None:
    game: Game = Game('Breakout',[800,600],BreakoutState())
    game.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if
