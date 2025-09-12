from SimpleGE import *

class SnakeState(GameState):
    def __init__(self) -> None:
        super().__init__()

        return
    #end __init__

    def render(self) -> None:
        self.renderBuffer.fill((22,4,75))
        
        return
    #end render
#end SnakeState
	
def main() -> None:
        myGame: Game = Game(
                name = 'Snake'
                ,displaySize = [800,600]
                ,initialState = SnakeState()
        )
        
        myGame.run()

        return
#end main

if __name__ == '__main__':
        main()
#end if
