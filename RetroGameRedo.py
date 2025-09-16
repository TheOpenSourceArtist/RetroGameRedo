from SimpleGE import *
import Breakout
import Snake

class RetroRedo(Game):
    def __init__(self) -> None:
        super().__init__('Retro Redo',[800,600])
        self.states: list[GameState] = [
            #Break Out States
            Breakout.Menu()
            ,Breakout.BreakoutState()
            ,Breakout.EndGame()
            
            #Snake States
            ,Snake.SnakeState()
        ]
        self.stateIndex: int = 1
        self.switchState(self.states[self.stateIndex])

        return
    #end __init__

    def update(self) -> None:
        super().update()
        
        if self.keysDown[pg.K_ESCAPE]:
            self.running = False
        #end if
        
        if self._state.name == 'breakout' and self._state.exitCode == 1:
            self.switchState(self.states[0])
        elif self._state.name == 'breakout' and self._state.exitCode == 2:
            self.switchState(self.states[2])
        #end if

        return
    #end update
#end RetroRedo

def main() -> None:
    game: Game = RetroRedo()
    game.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if
