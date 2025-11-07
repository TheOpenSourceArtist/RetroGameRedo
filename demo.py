from SimpleGE import *
from random import randint

class Square(RGBSurface):
    def __init__(self) -> None:
        super().__init__(pg.surface.Surface((20,20)))
        self.img.fill((255,0,0))

        return
    #end __init__
#end Square

class TestState(GameState):
    def __init__(self) -> None:
        super().__init__('Test')
        self.square: Square = Square()
        self.entities.append(self.square)

        return
    #end __init__

    def update(self) -> None:
        super().update()

        if pg.K_SPACE in self.keysPressed:
##        if self.keysDown[pg.K_SPACE]:
            self.square.rect.center = [randint(0,800),randint(0,600)]

        return
    #end update
#end TestState

def main() -> None:
    game: Game = Game('SimpleGE Demo',[800,600])
    game.switchState(TestState())
    game.run()

    return
#end main

if __name__ == '__main__':
    main()
#end if
