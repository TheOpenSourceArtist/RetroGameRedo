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
    def __init__(self, name:str = '', renderSize: list[int] = [800,600]) -> None:
        pg.init()
        super().__init__(name)
        
        self.renderSize: list[int] = list(renderSize)
        self.renderBuffer: pg.surface.Surface = pg.surface.Surface(
            self.renderSize
        )
        self.keysDown: list[bool] = pg.key.get_pressed()
        self.mouseDown: list[bool] = pg.mouse.get_pressed()
        self.mousePos: list[int] = pg.mouse.get_pos()
        self.entities: list[Entity] = list()
        self.deltaTime: float = 0.0
        
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
        self.__state: GameState = initialState

        if self.__state == None:
            self.__state = GameState()
        #end if
        
        self.renderScale: list[float] =[
            float(self.__state.renderSize[0]) / self.displaySize[0]
            ,float(self.__state.renderSize[1]) / self.displaySize[1]
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

        if isinstance(self.__state,GameState):
            self.__state.keysDown = pg.key.get_pressed()
            self.__state.mouseDown = pg.mouse.get_pressed()
            self.__state.mousePos = pg.mouse.get_pos()
            self.__state.mousePos = [
                 self.__state.mousePos[0] * self.renderScale[0]
                 ,self.__state.mousePos[1] * self.renderScale[1]
            ]
        #end if
        
        return
    #end handleEvents

    def render(self) -> None:
        if isinstance(self.__state,GameState):
            self.__state.render()
            pg.transform.scale(
                self.__state.renderBuffer
                ,self.displaySize
                ,self.display
            )
        #end if

        pg.display.flip()

        return
    #end render

    def update(self) -> None:
        if isinstance(self.__state,GameState):
            self.__state.deltaTime = self.deltaTime
            self.__state.update()
        #end if

        return
    #end update

    def syncFPS(self) -> None:
        self.deltaTime = self.clock.tick(self.fps)
        
        return
    #end suncFPS

    def switchState(self, otherState: GameState) -> None:
        if isinstance(otherState, GameState):
            self.__state = otherState
        #end if

        return
    #end switchState
    
    def run(self) -> None:
        if isinstance(self.__state,GameState):
            while self.running == True:
                self.handleEvents()
                self.update()
                self.render()
                self.syncFPS()
            #end while
        #end if

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
