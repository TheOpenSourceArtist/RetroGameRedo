from SimplerGE import *
from random import choices, choice, randint
from PIL import Image

GAMESTATE_MENU: int = 0
GAMESTATE_PLAY_1P: int = 1
GAMESTATE_PLAY_2P: int = 2
GAMESTATE_HIGH_SCORE: int = 3

class Frog(Entity):
    def __init__(self, spawnPoint: list[int] = [0,0]) -> None:
        super().__init__((spawnPoint,(16,16)),pg.image.load('gfx/frog16x16.bmp'))
        self.speed: int = 20
        self.spawnPoint: pg.Rect = pg.Rect(self.rect)
        self.states: list[pg.surface.Surface] = [
            self.img
            ,pg.transform.rotate(self.img,90)
            ,pg.transform.rotate(self.img,180)
            ,pg.transform.rotate(self.img,270)
        ]
        self.state: int = 0
        
        for state in self.states:
            state.set_colorkey(SGE_COLORKEY_DEFAULT)
        #end for
        
        self.mount: pg.Rect = None
        self.collisionRect: pg.Rect = self.rect.inflate(-7,-7)
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        if isinstance(self.mount,Entity):
            self.rect.center += self.mount.velocity
        #end if
            
        self.collisionRect.center = self.rect.center
        
        return
    #end update
    
    def render(self, renderBuffer:pg.surface.Surface) -> None:
        renderBuffer.blit(self.states[self.state],self.rect)
        pg.draw.rect(renderBuffer,(255,255,255),self.collisionRect, 1)
        
        return
    #end render
    
    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center
        self.state = 0
        
        return
    #end spawn
    
    def collide(self, other: pg.Rect) -> bool:
        
        return self.collisionRect.colliderect(other)
#end Frog
    
class GayFrogs(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,20,20),pg.image.load('gfx/gayFrogs.bmp'))
        imgSize: list[int] = self.img.get_size()
        self.frogs: list[pg.surface.Surface] = [
            self.img.subsurface(x,y,20,20)
            for y in range(0,imgSize[1],20)
            for x in range(0,imgSize[0],20)
        ]
        self.numStates: int = len(self.frogs)
        self.rects: list[pg.Rect] = [pg.Rect(60 * i + 40,40,20,20) for i in range(self.numStates -1)]
        self.states: int = [choice(list(range(1, self.numStates))) for i in range(self.numStates - 1)]
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for i in range(self.numStates - 1):
            renderBuffer.blit(self.frogs[self.states[i]],self.rects[i])
        
        return
    #end render
    
    def collide(self, other: pg.Rect) -> bool:
        for i in range(self.numStates - 1):
            if self.states[i] != 0 and self.rects[i].colliderect(other):
                self.states[i] = 0
                return True
            #end if
        #end for
        
        return False
    #end collide
    
    def reset(self) -> None:
        self.states: int = [choice(list(range(1, self.numStates))) for i in range(self.numStates - 1)]
        
        return
    #end reset
#end GayFrogs
    
class TrafficLine(Entity):
    def __init__(self, carRect:pg.Rect, imgPath: str, speed: float, spawnChance: float, numCars: int, spacing: int) -> None:
        super().__init__(carRect,pg.image.load(imgPath),(speed,0))
        self.numCars: int = numCars
        self.spacing: int = spacing
        self.rects: list[pg.Rect] = [self.rect.move(self.spacing * i,0) for i in range(self.numCars)]
        self.spawnChance: list[float] = [spawnChance,1 - spawnChance]
        self.onRoad: list[bool] = [choices((True,False),self.spawnChance)[0] for i in range(self.numCars)]
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        for rect in self.rects:
            rect.center += self.velocity
        #end for
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for i in range(self.numCars):
            if self.onRoad[i]:
                renderBuffer.blit(self.img,self.rects[i])
            #end if
        #end for
        
        return
    #end render
    
    def spawn(self, carIndex: int) -> None:
        self.onRoad[carIndex] = choices((True,False),self.spawnChance)[0]
        
        return
    #end onRoad
    
    def collide(self, other: pg.Rect) -> bool:
        for i in range(self.numCars):
            if self.onRoad[i] and self.rects[i].colliderect(other):
                return True
            #end if
        #end for
        
        return False
    #end collide
