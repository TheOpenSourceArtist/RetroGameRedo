from base import *
from renderable import *

class Button(Renderable):
    def __init__(self, text: str, size: list[int] = [100,25], topleft: list[int] = [0,0]) -> None:
        super().__init__()
        #Button will have 6 renderable states
        self.rect: pg.Rect = pg.Rect(topleft,size)
        
        self.initialState: RGBSurface = RGBSurface(pg.surface.Surface(size))
        self.initialState.img.fill((77,77,77))
        
        self.lockedState: RGBSurface = RGBSurface(pg.surface.Surface(size))
        self.lockedState.img.fill((200,77,77))
        
        self.hoverState: RGBSurface = RGBSurface(pg.surface.Surface(size))
        self.hoverState.img.fill((77,77,200))
        
        self.downState: RGBSurface = RGBSurface(pg.surface.Surface(size))
        self.downState.img.fill((50,50,50))
        
        self.pendingState: RGBSurface = RGBSurface(pg.surface.Surface(size))
        self.pendingState.img.fill((200,77,200))
        
        self.activatedState: RGBSurface = RGBSurface(pg.surface.Surface(size))
        self.activatedState.img.fill((77,200,77))
        
        self.states: list[Renderable] = [
           self.initialState
           ,self.lockedState
           ,self.hoverState
           ,self.downState
           ,self.pendingState
           ,self.activatedState
        ]
        
        self.state: int = 0
        
        self.text: Text = Text(text, self.rect.h)
        self.text.rect.center = self.rect.center
        
        return
    #end __init__
    
    def handleMouse(self, mouseDown: list[bool], mousePos: list[int]) -> None:
        #initial state
        if self.state == 0:
            if not mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif not mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 2
            elif mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 1
            elif mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 3
            #end if
        #locked state
        elif self.state == 1:
            if not mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif not mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 2
            elif mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 1
            elif mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 1
            #end if
        #hover state
        elif self.state == 2:
            if not mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif not mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 2
            elif mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 1
            elif mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 3
            #end if
        #down state
        elif self.state == 3:
            if not mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif not mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 5
            elif mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 4
            elif mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 3
            #end if
        #pending state
        elif self.state == 4:
            if not mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif not mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 5
            elif mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 4
            elif mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 3
            #end if
        #activated state
        elif self.state == 5:
            if not mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif not mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 5
            elif mouseDown[0] and not self.rect.collidepoint(mousePos):
                self.state = 0
            elif mouseDown[0] and self.rect.collidepoint(mousePos):
                self.state = 5
            #end if
        #end if
        
        return
    #end handleMouse
    
    def render(self, surface)->None:
        surface.blit(self.states[self.state].img, self.rect)
        surface.blit(self.text.img,self.text.rect)
        
        return
    #end render
#end Button
    
class GUITest(GameState):
    def __init__(self, name: str = 'guitest', renderSize: list[int] = [800,600]) -> None:
        super().__init__(name,renderSize)
        
        return
    #end __init__
    
    def render(self) -> None:
        self.renderBuffer.fill((0,0,0))
        
        for entity in self.entities:
            if isinstance(entity,Renderable):
                entity.render(self.renderBuffer)
            elif isinstance(entity,Entity):
                entity.render()
            #end if
        #end for
        
        return
    #end render
    
    def update(self) -> None:
        for entity in self.entities:
            if isinstance(entity, Button):
                entity.handleMouse(self.mouseDown,self.mousePos)
            #end if
            
            if isinstance(entity,Renderable):
                entity.update(self.deltaTime)
            elif isinstance(entity,Entity):
                entity.render()
            #end if
        #end for
        
        return
    #end update
#end GUITest
    
def main() -> None:
    state: GameState = GUITest()
    state.entities.append(Button('Button'))
    game: Game = Game('GUI Sandbox',[800,600],state)
    game.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if