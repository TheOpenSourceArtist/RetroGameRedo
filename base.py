import pygame as pg

class Entity:
    def __init__(self, name: str = '') -> None:
        self.name: str = name
        
        if self.name == None or self.name == '':
            self.name = str(id(self))
        #end if
        
        self.active: bool = True
        self.visible: bool = True
        
        return
    #end __init__
    
    def render(self) -> None:
        
        return
    #end render
    
    def update(self) -> None:
        
        return
    #end update
#end Entity
    
class GameState(Entity):
    def __init__(self, name:str = '', renderSize: list[int] = [800,600], entities: list[Entity] = list()) -> None:
        pg.init()
        super().__init__(name)
        
        self.renderSize: list[int] = list(renderSize)
        self.renderBuffer: pg.surface.Surface = pg.surface.Surface(
            self.renderSize
        )
        self.entities: list[Entity] = entities
        self.keysDown: list[bool] = pg.key.get_pressed()
        self.mouseDown: list[bool] = pg.mouse.get_pressed()
        self.mousePos: list[int] = pg.mouse.get_pos()
        self.deltaTime: float = 0.0
        self.exitCode: int = 0
        
        return
    #end __init__
#end GameState
    
class Game(Entity):
    def __init__(self, name:str = '', displaySize: list[int] = [800,600], initialState: GameState = None) -> None:
        pg.init()
        super().__init__(name)
        pg.display.set_caption(self.name)

        self.fps: int = 60
        self.clock: pg.time.Clock = pg.time.Clock()
        self.deltaTime: float = 0.0
        self.displaySize: list[int] = displaySize
        self.display: pg.surface.Surface = pg.display.set_mode(self.displaySize)
        self.keysDown: list[bool] = pg.key.get_pressed()
        self.mouseDown: list[bool] = pg.mouse.get_pressed()
        self.mousePos: list[int] = pg.mouse.get_pos()
        self._state: GameState = initialState

        if self._state == None:
            self._state = GameState()
        #end if
        
        self.renderScale: list[float] =[
            float(self._state.renderSize[0]) / self.displaySize[0]
            ,float(self._state.renderSize[1]) / self.displaySize[1]
        ]
        self.running: bool = True 
        
        return
    #end __init__

    def handleEvents(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            #end if
        #end for
                
        self.keysDown = pg.key.get_pressed()
        self.mouseDown = pg.mouse.get_pressed()
        self.mousePos = pg.mouse.get_pos()
        self.mousePos = [
             self.mousePos[0] * self.renderScale[0]
             ,self.mousePos[1] * self.renderScale[1]
        ]

        if isinstance(self._state,GameState):
            self._state.keysDown = self.keysDown
            self._state.mouseDown = self.mouseDown
            self._state.mousePos = self.mousePos
        #end if
        
        return
    #end handleEvents

    def render(self) -> None:
        if isinstance(self._state,GameState):
            self._state.render()
            pg.transform.scale(
                self._state.renderBuffer
                ,self.displaySize
                ,self.display
            )
        #end if

        pg.display.flip()

        return
    #end render

    def update(self) -> None:
        if isinstance(self._state,GameState):
            self._state.deltaTime = self.deltaTime
            self._state.update()
        #end if

        return
    #end update

    def syncFPS(self) -> None:
        self.deltaTime = self.clock.tick(self.fps)
        
        return
    #end suncFPS

    def switchState(self, otherState: GameState) -> None:
        if isinstance(otherState, GameState):
            self._state = otherState
            self.renderScale = [
                float(self._state.renderSize[0]) / self.displaySize[0]
                ,float(self._state.renderSize[1]) / self.displaySize[1]
            ]
        #end if

        return
    #end switchState
    
    def run(self) -> None:
        while self.running == True:
            self.handleEvents()
            self.update()
            self.render()
            self.syncFPS()
        #end while

        pg.quit()
        
        return
    #end run
#end GameState

def main() -> None:
    g: Game = Game('Simple GameEngine')
    g.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if