#end TrafficLine
    
class Log(Entity):
    def __init__(self, size: int = 2, pos: list[int] = [0,0], velocity: list[int] = [0,0]) -> None:
        super().__init__((0,0,20,10),vel = velocity)
        self.tileSet: pg.surface.Surface = pg.image.load("gfx/log.bmp")
        self.tiles: list[pg.surface.Surface] = [
            self.tileSet.subsurface((x,y,self.rect.w,self.rect.h))
            for y in range(0,self.tileSet.get_size()[1], self.rect.h)
            for x in range(0,self.tileSet.get_size()[0], self.rect.w)
        ]
        
        for tile in self.tiles:
            tile.set_colorkey(SGE_COLORKEY_DEFAULT)
        #end for
            
        self.size: int = size
        self.segments: list[int] = [0,2]
        
        while len(self.segments) < self.size:
            self.segments.insert(-1,1)
        #end while
            
        self.rect.w = 20 * size
        self.img = pg.surface.Surface(self.rect.size)
        
        for i in range(size):
            self.img.blit(self.tiles[self.segments[i]],(20 * i,0))
        #end for
        
        return
    #end __init__
    
    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center
        
        return
    #end spawn
    
    def collide(self, other: pg.Rect) -> bool:
        
        return self.rect.colliderect(other)
    #end collide
#end Log
    
class Turtle(Entity):
    def __init__(self, flipped: bool = False) -> None:
        super().__init__((0,0,20,20),pg.image.load('gfx/turtle.bmp'))
        self.states: list[pg.surface.Surface] = [
            self.img.subsurface((x,y,20,20))
            for y in range(0,self.img.get_size()[1],20)
            for x in range(0, self.img.get_size()[0],20)
        ]
        self.states.extend([
            pg.transform.rotate(self.img.subsurface((x,y,20,20)),180)
            for y in range(0,self.img.get_size()[1],20)
            for x in range(0, self.img.get_size()[0],20)
        ])
        
        for state in self.states:
            state.set_colorkey(SGE_COLORKEY_DEFAULT)
        #end for
            
        self.stateNum: int = 0
        self.numStates: int = int(len(self.states)/2)
        self.stateTimer: int = 200
        self.stateTimeDelta: int = 0
        self.offset: int = 0
        self.flipped: bool = flipped
            
        self.diving: bool = False
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        if self.flipped:
            self.offset = self.numStates
        else:
            self.offset = 0
        #end if
            
        if randint(1,100) < 10:
            self.diving = True
        #end if
        
        self.stateTimeDelta += deltaTime
        
        if self.stateTimeDelta >= self.stateTimer:
            if self.diving:
                self.stateTimeDelta = 0
                self.stateNum = ((self.stateNum + 1) % self.numStates) + self.offset
            #end if
        #end if
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        renderBuffer.blit(self.states[self.stateNum], self.rect)
        
        return
    #end render
    
    def collide(self, other: pg.Rect) -> bool:
        
        return self.rect.colliderect(other)
    #end collide
#end Turtle
    
