from SimpleGE import *
import Breakout
import Snake

class RetroRedo(Game):
    def __init__(self) -> None:
        super().__init__('Retro Redo',[800,600])
        self.states: list[GameState] = [
            Breakout.BreakoutState()
            ,Snake.SnakeState()
        ]
        self.switchState(self.states[0])

        return
    #end __init__

    def update(self) -> None:
        super().update()

        if self._state.keysDown[pg.K_SPACE]:
            self.switchState(self.states[1])

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
