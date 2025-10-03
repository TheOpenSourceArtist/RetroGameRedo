from SimpleGE import *
    
class FroggerState(GameState):
    def __init__(self) -> None:
        super().__init__('frogger',[800,600])

        self.screenGrid: list[tuple[int]] = []
        self.cellSize: int = 40
        self.screenGridSize: list[int] = [
            int(self.renderSize[0] / self.cellSize)
            ,int(self.renderSize[1] / self.cellSize)
        ]        
        
        for gridY in range(0,self.renderSize[1], self.cellSize):
            for gridX in range(0,self.renderSize[0], self.cellSize):
                self.screenGrid.append((gridX,gridY))
            #end for
        #end for

        self.grass: RGBSurface = RGBSurface(
            pg.surface.Surface((self.cellSize,self.cellSize))
        )
        self.grass.img.fill((0,255,0))

        self.road: RGBSurface = RGBSurface(
            pg.surface.Surface((self.cellSize,self.cellSize))
        )
        self.road.img.fill((50,50,50))

        self.water: RGBSurface = RGBSurface(
            pg.surface.Surface((self.cellSize,self.cellSize))
        )
        self.water.img.fill((0,0,255))
        
        self.tileSet: list[RGBSurface] = [
            self.grass
            ,self.road
            ,self.water
        ]

        self.tileMap: list[int] = [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0
            ,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
            ,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
            ,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
            ,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
            ,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
            ,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
            ,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
            ,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ]

        self.frog: Renderable = Geometry(
            pg.math.Vector2(
                self.screenGrid[13 * 20 + 9]
            ) + [self.cellSize / 2,self.cellSize / 2]
            ,32
            ,self.cellSize / 2
            ,0
            ,(25,100,25)
        )

        self.numLives: int = 5
        self.lives: Text = Text("Lives: %d" % self.numLives,self.cellSize)

        self.entities.append(self.frog)
        self.entities.append(self.lives)
        
        return
    #end __init__
    
    def render(self) -> None:
        self.renderBuffer.fill((0,0,0))

        #render tile map
        for i in range(self.screenGridSize[0] * self.screenGridSize[1]):
            self.renderBuffer.blit(
                self.tileSet[self.tileMap[i]].img,self.screenGrid[i]
            )
        #end for

        #render entity list
        for entity in self.entities:
            if isinstance(entity,Entity):
                entity.render(self.renderBuffer)
            #end if
        #end for
        
        return
    #end render
    
    def update(self) -> None:
        
        return
    #end update
#end BreakoutState

def main() -> None:
    game: Game = Game('Frogger',[800,600],FroggerState())
    game.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if
