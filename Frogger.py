from SimpleGE import *
from random import randint, random

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
        self.velocity = pg.math.Vector2(-5,0)
        self.active = True
        self.visible = True

        return
    #end spawn
#end Car
    
class Frog(RGBSurface):
    def __init__(self, size: list[int] = [40,40], pos: list[int] = [0,0], color: list[int] = [0,100,0]) -> None:
        super().__init__(pg.surface.Surface(size))
        self.rect.topleft = pos
        self.spawnPoint: pg.Rect = pg.Rect(pos,size)
        self.img.fill((255,0,255))
        pg.draw.circle(self.img,color,[size[0]/2,size[1]/2],size[0]/2)
        self.img.set_colorkey((255,0,255))
        
        return
    #end __init__
    
    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center
        self.active = True
        self.visible = True

        return
    #end spawn
#end Frog
    
class TileGrid(Entity):
    def __init__(self, tileSet: list[pg.surface.Surface], tileMap: list[list[int]], tileSize: int = 40) -> None:
        super().__init__()
        self.tileSet: list[pg.surface.Surface] = tileSet
        self.tileMap: list[list[pg.Rect]] = tileMap
        self.cellSize: int = tileSize
        self.tiles: list[list[Renderable]] = list()
        self.mapSize: list[int] = [len(self.tileMap[0]), len(self.tileMap)]
        
        for mapRow in range(self.mapSize[1]):
            tileRow: list[Renderable] = list()
            
            for mapCol in range(self.mapSize[0]):
                tileRow.append(
                    RGBSurface(
                        self.tileSet[self.tileMap[mapRow][mapCol]]
                        ,[0,0]
                    )
                )
                tileRow[-1].rect = pg.Rect((mapCol * self.cellSize, mapRow * self.cellSize),(self.cellSize,self.cellSize))
            #end for
            self.tiles.append(tileRow)
        #end for
        
        return
    #end __init__
    
    def render(self, buffer: pg.surface.Surface) -> None:
        for tileRow in self.tiles:
            for tile in tileRow:
                tile.render(buffer)
            #end for
        #end for
        
        return
    #end render
#end TileGrid
    
class FroggerState(GameState):
    def __init__(self) -> None:
        super().__init__('frogger',[400,300])
        
        self.screenRect: pg.Rect = pg.Rect([0,0],self.renderSize)
        
        self.tileCellSize: int = int(self.renderSize[0] / 20)

        self.grass: pg.surface.Surface = pg.surface.Surface((self.tileCellSize,self.tileCellSize))
        self.grass.fill((0,255,0))

        self.road: pg.surface.Surface = pg.surface.Surface((self.tileCellSize,self.tileCellSize))
        self.road.fill((50,50,50))

        self.water: pg.surface.Surface = pg.surface.Surface((self.tileCellSize,self.tileCellSize))
        self.water.fill((0,0,255))
        
        self.tileSet: list[pg.surface.Surface] = [
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
        
        self.tileMapSize: list[int] = [len(self.tileMap),len(self.tileMap[0])]
        self.tileGrid: TileGrid = TileGrid(self.tileSet,self.tileMap,self.tileCellSize)
        
        #set up frogs
        self.frog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[13][10].rect.topleft)
        
        self.blueFrog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[1][2].rect.topleft, (0,0,100))
        self.redFrog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[1][5].rect.topleft, (100,0,0))
        self.purpleFrog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[1][8].rect.topleft, (100,0,100))
        self.yellowFrog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[1][11].rect.topleft, (200,200,0))
        self.orangeFrog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[1][14].rect.topleft, (200,100,0))
        self.pinkFrog: Frog = Frog([self.tileCellSize,self.tileCellSize], self.tileGrid.tiles[1][17].rect.topleft, (200,0,200))
        
        self.gayFrogs: EntityGroup = EntityGroup([
            self.blueFrog
            ,self.redFrog
            ,self.purpleFrog
            ,self.yellowFrog
            ,self.orangeFrog
            ,self.pinkFrog
        ])
        
        #set up gui text
        self.numLives: int = 5
        self.lives: Text = Text("LIVES: %d" % self.numLives, self.tileCellSize)
        self.timeLeft: int = 90
        self.time: Text = Text("TIME: %d" % self.timeLeft, self.tileCellSize)
        self.time.rect.right = self.renderSize[0] - 1
        
        #set up cars
        cell: pg.Rect = self.tileGrid.tiles[8][19].rect
        carSize: list[int] = [self.tileCellSize * 2, self.tileCellSize * 0.75]
        self.trucks: EntityGroup = EntityGroup()
        self.numTrucks: int = 3
        
        for i in range(self.numTrucks):
            self.trucks.add(Car(
                carSize
                ,[cell.right,cell.top + (self.tileCellSize - carSize[1])]
                , (200,200,200)
            ))
            self.trucks[-1].active = False
        #end for
            
        self.truckInd: int = 0
        self.truckSpawnPerc: float = 0.025
        
        #append the entities to the entity list
        self.entities.append(self.tileGrid)
        
        self.entities.append(self.gayFrogs)
        
        self.entities.append(self.trucks)
        
        self.entities.append(self.frog)
        
        self.entities.append(self.lives)
        self.entities.append(self.time)
        
        return
    #end __init__
    
    def update(self) -> None:
        #handle key presses
        if pg.K_UP in self.keysPressed:
            self.frog.rect.bottom -= self.tileCellSize
            
            if self.frog.rect.top < 0:
                self.frog.rect.top = 0
            #end if
        #end if
        if pg.K_DOWN in self.keysPressed:
            self.frog.rect.bottom += self.tileCellSize
            
            if self.frog.rect.bottom >= self.renderSize[1]:
                self.frog.rect.bottom = self.renderSize[1] - 1
            #end if
        #end if
        if pg.K_LEFT in self.keysPressed:
            self.frog.rect.right -= self.tileCellSize
            
            if self.frog.rect.left < 0:
                self.frog.rect.left = 0
            #end if
        #end if
        if pg.K_RIGHT in self.keysPressed:
            self.frog.rect.right += self.tileCellSize
            
            if self.frog.rect.right >= self.renderSize[0]:
                self.frog.rect.right = self.renderSize[0] - 1
            #end if
        #end if
        
        if random() <= self.truckSpawnPerc:
            if len([x for x in self.trucks if x.rect.right > 0 and x.rect.left < self.renderSize[0]]) < self.numTrucks:
                self.trucks[self.truckInd].spawn()
                self.truckInd = (self.truckInd + 1) % self.numTrucks
            #end if
        #end if
                
        #handle bounds and collisions
                
        #frog truck collision
        if any([truck.rect.colliderect(self.frog) for truck in self.trucks]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
        
        #frog water collision
        if any([any([tile.rect.colliderect(self.frog.rect) for tile in row]) for row in self.tileGrid.tiles[2:6]]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
                    
        #update gui text
        self.lives.updateText("LIVES: %d" % self.numLives)
        self.time.updateText("TIME: %d" % self.timeLeft)
        
        super().update()
        
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