class Gator(Entity):
    def __init__(self, flipped = False) -> None:
        super().__init__((0,0,60,20),pg.image.load('gfx/gator.bmp'))
        self.states: list[pg.surface.Surface] = [
            self.img.subsurface((x,y,60,20))
            for y in range(0,self.img.get_size()[1],20)
            for x in range(0, self.img.get_size()[0],60)
        ]
        self.states.extend([
            pg.transform.rotate(self.img.subsurface((x,y,60,20)),180)
            for y in range(0,self.img.get_size()[1],20)
            for x in range(0, self.img.get_size()[0],60)
        ])
        
        for state in self.states:
            state.set_colorkey(SGE_COLORKEY_DEFAULT)
        #end for
            
        self.stateNum: int = 0
        self.numStates: int = int(len(self.states)/2)
        self.stateTimer: int = 200
        self.stateTimeDelta: int = 0
        self.offset: int = 0
        self.flipped: bool = flipped
        
        self.head: Entity = Entity((0,0,6,10))
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        if self.flipped:
            self.offset = self.numStates
            self.head.rect.midright = self.rect.midright
        else:
            self.offset = 0
            self.head.rect.midleft = self.rect.midleft
        #end if
        
        self.stateTimeDelta += deltaTime
        
        if self.stateTimeDelta >= self.stateTimer:
            self.stateTimeDelta = 0
            self.stateNum = ((self.stateNum + 1) % self.numStates) + self.offset
        #end if
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        renderBuffer.blit(self.states[self.stateNum], self.rect)
        pg.draw.rect(renderBuffer,(255,255,255),self.head.rect,1)
        
        return
    #end render
    
    def collide(self, other: pg.Rect) -> bool:
        
        return self.rect.colliderect(other)
    #end collide
#end Gator
    
class RiverEntity(Entity):
    def __init__(self, flipped: bool = False) -> None:
        super().__init__()
        self.states: list[Entity] = [
            Log(4)
            ,Log(3)
            ,Log(2)
            ,Gator(flipped)
            ,Turtle(flipped)
        ]
        self.numStates: int = len(self.states)
        self.stateNum: int = randint(0,self.numStates - 1)
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        if self.states[self.stateNum].visible:
            self.states[self.stateNum].render(renderBuffer)
        #end if
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        self.states[self.stateNum].rect.center = self.rect.center
        self.states[self.stateNum].visible = self.visible
        self.states[self.stateNum].update(deltaTime)
        
        return
    #end render
    
    def changeState(self) -> None:
        self.stateNum: int = randint(0,self.numStates - 1)
        
        return
    #end changeState
#end RiverEntity
    
class RiverLine(Entity):
    def __init__(self, rect:pg.Rect, speed: float = 1) -> None:
        super().__init__(rect,vel=(speed, 0))
        self.numRiverRects: int = 6
        self.riverRects: list[pg.Rect] = [
            self.rect.move(0,0)
            for i in range(self.numRiverRects)
        ]
        self.riverEntities: list[RiverEntity] = list()
        
        if speed < 0:
            for i in range(1,self.numRiverRects):
                self.riverRects[i].midleft = self.riverRects[i-1].midright
                self.riverEntities.append(RiverEntity(False))
                self.riverEntities[-1].visible = choice((True,False))
            #end for
                
            self.riverEntities.append(RiverEntity(False))
            self.riverEntities[-1].visible = choice((True,False))
        else:
            for i in range(1,self.numRiverRects):
                self.riverRects[i].midright = self.riverRects[i-1].midleft
                self.riverEntities.append(RiverEntity(True))
                self.riverEntities[-1].visible = choice((True,False))
            #end for
                
            self.riverEntities.append(RiverEntity(True))
            self.riverEntities[-1].visible = choice((True,False))
        #end if
        
        return
    #end __init__
    
    def collide(self, other: pg.Rect) -> None:
        for i in range(self.numRiverRects):
            stateNum = self.riverEntities[i].stateNum
            entity = self.riverEntities[i].states[stateNum]
            
            if entity.visible and entity.collide(other):
                return True
            #end if
        #end for
        
        return False
    #end collide
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for i in range(self.numRiverRects):
            stateNum = self.riverEntities[i].stateNum
            entity = self.riverEntities[i].states[stateNum]
            pg.draw.rect(renderBuffer,(255,255,255),entity.rect,1)
            self.riverEntities[i].render(renderBuffer)
        #end for
        
        return
    #end render
    
    def update(self, deltaTime:float) -> None:
        for i in range(self.numRiverRects):
            self.riverRects[i].center += self.velocity
            self.riverEntities[i].rect.center = self.riverRects[i].center
            self.riverEntities[i].update(deltaTime)
        #end for
        
        return
    #end update
    
    def handleBounds(self, bounds: pg.Rect) -> None:
        if self.velocity.x < 0:
            for i in range(self.numRiverRects):
                if self.riverRects[i].right < 0:
                    self.riverRects[i].left = bounds.w - 1
                    self.riverEntities[i].changeState()
                    self.riverEntities[i].visible = choice((True,False))
                #end if
            #end for
        else:
            for i in range(self.numRiverRects):
                if self.riverRects[i].left >= bounds.w:
                    self.riverRects[i].right = 0
                    self.riverEntities[i].changeState()
                    self.riverEntities[i].visible = choice((True,False))
                #end if
            #end for
        #end if
            
        return
    #end handleBounds
