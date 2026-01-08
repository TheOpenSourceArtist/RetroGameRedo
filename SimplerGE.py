import pygame as pg

SGE_COLORKEY_DEFAULT: tuple[int] = (255,0,255,255)

pg.init()

class Entity:
    def __init__(self, rect: pg.Rect = (0,0,0,0), img:pg.surface.Surface = None, vel: list[float] = [0,0], accel: list[float] = [0,0]) -> None:
        self.active: bool = True #should run update
        self.visible: bool = True #should run render
        self.solid: bool = True #should handle collisions
        self.rect: pg.Rect = pg.Rect(rect) #size and position
        self.img: pg.surface.Surface = img #image pixel data
        
        if not isinstance(self.img,pg.surface.Surface):
            self.img = pg.surface.Surface(self.rect.size)
        #end if
            
        self.img.set_colorkey(SGE_COLORKEY_DEFAULT)
        
        self.velocity: pg.math.Vector2 = pg.math.Vector2(vel)
        self.accel: pg.math.Vector2 = pg.math.Vector2(accel)
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        renderBuffer.blit(self.img, self.rect)
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        self.velocity += self.accel
        self.rect.center += self.velocity
        
        return
    #end update
    
    def collide(self, other) -> bool:
        if isinstance(other, Entity):
            if not self.solid or not other.solid:
                return False
            else:
                return self.rect.colliderect(other.rect)
        else:
            return False
        #end if
    #end collide
#end Entity
    
class GameState(Entity):
    def __init__(self, renderSize: list[int] = (800,600)) -> None:
        super().__init__(((0,0),renderSize))
        self.entities: list[Entity] = list()
        self.exitCode: int = 0
        self.active = False
        self.visible = False
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        #clear the render buffer
        self.img.fill((0,0,0))
        
        #render each entity
        for entity in self.entities:
            if isinstance(entity, Entity):
                if entity.visible:
                    entity.render(self.img)
                #end if
            #end if
        #end for
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        #update each entity
        for entity in self.entities:
            if isinstance(entity, Entity):
                if entity.active:
                    entity.update(deltaTime)
                #end if
            #end if
        #end for
        
        return
    #end update
    
    def onKeysDown(self, keys: list[bool]) -> None:
        
        return
    #end handleKeyboard
    
    def onKeyPressed(self, key: int) -> None:
        
        return
    #end onKeyPressed
    
    def onKeyReleased(self, key: int) -> None:
        
        return
    #end onKeyReleased
    
    def onMouseButtonsDown(self, buttons: list[bool]) -> None:
        
        return
    #end onMouseButtonsDown
    
    def onMouseButtonPressed(self, button: int) -> None:
        
        return
    #end onMouseButtonPressed
    
    def onMouseButtonReleased(self, button: int) -> None:
        
        return
    #end onMouseButtonReleased
    
    def onMouseButtonsDown(self, buttons: list[bool]) -> None:
        
        return
    #onMouseButtonsDown
    
    def onMousePosUpdate(self, pos: list[int]) -> None:
        
        return
    #end onMousePosUpdate

    def onJoyButtonPressed(self, button: int) -> None:

        return
    #end onJoyButtonPressed
    
    def onStateEnter(self) -> None:
        self.visible = True
        self.active = True
        self.exitCode = 0
        
        return
    #end onStateEnter
    
    def onStateExit(self) -> None:
        self.visible = False
        self.active = False
        self.exitCode = 0
        
        return
    #end onStateExit
#end GameState
    
class Game(Entity):
    def __init__(self, title: str = "SimpleGE Window", displaySize: list[int] = (800,600), state: GameState = None) -> None:
        super().__init__(((0,0),displaySize))
        
        self.title: str = title
        pg.display.set_caption(self.title)
        self.active = False
        self.deltaTime = 0
        self.fps: int = 60
        self.clock: pg.time.Clock = pg.time.Clock()
        self.state: GameState = state
        
        if not isinstance(self.state,GameState):
            self.state = None
        #end if
        
        return
    #end __init__
    
    def __del__(self) -> None:
        pg.quit()
        
        return
    #end __del__
    
    def run(self) -> None:
        self.active = True
        self.img = pg.display.set_mode(self.rect.size)
        
        while self.active:
            self.handleEvents()
            self.update(self.deltaTime)
            self.render(self.img)
            self.syncFPS()
        #end while
        
        pg.quit()
        
        return
    #end run
    
    def handleEvents(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.active = False
            elif event.type == pg.KEYDOWN:
                if isinstance(self.state,GameState):
                    self.state.onKeyPressed(event.key)
                #end if
            elif event.type == pg.KEYUP:
                if isinstance(self.state,GameState):
                    self.state.onKeyReleased(event.key)
                #end if
            elif event.type == pg.MOUSEBUTTONDOWN:
                if isinstance(self.state,GameState):
                    self.state.onMouseButtonPressed(event.button)
                #end if
            elif event.type == pg.MOUSEBUTTONUP:
                if isinstance(self.state,GameState):
                    self.state.onMouseButtonReleased(event.button)
                #end if
            elif event.type == pg.JOYBUTTONDOWN:
                if isinstance(self.state,GameState):
                    self.state.onJoyButtonPressed(event.button)
                #end if
            #end if
        #end for
        
        #handle inputs for the gamestate
        if isinstance(self.state,GameState):
            self.state.onKeysDown(pg.key.get_pressed())
            self.state.onMouseButtonsDown(pg.mouse.get_pressed())
            self.state.onMousePosUpdate(pg.mouse.get_pos())
        #end if
        
        return
    #end handleEvents
    
    def update(self, deltaTime: float) -> None:
        if isinstance(self.state,GameState):
            if self.state.active:
                self.state.update(deltaTime)
            #end if
        #end if
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        #clear the display buffer
        self.img.fill((0,0,0))
        
        #call the state's render function and render and scale it's buffer to the display
        if isinstance(self.state,GameState):
            if self.state.visible:
                self.state.render(renderBuffer)
                pg.transform.scale(self.state.img,self.rect.size,self.img)
            #end if
        #end if
            
        #present the display buffer
        pg.display.flip()
        
        return
    #end render
    
    def syncFPS(self) -> None:
        self.deltaTime = self.clock.tick(self.fps)
        
        return
    #end if
    
    def enterState(self, state: GameState) -> None:
        if isinstance(state, GameState):
            self.state = state
        #end if
            
        self.state.onStateEnter()
        
        return
    #end enterState
    
    def exitState(self) -> None:
        if isinstance(self.state,GameState):
            self.state.onStateExit()
        #end if
        
        self.state = None
        
        return
    #end exitState
    
    def switchState(self, state: GameState) -> None:
        self.exitState()
        self.enterState(state)
        
        return
    #end switchState
#end Game
