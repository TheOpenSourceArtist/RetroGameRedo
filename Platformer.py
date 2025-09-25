from SimpleGE import *

class Platform(RGBSurface):
    def __init__(self, size: list[int] = [200,25], center: list[int] = [0,0]) -> None:
        super().__init__(pg.surface.Surface((size)))
        self.img.fill((255,0,0))
        self.rect.center = center
        
        return
    #end __init__
#end Platform
    
class Sprite(RGBSurface):
    def __init__(self, center: list[int] = [0,0]) -> None:
        print('making sprite')
        super().__init__(pg.surface.Surface((50,50)))
        self.img.fill((0,0,255))
        self.rect.center = center
        self.velocity: pg.math.Vector2 = pg.math.Vector2(0,0)
        self.gravity: pg.math.Vector2 = pg.math.Vector2(0,1)
        self.jumpForce: pg.math.Vector2 = pg.math.Vector2(0,-2)
        self.grounded: bool = False
        self.moveSpeed: int = 2
        self.maxJumpSpeed: int = 15
        self.jumping: bool = False
        self.jumpReady: bool = True
        
        return
    #end __init__
    
    def handleKeyboard(self, keys: list[bool]) -> None:
        if self.grounded:
            if self.jumpReady:
                if keys[pg.K_SPACE]:
                    #grounded, jump ready, space pressed
                    self.grounded = False
                    self.jumpReady = False
                    self.jumping = True
                else:
                    #grounded, jump ready, space not pressed
                    self.grounded = True
                    self.jumpReady = True
                    self.jumping = False
                #end
            else:
                if keys[pg.K_SPACE]:
                    #grounded, jump not ready, space pressed
                    self.grounded = True
                    self.jumpReady = False
                    self.jumping = False
                else:
                    #grounded, jump not ready, space not pressed
                    self.grounded = True
                    self.jumpReady = True
                    self.jumping = False
                #end
            #end if
        else:
            if self.jumping:
                if keys[pg.K_SPACE]:
                    #not grounded, jumping, space pressed
                    self.grounded = False
                    self.jumpReady = False
                    self.jumping = True
                else:
                    #not grounded, jumping, space not pressed
                    self.grounded = False
                    self.jumpReady = False #could add double jump here
                    self.jumping = False
                #end if
            else:
                if keys[pg.K_SPACE]:
                    #not grounded, not jumping, space pressed
                    self.grounded = False
                    self.jumpReady = False
                    self.jumping = False
                else:
                    #not grounded, not jumping, space not pressed
                    self.grounded = False
                    self.jumpReady = False
                    self.jumping = False
                #end if
            #end if
        #end if
        
        if self.jumping:
            self.velocity += self.jumpForce
            
            if -self.velocity.y >= self.maxJumpSpeed:
                self.jumping = False
            #end if
        #end if
            
        if keys[pg.K_LEFT]:
            self.velocity.x = -self.moveSpeed
        elif keys[pg.K_RIGHT]:
            self.velocity.x = self.moveSpeed
        else:
            self.velocity.x = 0
        
        return
    #end handleKeyboard
    
    def update(self, dt: float) -> None:
        if self.grounded:
            self.velocity.y = 0
        else:
            self.velocity += self.gravity
        
        self.rect.center += self.velocity
        
        return
    #end update
    
    def handleCollision(self, other: RGBSurface) -> None:
        if self.rect.bottom <= other.rect.top and self.rect.bottom + self.velocity.y >= other.rect.top:
            if self.rect.right >= other.rect.left and self.rect.right + self.velocity.x >= other.rect.left:
                if self.rect.left <= other.rect.right and self.rect.left + self.velocity.x <= other.rect.right:
                    self.rect.bottom = other.rect.top
                    self.grounded = True
                else:
                    self.grounded = False
                #end for
            else:
                self.grounded = False
            #end if
        return
    #end handleCollision
#end Sprite

class TestState(GameState):
    def __init__(self) -> None:
        super().__init__('TestState',[400,300])
        self.platforms: list[Platform] = [
            Platform([200,25],self.renderBuffer.get_rect().center)
            , Platform([self.renderSize[0],25], self.renderBuffer.get_rect().midbottom)
        ]
        self.player: Sprite = Sprite(self.renderBuffer.get_rect().midtop)
        
        self.entities.extend(self.platforms)
        self.entities.append(self.player)
        
        return
    #end __init__
    
    def render(self) -> None:
        self.renderBuffer.fill((0,0,0))
        
        for entity in self.entities:
            if isinstance(entity,Renderable):
                entity.render(self.renderBuffer)
            #end if
        #end for
                
        return
    #end render
    
    def update(self) -> None:
        self.player.handleKeyboard(self.keysDown)
        
        for entity in self.entities:
            if isinstance(entity,Renderable):
                entity.update(self.deltaTime)
            #end if
                
            if isinstance(entity,Platform):
                self.player.handleCollision(entity)
            #end if
        #end for
                
        return
    #end update
#end TestState

class Platformer(Game):
    def __init__(self) -> None:
        super().__init__('Platformer Test', [800,600])
        self.states: list[GameState] = [
            TestState()
        ]
        self.stateIndex: int = 0
        self.switchState(self.states[self.stateIndex])
        
        return
    #end __init__
#end Platformer

def main() -> None:
    game: Platformer = Platformer()
    game.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if