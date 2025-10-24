from SimpleGE import *

class Car(RGBSurface):
    def __init__(self, size: list[int] = [50,25], pos: list[int] = [0,0], color: list[int] = [77,77,77]) -> None:
        super().__init__(pg.surface.Surface(size),pos)
        self.img.fill(color)
        self.velocity: pg.math.Vector2 = pg.math.Vector2(-5,0)
        self.spawnPoint: pg.Rect = pg.Rect(pos,size)

        return
    #end __init__

    def update(self, dt: float = None) -> None:
        self.rect.center += self.velocity

        return
    #end update

    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center

        return
    #end spawn
#end Car
    
class FroggerState(GameState):
    def __init__(self) -> None:
        super().__init__('frogger',[800,600])
        
        self.tileCellSize: int = 40

        self.grass: RGBSurface = RGBSurface(
            pg.surface.Surface((self.tileCellSize,self.tileCellSize))
        )
        self.grass.img.fill((0,255,0))

        self.road: RGBSurface = RGBSurface(
            pg.surface.Surface((self.tileCellSize,self.tileCellSize))
        )
        self.road.img.fill((50,50,50))

        self.water: RGBSurface = RGBSurface(
            pg.surface.Surface((self.tileCellSize,self.tileCellSize))
        )
        self.water.img.fill((0,0,255))
        
        self.tileSet: list[RGBSurface] = [
            self.grass
            ,self.road
            ,self.water
        ]

        self.tileMap: list[list[int]] = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ,[0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0]
            ,[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
            ,[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
            ,[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
            ,[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
            ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        
        self.tileGrid: list[list[pg.Rect]] = list()
        self.tileGridSize: list[int] = [
            len(self.tileMap[0])
            ,len(self.tileMap)
        ]
        
        for gridY in range(self.tileGridSize[1]):
            gridRow: list[pg.Rect] = list()
            
            for gridX in range(self.tileGridSize[0]):
                gridRow.append(pg.Rect(
                    (gridX * self.tileCellSize, gridY * self.tileCellSize)
                    ,(self.tileCellSize, self.tileCellSize)
                ))
            #end for
            
            self.tileGrid.append(gridRow)
        #end for

        self.frogPos: list[int] = [9,13]
        self.frog: Renderable = Geometry(
            self.tileGrid[self.frogPos[1]][self.frogPos[0]].center
            ,32
            ,self.tileCellSize / 2
            ,0
            ,(25,100,25)
        )

        self.numLives: int = 5
        self.lives: Text = Text("Lives: %d" % self.numLives,self.tileCellSize)

        self.entities.append(self.frog)
        self.entities.append(self.lives)

        self.car: Car = Car(
            [self.tileCellSize * 1.75, self.tileCellSize * 0.75]
            ,self.tileGrid[8][-2].topleft
            ,[200,200,200]
        )
        self.car.rect.center = self.tileGrid[8][-1].center
        self.car.spawnPoint.midleft = self.tileGrid[8][-1].midright
        self.entities.append(self.car)
        
        return
    #end __init__
    
    def render(self) -> None:
        #self.renderBuffer.fill((0,0,0))

        #render tile map
        for tileY in range(self.tileGridSize[1]):
            for tileX in range(self.tileGridSize[0]):
                self.renderBuffer.blit(self.tileSet[self.tileMap[tileY][tileX]].img,self.tileGrid[tileY][tileX])
            #end for
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
        super().update()
        
        if pg.K_UP in self.keysPressed:
            self.frogPos[1] -= 1
            
            if self.frogPos[1] < 0:
                self.frogPos[1] = 0
            #end if
        #end if
                
        if pg.K_DOWN in self.keysPressed:
            self.frogPos[1] += 1
            
            if self.frogPos[1] >= self.tileGridSize[1]:
                self.frogPos[1] = self.tileGridSize[1] - 1
            #end if
        #end if
                
        if pg.K_RIGHT in self.keysPressed:
            self.frogPos[0] += 1
            
            if self.frogPos[0] >= self.tileGridSize[0]:
                self.frogPos[0] = self.tileGridSize[0] - 1
            #end if
        #end if
                
        if pg.K_LEFT in self.keysPressed:
            self.frogPos[0] -= 1
            
            if self.frogPos[0] < 0:
                self.frogPos[0] = 0
            #end if
        #end if
        
        self.frog.center = self.tileGrid[self.frogPos[1]][self.frogPos[0]].center

        #check for frog on car collision
        if self.car.rect.collidepoint(self.frog.center):
            self.car.spawn()
            self.numLives -= 1
            self.lives.updateText("Lives: %d" % self.numLives)
            self.frogPos = [9,13]
            self.frog.center = self.tileGrid[self.frogPos[1]][self.frogPos[0]].center
        #end if
        
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