#end RiverLine
    
class BloodSport(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,10,10))
        self.img.fill(SGE_COLORKEY_DEFAULT)
        pg.draw.circle(self.img,(100,0,25),self.rect.center,self.rect.w/2)
        self.visible = False
        self.numSpots: int = 5
        self.spots: list[pg.surface.Surface] = [
            Entity((0,0,5,5))
            for x in range(self.numSpots)
        ]
        
        for spot in self.spots:
            v: pg.math.Vector2 = pg.math.Vector2.from_polar([randint(5,10),randint(0,359)])
            spot.img.fill(SGE_COLORKEY_DEFAULT)
            pg.draw.circle(spot.img,(100,0,25),spot.rect.center,2)
            spot.rect.center = v
        #end for
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        super().render(renderBuffer)
        
        for spot in self.spots:
            renderBuffer.blit(spot.img,(self.rect.centerx + spot.rect.centerx, self.rect.centery + spot.rect.centery))
        #end for
        
        return
    #end render
#end BloodSport
    
class Header(Entity):
    def __init__(self, size: list[int] = [400,20]) -> None:
        super().__init__(((0,0),size))
        self.font: pg.font.Font = pg.font.Font(size=self.rect.h)
        
        self.lives: Entity = Entity()
        self.numLives: int = 5
        self.lives.img = self.font.render("LIVES: %d" % self.numLives, False, (255,255,255))
        self.lives.rect = self.lives.img.get_rect()
        
        self.score: Entity = Entity()
        self.numScore: int = 0
        self.score.img = self.font.render("SCORE: %s" % format(self.numScore,'0=6d'), False, (255,255,255))
        self.score.rect = self.score.img.get_rect()
        self.score.rect.centerx = self.rect.centerx
        
        self.time: Entity = Entity()
        self.numSeconds: int = 100
        self.time.img = self.font.render("TIME: %s" % format(self.numSeconds,'0=3d'), False, (255,255,255))
        self.time.rect = self.time.img.get_rect()
        self.time.rect.right = self.rect.right
        
        self.curTime: int = 0
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        self.lives.render(renderBuffer)
        self.score.render(renderBuffer)
        self.time.render(renderBuffer)
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        self.curTime += deltaTime
        
        if self.curTime >= 1000:
            self.numSeconds -= 1
            self.curTime = 0
            self.time.img = self.font.render("TIME: %s" % format(self.numSeconds,'0=3d'), False, (255,255,255))
        #end if
            
        self.score.img = self.font.render("SCORE: %s" % format(self.numScore,'0=6d'), False, (255,255,255))
        self.lives.img = self.font.render("LIVES: %d" % self.numLives, False, (255,255,255))
        
        return
    #end update
#end Header
    
