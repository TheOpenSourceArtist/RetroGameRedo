from SimplerGE import *
from random import choices, choice
from PIL import Image

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
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        
        if isinstance(self.mount,Entity):
            self.rect.center += self.mount.velocity
        #end if
        
        return
    #end update
    
    def render(self, renderBuffer:pg.surface.Surface) -> None:
        renderBuffer.blit(self.states[self.state],self.rect)
        
        return
    #end render
    
    def spawn(self) -> None:
        self.rect.center = self.spawnPoint.center
        self.state = 0
        
        return
    #end spawn
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
    
    def collide(self, other: Entity) -> bool:
        for i in range(self.numStates - 1):
            if self.states[i] != 0 and self.rects[i].colliderect(other.rect):
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
    
    def collide(self, other: Entity) -> bool:
        for i in range(self.numCars):
            if self.onRoad[i] and self.rects[i].colliderect(other.rect):
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
#end Log
    
class Turtle(Entity):
    def __init__(self) -> None:
        super().__init__()
        
        return
    #end __init__
#end Turtle
    
class Gator(Entity):
    def __init__(self, offset: int = 0) -> None:
        super().__init__((0,0,60,20),pg.image.load('gfx/gator.bmp'))
        self.states: list[pg.surface.Surface] = [
            self.img.subsurface((0,0,60,20))
            ,self.img.subsurface((0,20,60,20))
            ,pg.transform.rotate(self.img.subsurface((0,0,60,20)),180)
            ,pg.transform.rotate(self.img.subsurface((0,20,60,20)),180)
        ]
        
        for state in self.states:
            state.set_colorkey(SGE_COLORKEY_DEFAULT)
        #end for
        
        self.stateDelay: int = 500
        self.stateDT: int = 0
        self.stateIndex: int = 0
        self.numStates: int = 2
        self.startState: int = offset
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        renderBuffer.blit(self.states[self.stateIndex],self.rect)
        
        return
    #end render
    
    def update(self, deltaTime: float) -> None:
        self.stateDT += deltaTime
        
        if self.stateDT >= self.stateDelay:
            self.stateIndex = ((self.stateIndex + 1) % self.numStates) + self.startState
            self.stateDT = 0
        #end if
        
        return
    #end update
#end Gator
    
class RiverLine(Entity):
    def __init__(self, rect:pg.Rect, speed: float = 1) -> None:
        super().__init__(rect,vel=(speed, 0))
        self.entities: list[Entity] = [
            Gator()
            ,Log(4)
            ,Log(3)
            ,Log(2)
        ]
        self.numEntities: int = len(self.entities)
        self.numThingsInWater: int = 6
        self.spacing: int = self.rect.w
        
        if speed >= 0:
            self.spacing *= -1
            self.entities[0].startState = 2
        #endif
        
        self.rects: list[pg.Rect] = [self.rect.move(self.spacing * i,0) for i in range(self.numThingsInWater)]
        self.thingsInWater: list[int] = [choice(list(range(self.numEntities))) for i in range(self.numThingsInWater)]
        self.thingsShown: list[bool] = [choice([True,False]) for i in range(self.numThingsInWater)]
        
        return
    #end __init__
    
    def collide(self, other: Entity) -> None:
        for i in range(self.numThingsInWater):
            self.entities[self.thingsInWater[i]].rect.center = self.rects[i].center
            if self.entities[self.thingsInWater[i]].rect.colliderect(other.rect):
                if self.thingsShown[i]:
                    return True
                #end if
            #end if
        #end for
        
        return False
    #end mount
    
    def spawn(self, i: int) -> None:
        self.thingsShown[i] = choice([True,False])
        self.thingsInWater[i] = choice(list(range(self.numEntities)))
        
        if self.velocity.x >= 0:
            self.rects[i].right = 0
        else:
            self.rects[i].left = 399
        #end if
        
        return
    #end spawn
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for i in range(self.numThingsInWater):            
            if self.thingsShown[i]:
                self.entities[self.thingsInWater[i]].rect.center = self.rects[i].center
                self.entities[self.thingsInWater[i]].render(renderBuffer)
            #end if
        #end for
        
        return
    #end render
    
    def update(self, deltaTime:float) -> None:
        for i in range(self.numThingsInWater):
            self.rects[i].center += self.velocity
        #end for
            
        for entity in self.entities:
            entity.update(deltaTime)
        #end for
        
        return
    #end update
#end RiverLine
    
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
        
        self.entities.append(self.bg)
        self.entities.append(self.riverRow1)
        self.entities.append(self.riverRow2)
        self.entities.append(self.riverRow3)
        self.entities.append(self.riverRow4)
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
        
        #snap frog center to tile grid
        tileX: int = int(self.frog.rect.x / self.bg.rect.w)
        tileY: int = int(self.frog.rect.y / self.bg.rect.w)
        self.frog.rect.center = self.bg.tileGrid[tileY][tileX].center
        
        if key==pg.K_SPACE:
            strimg = pg.image.tostring(self.img,'RGB',False)
            img = Image.frombytes('RGB',self.img.get_size(),strimg)
            img.save("gfx/screenshot.png")
            
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
        
        #river row 1
        for i in range(self.riverRow1.numThingsInWater):
            if self.riverRow1.rects[i].left >= self.rect.w:
                self.riverRow1.spawn(i)
            #end if
        #end for
                
        #river row 2
        for i in range(self.riverRow2.numThingsInWater):
            if self.riverRow2.rects[i].right < 0:
                self.riverRow2.spawn(i)
            #end if
        #end for
                
        #river row 3
        for i in range(self.riverRow3.numThingsInWater):
            if self.riverRow3.rects[i].left >= self.rect.w:
                self.riverRow3.spawn(i)
            #end if
        #end for
                
        #river row 4
        for i in range(self.riverRow4.numThingsInWater):
            if self.riverRow4.rects[i].right < 0:
                self.riverRow4.spawn(i)
            #end if
        #end for
                
        #check for collisions
        if self.trucks.collide(self.frog):
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.purpleCars.collide(self.frog):
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.redCars.collide(self.frog):
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.semis.collide(self.frog):
            self.frog.spawn()
            self.header.numLives -= 1
        #end if
            
        if self.gayFrogs.collide(self.frog):
            self.frog.spawn()
            self.header.numScore += self.header.numSeconds
            self.header.numSeconds = 100
        #end if
            
        self.frog.mount = None
        
        if self.riverRow4.collide(self.frog):
            self.frog.mount = self.riverRow4
        #end if
            
        if self.riverRow3.collide(self.frog):
            self.frog.mount = self.riverRow3
        #end if
            
        if self.riverRow2.collide(self.frog):
            self.frog.mount = self.riverRow2
        #end if
            
        if self.riverRow1.collide(self.frog):
            self.frog.mount = self.riverRow1
        #end if
            
        if self.frog.mount == None:
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
#end Frogger

def main() -> None:
    frogger: Frogger = Frogger()
    frogger.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if