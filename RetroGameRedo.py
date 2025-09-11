from SimpleGE import *
import Breakout

def main() -> None:
    game: Game = Game('Retro Game Redo',[800,600],Breakout.BreakoutState())
    game.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if