class TileBG(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,20,20))
        self.tileSet: pg.surface.Surface = pg.image.load("gfx/tileSet.bmp")
        self.tiles: list[pg.surface.Surface] = [
            self.tileSet.subsurface((x,y,self.rect.w,self.rect.h))
            for y in range(0,self.tileSet.get_size()[1], self.rect.h)
            for x in range(0,self.tileSet.get_size()[0], self.rect.w)
        ]
        self.tileGridSize: list[list] = [20,15]
        self.tileGrid: list[list[int]] = [
            [pg.Rect(x * self.rect.w, y * self.rect.h,20,20) for x in range(self.tileGridSize[0])]
            for y in range(self.tileGridSize[1])
        ]
        self.tileMap: list[int] = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ,[1,1,2,5,1,2,1,1,2,1,1,2,5,1,2,5,1,2,1,1]
            ,[2,4,7,2,2,7,2,2,7,4,2,7,2,2,7,2,2,7,4,2]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[1,5,1,1,1,1,1,1,5,1,1,1,5,1,1,1,5,5,1,1]
            ,[1,1,1,1,1,5,1,1,1,1,1,1,1,5,1,1,1,1,1,5]
            ,[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
            ,[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
            ,[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
            ,[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
            ,[1,1,1,5,1,5,1,1,5,1,1,1,1,1,5,1,1,5,1,1]
            ,[1,5,1,1,1,1,1,1,1,1,5,1,1,1,1,1,5,1,1,5]
        ]
        
        for y in range(self.tileGridSize[1]):
            for x in range(self.tileGridSize[0]):
                if self.tileMap[y][x] == 1 or self.tileMap[y][x] == 5:
                    self.tileMap[y][x] = choice([1,5])
        
        self.waterTileOffset: int = 0
        self.waterFrameDelay: int = 400
        self.waterDT: int = 0
        self.numWaterTiles: int = 4
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for row in range(self.tileGridSize[1]):
            for col in range(self.tileGridSize[0]):
                if self.tileMap[row][col] == 7:
                    renderBuffer.blit(self.tiles[self.tileMap[row][col] + self.waterTileOffset],self.tileGrid[row][col])
                else:
                    renderBuffer.blit(self.tiles[self.tileMap[row][col]],self.tileGrid[row][col])
                #end if
            #end for
        #end for
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        self.waterDT += deltaTime
        if self.waterDT >= self.waterFrameDelay:
            self.waterDT: int = 0
            self.waterTileOffset = (self.waterTileOffset + 1) % self.numWaterTiles
        #end if
        
        return
    #end update
#end Tile
    
class Logo(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,252,46), pg.image.load('gfx/froggerLogo.bmp'))
        self.frames: list[pg.surface.Surface] = list()
        
        for frameRow in range(0,self.img.get_size()[1],self.rect.h):
            for frameCol in range(0,self.img.get_size()[0],self.rect.w):
                self.frames.append(self.img.subsurface((frameCol,frameRow,self.rect.w,self.rect.h)))
            #end for
        #end for
        
        self.frameNum: int = 0
        self.numFrames: int = len(self.frames)
        self.frameTimer: int = 200
        self.frameTimeDelta: int = 0
        self.angle: float = -5
        self.dangle: float = 0.0
        self.ddangle: float = 0.1
        self.maxAngleDelta: int = 5
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        rotated: pg.surface.Surface = pg.transform.rotate(self.frames[self.frameNum],self.angle)
        rotated.set_colorkey(SGE_COLORKEY_DEFAULT)
        rotatedRect: pg.Rect = rotated.get_rect()
        rotatedRect.center = self.rect.center
        renderBuffer.blit(rotated, rotatedRect)
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        self.frameTimeDelta += deltaTime
        
        if self.frameTimeDelta >= self.frameTimer:
            self.frameTimeDelta = 0
            self.frameNum = (self.frameNum + 1) % self.numFrames
        #end if
        
        self.dangle += self.ddangle
        self.angle += self.dangle
        
        if self.dangle >= 1:
            self.ddangle *= -1
        elif self.dangle <= -1:
            self.ddangle *= -1
        #end if
        
        return
    #end update
#end Logo
    
class Selector(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,225,35))
        self.leftFrog: Frog = Frog()
        self.rightFrog: Frog = Frog()
        
        self.frogStateTimer: int = 500
        self.frogStateTimeDelta: int = 0
        self.frogState: int = 0
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        self.leftFrog.render(renderBuffer)
        self.rightFrog.render(renderBuffer)
        
        return
    #end render
    
    def update(self, deltaTime:float) -> None:
        self.leftFrog.rect.midright = self.rect.midleft
        self.rightFrog.rect.midleft = self.rect.midright
        
        self.frogStateTimeDelta += deltaTime
        
        if self.frogStateTimeDelta >= self.frogStateTimer:
            self.frogStateTimeDelta = 0
            self.frogState = (self.frogState + 1) % 4
            self.leftFrog.state = self.frogState
            self.rightFrog.state = self.frogState
        #end if
        
        return
    #end update
#end Selector
    
class Menu(GameState):
    def __init__(self) -> None:
        super().__init__([400,300])
        self.tileBG: TileBG = TileBG()
        
        self.tileBG.tileMap = [
            [2,4,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,4,2]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,5,1,1,1,1,1,1,5,1,1,1,5,1,1,1,5,5,1,1]
            ,[1,1,1,1,1,5,1,1,1,1,1,1,1,5,1,1,1,1,1,5]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ,[1,1,1,5,1,5,1,1,5,1,1,1,1,1,5,1,1,5,1,1]
            ,[1,5,1,1,1,1,1,1,1,1,5,1,1,1,1,1,5,1,1,5]
            ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        
        for row in range(self.tileBG.tileGridSize[1]):
            for col in range(self.tileBG.tileGridSize[0]):
                if self.tileBG.tileMap[row][col] in (1,5):
                    self.tileBG.tileMap[row][col] = choice([5,1])
                #end if
            #end for
        #end for
        
        self.logo: Logo = Logo()
        self.logo.rect.midtop = self.rect.midtop
        self.logo.rect.y += self.logo.rect.h * 0.5
        
        self.player1: Entity = Entity((0,0,162,31),pg.image.load('gfx/1player.bmp'))
        self.player1.rect.midtop = self.logo.rect.midbottom
        self.player1.rect.y += self.player1.rect.h * 2
        
        self.player2: Entity = Entity((0,0,163,33),pg.image.load('gfx/2player.bmp'))
        self.player2.rect.midtop = self.player1.rect.midbottom
        self.player2.rect.y += self.player2.rect.h * 0.5
        
        self.highScore: Entity = Entity((0,0,210,33),pg.image.load('gfx/highScore.bmp'))
        self.highScore.rect.midtop = self.player2.rect.midbottom
        self.highScore.rect.y += self.highScore.rect.h * 0.5
        
        self.selector: Selector = Selector()
        self.selector.rect.center = self.player1.rect.center
        self.selectorRects: list[pg.Rect] = [
            self.player1.rect
            ,self.player2.rect
            ,self.highScore.rect
        ]
        self.selectorRectNum: int = 0
        
        self.entities.append(self.tileBG)
        self.entities.append(self.logo)
        self.entities.append(self.player1)
        self.entities.append(self.player2)
        self.entities.append(self.highScore)
        self.entities.append(self.selector)
        
        return
    #end __init__
    
    def update(self, deltaTime:float) -> None:
        super().update(deltaTime)
        self.selector.rect = self.selectorRects[self.selectorRectNum] 
        
        return
    #end update
    
    def onKeyPressed(self, key: int) -> None:
        if key == pg.K_DOWN:
            self.selectorRectNum = (self.selectorRectNum + 1) % 3
            self.selector.rect = self.selectorRects[self.selectorRectNum]
        elif key == pg.K_UP:
            self.selectorRectNum -= 1
            
            if self.selectorRectNum < 0:
                self.selectorRectNum = 2
            #end if
                
            self.selector.rect = self.selectorRects[self.selectorRectNum]
        #end if        
        
        return
    #end onKeyPressed
    
    def onKeyReleased(self, key: int) -> None:
        if key == pg.K_SPACE or key == pg.K_RETURN:
            if self.selector.collide(self.player1):
                self.exitCode = 1
        
        return
    #end onKeyReleased
#end Menu

class Play(GameState):
    def __init__(self) -> None:
        super().__init__([400,300])
        
        #set up background tiles
        self.bg: TileBG = TileBG()
        logSize: int = 3
        self.riverRow1: RiverLine = RiverLine((-80,60,80,20),1)
        self.riverRow2: RiverLine = RiverLine((400,80,80,20),-1)
        self.riverRow3: RiverLine = RiverLine((-80,100,80,20),1)
        self.riverRow4: RiverLine = RiverLine((400,120,80,20),-1)
        self.semis: TrafficLine = TrafficLine((400,180,60,20), 'gfx/truck.bmp', -1, 0.5, 5, 100)
        self.redCars: TrafficLine = TrafficLine((-30,202,30,16), 'gfx/redCar.bmp',3,0.5,6,-80)
        self.purpleCars: TrafficLine = TrafficLine((399,222,38,16),'gfx/purpleCar.bmp',-2,0.5,6,80)
        self.trucks: TrafficLine = TrafficLine((-36,242,36,16),'gfx/yellowTruck.bmp',2,0.5,6,-80)
        self.gayFrogs: GayFrogs = GayFrogs()
        self.frog: Frog = Frog(self.bg.tileGrid[13][9].topleft)
        self.header: Header = Header()
        self.blood: BloodSport = BloodSport()
        
        self.entities.append(self.bg)
        self.entities.append(self.riverRow1)
        self.entities.append(self.riverRow2)
        self.entities.append(self.riverRow3)
        self.entities.append(self.riverRow4)
        self.entities.append(self.blood)
        self.entities.append(self.semis)
        self.entities.append(self.redCars)
        self.entities.append(self.purpleCars)
        self.entities.append(self.trucks)
        self.entities.append(self.gayFrogs)
        self.entities.append(self.frog)
        self.entities.append(self.header)
        
        return
    #end __init__
    
    def onKeyPressed(self, key: int) -> None:
        if key == pg.K_RIGHT:
            self.frog.state = 3
            self.frog.rect.x += self.frog.speed
            
            if self.frog.rect.right >= self.rect.w:
                self.frog.rect.right = self.rect.w - 1
            #end if
        #end if
        
        if key == pg.K_LEFT:
            self.frog.state = 1
            self.frog.rect.x -= self.frog.speed
            
            if self.frog.rect.left < 0:
                self.frog.rect.left = 0
            #end if
        #end if
            
        if key == pg.K_UP:
            self.frog.state = 0
            self.frog.rect.y -= self.frog.speed
            
            if self.frog.rect.top <= self.bg.rect.h:
                self.frog.rect.top = self.bg.rect.h
            #end if
        #end if
            
        if key == pg.K_DOWN:
            self.frog.state = 2
            self.frog.rect.y += self.frog.speed
            
            if self.frog.rect.bottom >= self.rect.h:
                self.frog.rect.bottom = self.rect.h - 1
            #end if
        #end if
        
        if self.frog.mount == None:
            #snap frog center to tile grid
            tileX: int = int(self.frog.rect.x / self.bg.rect.w)
            tileY: int = int(self.frog.rect.y / self.bg.rect.w)
            self.frog.rect.center = self.bg.tileGrid[tileY][tileX].center
        #end if
        
#         if key==pg.K_SPACE:
#             strimg = pg.image.tostring(self.img,'RGB',False)
#             img = Image.frombytes('RGB',self.img.get_size(),strimg)
#             img.save("gfx/screenshot.png")
            
        return
    #end onKeyPressed
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        #handle bounds
        #semis
        for i in range(self.semis.numCars):
            if self.semis.rects[i].right + 40 < 0:
                self.semis.rects[i].left = self.rect.w
                self.semis.spawn(i)
            #end if
        #end for
                
        #red cars
        for i in range(self.redCars.numCars):
            if self.redCars.rects[i].left - 45 >= self.rect.w:
                self.redCars.rects[i].left = -30
                self.redCars.spawn(i)
            #end if
        #end for
                
        #purple cars
        for i in range(self.purpleCars.numCars):
            if self.purpleCars.rects[i].right + 41 < 0:
                self.purpleCars.rects[i].left = self.rect.w - 1
                self.purpleCars.spawn(i)
            #end if
        #end for
                
        #trucks
        for i in range(self.trucks.numCars):
            if self.trucks.rects[i].left - 43 >= self.rect.w:
                self.trucks.rects[i].left = -36
                self.trucks.spawn(i)
            #end if
        #end for
                
        #river Row 1
        self.riverRow1.handleBounds(self.rect)
        self.riverRow2.handleBounds(self.rect)
        self.riverRow3.handleBounds(self.rect)
        self.riverRow4.handleBounds(self.rect)
                
        #check for collisions
        if self.trucks.collide(self.frog.collisionRect):
            self.blood.rect.center = self.frog.rect.center
            self.blood.visible = True
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.purpleCars.collide(self.frog.collisionRect):
            self.blood.rect.center = self.frog.rect.center
            self.blood.visible = True
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.redCars.collide(self.frog.collisionRect):
            self.blood.rect.center = self.frog.rect.center
            self.blood.visible = True
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.semis.collide(self.frog.collisionRect):
            self.blood.rect.center = self.frog.rect.center
            self.blood.visible = True
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.gayFrogs.collide(self.frog.collisionRect):
            self.frog.spawn()
            self.header.numScore += self.header.numSeconds
            self.header.numSeconds = 100
        #end if
            
        self.frog.mount = None
        
        if self.riverRow4.collide(self.frog.collisionRect):
            self.frog.mount = self.riverRow4
        #end if
            
        if self.riverRow3.collide(self.frog.collisionRect):
            self.frog.mount = self.riverRow3
        #end if
            
        if self.riverRow2.collide(self.frog.collisionRect):
            self.frog.mount = self.riverRow2
        #end if
            
        if self.riverRow1.collide(self.frog.collisionRect):
            self.frog.mount = self.riverRow1
        #end if
            
        if self.frog.mount == None:
            #snap frog center to tile grid
            tileX: int = int(self.frog.rect.x / self.bg.rect.w)
            tileY: int = int(self.frog.rect.y / self.bg.rect.w)
            self.frog.rect.center = self.bg.tileGrid[tileY][tileX].center
            
            for y in range(3,7):
                for x in range(20):
                    if self.bg.tileGrid[y][x].colliderect(self.frog):
                        self.frog.spawn()
                        self.header.numLives -= 1
                    #end if
                #end for
            #end for
        #end if
                        
        if self.frog.rect.left < 0:
            self.frog.rect.left = 0
        #end if
        
        if self.frog.rect.right >= self.rect.w:
            self.frog.rect.right = self.rect.w - 1
        #end if
        
        if self.frog.rect.top < 0:
            self.frog.rect.top = 0
        #end if
        
        if self.frog.rect.bottom >= self.rect.h:
            self.frog.rect.bottom = self.rect.h - 1
            
        #check for end game
        if all([x == 0 for x in self.gayFrogs.states]):
            self.gayFrogs.reset()
            self.header.numScore += 1000
            self.frog.spawn()
        #end if
        
        return
    #end update
#end Play

class Frogger(Game):
    def __init__(self) -> None:
        super().__init__("Frogger",[800,600])
        
        self.menuState: GameState = Menu()
        self.playState: GameState = Play()
        
        self.states: list[GameState] = [
            self.menuState
            ,self.playState
        ]
        self.stateNum: int = 0
        
        self.switchState(self.states[self.stateNum])
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        if self.state.exitCode == 1:
            self.switchState(self.playState)
        #end if
        
        return
    #end update
#end Frogger

def main() -> None:
    frogger: Frogger = Frogger()
    frogger.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if