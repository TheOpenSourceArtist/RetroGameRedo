from SimpleGE import *
from random import randint, random
from math import ceil

class Log(RGBSurface):
    def __init__(self, size: list[int] = [50,25], pos: list[int] = [0,0], speed: int = 0) -> None:
        super().__init__(pg.surface.Surface(size),pos)
        self.img.fill((100,50,0))
        self.velocity: pg.math.Vector2 = pg.math.Vector2(-speed,0)
        self.spawnPoint: pg.Rect = pg.Rect(pos,size)

        return
    #end __init__

    def update(self, dt: float = None) -> None:
        self.rect.center += self.velocity

        return
    #end update

    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center
        self.active = True
        self.visible = True

        return
    #end spawn
#end Log

class Car(RGBSurface):
    def __init__(self, size: list[int] = [50,25], pos: list[int] = [0,0], color: list[int] = [77,77,77], speed: int = 3) -> None:
        super().__init__(pg.surface.Surface(size),pos)
        self.img.fill(color)
        self.velocity: pg.math.Vector2 = pg.math.Vector2(-speed,0)
        self.spawnPoint: pg.Rect = pg.Rect(pos,size)
        self.collisionRect: pg.Rect = self.rect.inflate(4,0)

        return
    #end __init__

    def update(self, dt: float = None) -> None:
        self.rect.center += self.velocity

        return
    #end update

    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center
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
        self.frog: Frog = Frog(
            [self.tileCellSize*0.75,self.tileCellSize*0.75]
            , self.tileGrid.tiles[13][10].rect.move([self.tileCellSize * 0.125, self.tileCellSize * 0.125]).topleft
        )
        
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
        self.timeLeft: float = 90.0
        self.time: Text = Text("TIME: %d" % ceil(self.timeLeft), self.tileCellSize)
        self.time.rect.right = self.renderSize[0] - 1
        self.numScore: int = 0
        self.score: Text = Text("SCORE: %d" % self.numScore, self.tileCellSize)
        self.score.rect.midtop = self.tileGrid.tiles[0][9].rect.midtop
        
        #set up trucks
        carSize: list[int] = [self.tileCellSize * 2, self.tileCellSize * 0.75]
        self.trucks: EntityGroup = EntityGroup()
        self.numTrucks: int = 5
        
        for i in range(self.numTrucks):
            self.trucks.add(Car(
                carSize
                , self.tileGrid.tiles[8][19].rect.move(self.tileCellSize,(self.tileCellSize - carSize[1]) / 2).topleft
                , (200,200,200)
                ,3
            ))
            self.trucks[-1].active = False
        #end for
            
        self.truckInd: int = 0
        self.truckSpawnPerc: float = 0.025
        
        #set up yellow cars
        self.yellowCars: EntityGroup = EntityGroup()
        carSize = [self.tileCellSize * 1.0, self.tileCellSize * 0.75]
        for i in range(self.numTrucks):
            self.yellowCars.add(Car(
                carSize
                ,self.tileGrid.tiles[9][0].rect.move(-self.tileCellSize * 2,(self.tileCellSize - carSize[1]) / 2).topleft
                , (200,200,100)
                ,-4.25
            ))
            self.yellowCars[-1].active = False
        #end for
            
        self.yellowCarInd: int = 0
        
        #set up purple cars
        self.purpleCars: EntityGroup = EntityGroup()
        carSize = [self.tileCellSize * 1.0, self.tileCellSize * 0.75]
        for i in range(self.numTrucks):
            self.purpleCars.add(Car(
                carSize
                ,self.tileGrid.tiles[11][19].rect.move(self.tileCellSize,(self.tileCellSize - carSize[1]) / 2).topleft
                , (200,100,200)
                ,5
            ))
            self.purpleCars[-1].active = False
        #end for
            
        self.purpleCarInd: int = 0
            
        #set up Blue cars
        self.blueCars: EntityGroup = EntityGroup()
        carSize = [self.tileCellSize * 1.0, self.tileCellSize * 0.75]
        for i in range(self.numTrucks):
            self.blueCars.add(Car(
                carSize
                ,self.tileGrid.tiles[12][0].rect.move(-self.tileCellSize * 2,(self.tileCellSize - carSize[1]) / 2).topleft
                , (100,100,255)
                ,-5.25
            ))
            self.blueCars[-1].active = False
        #end for
            
        self.blueCarInd: int = 0
        
        #set up logs
        logSize: list[int] = [randint(2,5) * self.tileCellSize,self.tileCellSize * 0.5]
        self.logs: EntityGroup = EntityGroup()
        
        for row in range(4):
            logSize = [randint(2,5) * self.tileCellSize,self.tileCellSize * 0.5]
            if row % 2 == 0:
                self.logs.add(Log(
                    logSize
                    ,self.tileGrid.tiles[2 + row][0].rect.move(-5 * self.tileCellSize,(self.tileCellSize - logSize[1]) / 2).topleft
                    ,-1.5
                ))
            else:
                self.logs.add(Log(
                    logSize
                    ,self.tileGrid.tiles[2 + row][19].rect.move(0,(self.tileCellSize - logSize[1]) / 2).topright
                    ,1.5
                ))
            #end if
            self.logs[-1].active = True
        #end for
                
        
        #append the entities to the entity list
        self.entities.append(self.tileGrid)
        
        self.entities.append(self.gayFrogs)
        
        self.entities.append(self.trucks)
        self.entities.append(self.purpleCars)
        self.entities.append(self.yellowCars)
        self.entities.append(self.blueCars)
        
        self.entities.append(self.logs)
        
        self.entities.append(self.frog)
        
        self.entities.append(self.lives)
        self.entities.append(self.time)
        self.entities.append(self.score)
        
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
        
        #spawn trucks
        if random() <= self.truckSpawnPerc:
            #truck is off screen
            if self.trucks[self.truckInd].rect.right < 0 or self.trucks[self.truckInd].rect.left >= self.renderSize[0]:
                self.trucks[self.truckInd].spawn()
                self.trucks[self.truckInd].rect.left = max([
                    x.rect.right for x in self.trucks]) + self.tileCellSize * randint(1,3)
                self.truckInd = (self.truckInd + 1) % self.numTrucks
            #end if
        #end if
        
        #spawn purple cars
        if random() <= self.truckSpawnPerc:
            if self.purpleCars[self.purpleCarInd].rect.right < 0 or self.purpleCars[self.purpleCarInd].rect.left >= self.renderSize[0]:
                self.purpleCars[self.purpleCarInd].spawn()
                self.purpleCars[self.purpleCarInd].rect.left = max([
                    x.rect.right for x in self.purpleCars]) + self.tileCellSize * randint(1,3)
                self.purpleCarInd = (self.purpleCarInd + 1) % self.numTrucks
            #end if
        #end if
                
        #spawn yellow cars
        if random() <= self.truckSpawnPerc:
            if self.yellowCars[self.yellowCarInd].rect.right < 0 or self.yellowCars[self.yellowCarInd].rect.left >= self.renderSize[0]:
                self.yellowCars[self.yellowCarInd].spawn()
                self.yellowCars[self.yellowCarInd].rect.right = min([
                    x.rect.left for x in self.yellowCars]) - self.tileCellSize * randint(1,3)
                self.yellowCarInd = (self.yellowCarInd + 1) % self.numTrucks
            #end if
        #end if
                
        #spawn Blue cars
        if random() <= self.truckSpawnPerc:
            if self.blueCars[self.blueCarInd].rect.right < 0 or self.blueCars[self.blueCarInd].rect.left >= self.renderSize[0]:
                self.blueCars[self.blueCarInd].spawn()
                self.blueCars[self.blueCarInd].rect.right = min([
                    x.rect.left for x in self.blueCars]) - self.tileCellSize * randint(1,3)
                self.blueCarInd = (self.blueCarInd + 1) % self.numTrucks
            #end if
        #end if
                
        #handle bounds and collisions
                
        #frog truck collision
        if any([truck.rect.colliderect(self.frog) for truck in self.trucks]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
            
            
        #frog purple Car collision
        if any([car.rect.colliderect(self.frog) for car in self.purpleCars]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
            
        #frog yellow Car collision
        if any([car.rect.colliderect(self.frog) for car in self.yellowCars]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
            
        #frog Blue Car collision
        if any([car.rect.colliderect(self.frog) for car in self.blueCars]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
        
        #frog water/log/turtle collision
        if any([log.rect.colliderect(self.frog) for log in self.logs]):
            pass
        elif any([any([tile.rect.colliderect(self.frog.rect) for tile in row]) for row in self.tileGrid.tiles[2:6]]):
            self.frog.spawn()
            self.numLives -= 1
            self.lives.updateText("LIVES: %d" % self.numLives)
        #end if
                    
        #update gui text
        self.timeLeft -= (self.deltaTime / 1000)
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
