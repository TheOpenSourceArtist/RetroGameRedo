from SimplerGE import *
from sys import argv
import traceback

DISPLAY_SIZE: list[int] = [1000,600]
RENDER_SIZE: list[int] = [1000,600]
PANEL_SIZE: list[int] = [int(RENDER_SIZE[0] * 0.35),int(RENDER_SIZE[1])]
WORKAREA_SIZE: list[int] = [RENDER_SIZE[0] - PANEL_SIZE[0], RENDER_SIZE[1]]
TILESETPREVIEW_SIZE: list[int] = [int(PANEL_SIZE[0] * 0.8),int(PANEL_SIZE[0] * 0.8)]

FONT_SIZE: int = int(RENDER_SIZE[1] * 0.07)

TILEWIDTH: int = 8
TILEHEIGHT: int = 8
TILEMAPWIDTH: int = 20
TILEMAPHEIGHT: int = 20

BLACK: list[int] = [0,0,0]
DARK: list[int] = [77,77,77]
LIGHT: list[int] = [125,125,125]
WHITE:list[int] = [255,255,255]
TRANSPARENT: list[int] = [255,0,255]
    
class Label(Entity):
    font: pg.font.Font = pg.font.Font(size = FONT_SIZE)
    
    def __init__(self, text: str = '') -> None:
        self.text: str = text
        textImg: pg.surface.Surface = Label.font.render(self.text, False, BLACK)
        textRect: pg.Rect = textImg.get_rect()
        img: pg.surface.Surface = pg.surface.Surface(textRect.size)
        img.fill(TRANSPARENT)
        img.set_colorkey(TRANSPARENT)
        img.blit(textImg,textRect)
        super().__init__(textRect,img)
        
        return
    #end __int__
#end Label
    
class Incrementor(Entity):
    def __init__(self, text: str = '', value: int = 0) -> None:
        self.entities: list[Entity] = []
        self.lblDecrement: Label = Label('<')
        self.text: str = text
        self.value: int = value
        self.lblText: Label = Label('%s %d' % (self.text,self.value))
        self.lblIncrement: Label = Label('>')
        super().__init__((0,0,self.lblText.rect.w,self.lblText.rect.h))
        
        self.lblText.rect.center = self.rect.center
        self.lblDecrement.rect.midright = self.lblText.rect.midleft
        self.lblIncrement.rect.midleft = self.lblText.rect.midright
        
        return
    #end __init__
    
    def increment(self) -> None:
        self.value += 1
        self.lblText: Label = Label('%s %d' % (self.text,self.value))
        
        return
    #end increment
    
    def decrement(self) -> None:
        self.value -= 1
        self.lblText: Label = Label('%s %d' % (self.text,self.value))
        
        return
    #end increment
    
    def update(self, deltaTime: float) -> None:
        self.lblText.rect.center = self.rect.center
        self.lblDecrement.rect.midright = self.lblText.rect.midleft
        self.lblIncrement.rect.midleft = self.lblText.rect.midright
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        self.lblDecrement.render(renderBuffer)
        pg.draw.rect(renderBuffer,BLACK,self.lblDecrement.rect,1)
        self.lblText.render(renderBuffer)
        self.lblIncrement.render(renderBuffer)
        pg.draw.rect(renderBuffer,BLACK,self.lblIncrement.rect,1)
        
        return
    #end render
#end Incrementor
    
class Button(Label):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        super().render(renderBuffer)
        pg.draw.rect(renderBuffer,BLACK,self.rect,2)
        
        return
    #end render
#end Button
    
class TileSetPreview(Entity):
    def __init__(self, imgPath: str) -> None:
        tileSetImg: pg.surface.Surface = pg.image.load(imgPath)
        img: pg.surface.Surface = pg.surface.Surface(TILESETPREVIEW_SIZE)
        tileSetImg = pg.transform.scale(tileSetImg,TILESETPREVIEW_SIZE)
        img.blit(tileSetImg,(0,0))
        super().__init__(((0,0),TILESETPREVIEW_SIZE),img)
        
        return
    #end __init__
#end TileSetPreview
    
class TileSelector(Entity):
    def __init__(self, imgPath: str) -> None:
        super().__init__((0,0,PANEL_SIZE[0],PANEL_SIZE[1]))
        self.entities: list[Entity] = []
        self.bg: Entity = Entity(self.rect.move(0,0))
        self.bg.img.fill(DARK)
        self.lblTileSetPreview: Label = Label('Tile Set Preview')
        self.lblTileSetPreview.rect.midtop = self.rect.midtop
        self.tileSetPreview: TileSetPreview = TileSetPreview(argv[-1])
        self.tileSetPreview.rect.midtop = self.lblTileSetPreview.rect.midbottom
        self.tileWidth: int = TILEWIDTH
        self.incTileWidth: Incrementor = Incrementor('Tile Width: ', self.tileWidth)
        self.incTileWidth.rect.midtop = self.tileSetPreview.rect.midbottom
        
        self.tileHeight: int = TILEHEIGHT
        self.incTileHeight: Incrementor = Incrementor('Tile Height: ', self.tileHeight)
        self.incTileHeight.rect.midtop = self.incTileWidth.rect.midbottom
        
        self.tileSetImg: pg.surface.Surface = pg.image.load(argv[-1])
        self.tiles: list[pg.surface.Surface] = []
        self.numTiles: int = len(self.tiles)
        self.tileRects: list[pg.Rect] = []
        
#         self.getTiles(self.tileSetImg,self.tileWidth,self.tileHeight)
        self.getTiles()
        self.selectedTile: int = 0
        
        self.entities.append(self.bg)
        self.entities.append(self.lblTileSetPreview)
        self.entities.append(self.tileSetPreview)
        self.entities.append(self.incTileWidth)
        self.entities.append(self.incTileHeight)
        
        return
    #end __init__
    
    def update(self, deltaTime: float) -> None:
        for entity in self.entities:
            entity.update(deltaTime)
        #end for
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for entity in self.entities:
            entity.render(renderBuffer)
        #end for
            
        for rect in self.tileRects:
            pg.draw.rect(renderBuffer,BLACK,rect,1)
        #end for
        
        if self.selectedTile > -1 and self.selectedTile < self.numTiles:
            pg.draw.rect(renderBuffer, WHITE, self.tileRects[self.selectedTile],2)
        
        return
    #end render
    
    def getTiles(self) -> None:
        self.tileRects = []
        self.tiles = []
        self.selectedTile = 0
        
        img: pg.surface.Surface = self.tileSetImg
        width: int = self.tileWidth
        height: int = self.tileHeight
        scaledW: int = (width / img.get_size()[0]) * self.tileSetPreview.rect.w
        scaledH: int = (height / img.get_size()[1]) * self.tileSetPreview.rect.h
        y: int = 0
        x: int = 0
        
        for r in range(0,img.get_size()[1],height):
            x = 0
            
            for c in range(0,img.get_size()[0],width):
                if c + width <= img.get_size()[0] and r + height <= img.get_size()[1]:
                    self.tiles.append(img.subsurface((c,r,width,height)))
                    self.tileRects.append(pg.Rect(
                        round((x * scaledW) + self.tileSetPreview.rect.x)
                        ,round((y * scaledH) + self.tileSetPreview.rect.y)
                        ,round(scaledW)
                        ,round(scaledH)
                    ))
                #end if
                
                x += 1
            #end for
            
            y += 1
        #end for
        
        self.numTiles = len(self.tiles)
        
        return
    #end getTiles
    
    def getSelectedTile(self, pos: list[int]) -> None:
        for i in range(self.numTiles):
            if self.tileRects[i].collidepoint(pos):
                self.selectedTile = i
                
                return
            #end if
        #end for
        
        return
    #end getSelectedTile
#end TileSelector
    
class TileMapInfo(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,PANEL_SIZE[0],PANEL_SIZE[1]))
        self.entities: list[Entity] = []
        self.incTileMapWidth: Incrementor = Incrementor('Tile Map Width: ',TILEMAPWIDTH)
        self.incTileMapHeight: Incrementor = Incrementor('Tile Map Height: ', TILEMAPHEIGHT)
        self.btnExport: Button = Button('Export Tile Map')
        
        self.entities.append(self.incTileMapWidth)
        self.entities.append(self.incTileMapHeight)
        self.entities.append(self.btnExport)
        
        self.pack()
        
        return
    #end __init__
    
    def pack(self) -> None:
        l: int = len(self.entities)
        
        if l > 0:
            self.entities[0].rect.midtop = self.rect.midtop
            
            for i in range(1, l):
                self.entities[i].rect.midtop = self.entities[i-1].rect.midbottom
            #end for
        #end if
        
        return
    #end pack
    
    def update(self, deltaTime: float) -> None:
        self.pack()
        
        for entity in self.entities:
            entity.update(deltaTime)
        #end for
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for entity in self.entities:
            entity.render(renderBuffer)
        #end for
        
        return
    #end render
#end TileMapInfo

class Panel(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,PANEL_SIZE[0],PANEL_SIZE[1]))
        self.entities: list[Entity] = []
        self.tileSelector: TileSelector = TileSelector(argv[-1])
        self.tileMapInfo: TileMapInfo = TileMapInfo()
        self.tileMapInfo.rect.midtop = self.tileSelector.incTileHeight.rect.midbottom
        
        self.entities.append(self.tileSelector)
        self.entities.append(self.tileMapInfo)
        
        return
    #end __int__
    
    def update(self, deltaTime: float) -> None:
        for entity in self.entities:
            entity.update(deltaTime)
        #end for
        
        return
    #end update
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for entity in self.entities:
            entity.render(renderBuffer)
        #end
        
        return
    #end render
#end Panel
    
class TileMap(Entity):
    def __init__(self, tileWidth: int, tileHeight: int, tileMapWidth: int, tileMapHeight: int) -> None:
        self.tileWidth: int = tileWidth
        self.tileHeight: int = tileHeight
        self.tileMapWidth: int = tileMapWidth
        self.tileMapHeight: int = tileMapHeight
        self.map: list[int] = [[-1 for x in range(self.tileMapWidth)] for y in range(self.tileMapHeight)]
        self.numTiles: int = 0
        self.scale: float = 3.0
        
        super().__init__((0,0,tileWidth * tileMapWidth * self.scale,tileHeight * tileMapHeight * self.scale), pg.image.load(argv[-1]))
#         self.img.fill(BLACK)
        self.tileRects: list[pg.Rect] = []
        self.tiles: list[pg.surface.Surface] = []
        self.selectedTile: int = 0
        self.getTiles()
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:            
        for y in range(self.tileMapHeight):
            for x in range(self.tileMapWidth):
                pg.draw.rect(renderBuffer,WHITE,self.tileRects[y][x],1)
                
                if self.map[y][x] > -1:
                    renderBuffer.blit(pg.transform.scale(self.tiles[self.map[y][x]],self.tileRects[y][x].size),self.tileRects[y][x])
                #end if
            #end for
        #end for
                
        return
    #end render
    
    def getTiles(self) -> None:
        self.tileRects = []
        self.tiles = []
        self.selectedTile = 0
        
#         img: pg.surface.Surface = self.tileSetImg
        width: int = self.tileWidth
        height: int = self.tileHeight
        scaledW: int = (width) * self.scale
        scaledH: int = (height) * self.scale
        y: int = 0
        x: int = 0
        
        for r in range(0,self.img.get_size()[1],height):
            x = 0
            
            for c in range(0,self.img.get_size()[0],width):
                if c + width <= self.img.get_size()[0] and r + height <= self.img.get_size()[1]:
                    self.tiles.append(self.img.subsurface((c,r,width,height)))
#                     self.tileRects.append(pg.Rect(
#                         round((x * scaledW) + self.rect.x)
#                         ,round((y * scaledH) + self.rect.y)
#                         ,round(scaledW)
#                         ,round(scaledH)
#                     ))
                #end if
                
                x += 1
            #end for
            
            y += 1
        #end for
        
        self.numTiles = len(self.tiles)
        
        for y in range(self.tileMapHeight):
            row: list[pg.Rect] = []
            
            for x in range(self.tileMapWidth):
                row.append(pg.Rect(
                    (x * self.scale * TILEWIDTH) + self.rect.x
                    ,(y * self.scale * TILEHEIGHT) + self.rect.y
                    ,(self.scale * TILEWIDTH)
                    ,(self.scale * TILEHEIGHT)
                ))
            #end for
                
            if y >= len(self.map):
                self.map.append([-1 for x in range(self.tileMapWidth)])
                self.rect.h += self.scale * TILEHEIGHT
                
            if len(row) > len(self.map[y]):
                self.map[y].append(-1)
                self.rect.w += self.scale * TILEWIDTH
            elif len(row) < len(self.map[y]):
                self.map[y].pop(-1)
                self.rect.w -= self.scale * TILEWIDTH
            #end if
            
            self.tileRects.append(row)
        #end for
            
        if len(self.tileRects) < len(self.map):
            self.map.pop(-1)
            self.rect.h -= self.scale * TILEHEIGHT
        #end if
            
        for y in range(self.tileMapHeight):
            for x in range(self.tileMapWidth):
                if self.map[y][x] >= self.numTiles:
                    self.map[y][x] = -1
                #end if
            #end for
        #end for
        
        return
    #end getTiles
    
    def setTile(self, pos: list[int]) -> None:
        for y in range(self.tileMapHeight):
            for x in range(self.tileMapWidth):
                if self.tileRects[y][x].collidepoint(pos):
                    self.map[y][x] = self.selectedTile
                    
                    return
                #end if
            #end for
        #end for
        
        return
    #end setTile
    
    def clearTile(self, pos: list[int]) -> None:
        for y in range(self.tileMapHeight):
            for x in range(self.tileMapWidth):
                if self.tileRects[y][x].collidepoint(pos):
                    self.map[y][x] = -1
                    
                    return
                #end if
            #end for
        #end for
        
        return
    #end setTile
    
    def export(self) -> None:
        output = """
imgPath: str = '%s'
imgSize: list[int] = %s
tileWidth: int = %d
tileHeight: int = %d
tileMapWidth: int = %d
tileMapHeight: int = %d
numTiles: int = %d
map: list[list[int]] = %s
""" % (argv[-1],repr(self.img.get_size()),self.tileWidth,self.tileHeight,self.tileMapWidth,self.tileMapHeight,self.numTiles,repr(self.map).replace('], [',']\n, ['))
        print(output)
        
        return
    #end export
#end TileMap
    
class WorkArea(Entity):
    def __init__(self) -> None:
        super().__init__((PANEL_SIZE[0],0,WORKAREA_SIZE[0],WORKAREA_SIZE[1]))
        self.entities: list[Entity] = []
        self.bg: Entity = Entity((self.rect.x,self.rect.y,WORKAREA_SIZE[0],WORKAREA_SIZE[1]))
        self.bg.img.fill(LIGHT)
        self.tileMap: TileMap = TileMap(TILEWIDTH,TILEHEIGHT,TILEMAPWIDTH,TILEMAPHEIGHT)
        self.tileMap.rect.topleft = self.rect.move(10,10).topleft
        self.tileMap.getTiles()
        
        self.entities.append(self.bg)
        self.entities.append(self.tileMap)
        
        return
    #end __int__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for entity in self.entities:
            entity.render(renderBuffer)
        #end for
        
        return
    #end render
#end WorkArea

class MainState(GameState):
    def __init__(self) -> None:
        super().__init__(RENDER_SIZE)
        self.panel: Panel = Panel()
        self.workArea: WorkArea = WorkArea()
        
        self.entities.append(self.workArea)
        self.entities.append(self.panel)
        
        self.mousePos: list[int] = [0,0]
        
        return
    #end __init__
    
    def onMousePosUpdate(self, pos: list[int]) -> None:
        self.mousePos = pos
        
        if pg.mouse.get_pressed()[0]:
            self.workArea.tileMap.setTile(pos)
        elif pg.mouse.get_pressed()[2]:
            self.workArea.tileMap.clearTile(pos)
        #end if
        
        return
    #end onMousePosUpdate
    
    def onMouseButtonPressed(self, button: int) -> None:
        if self.panel.tileSelector.incTileWidth.lblDecrement.rect.collidepoint(self.mousePos):
            self.panel.tileSelector.incTileWidth.decrement()
            self.panel.tileSelector.tileWidth = self.panel.tileSelector.incTileWidth.value
            
            if  self.panel.tileSelector.tileWidth > 0:
                self.panel.tileSelector.getTiles()
                self.workArea.tileMap.tileWidth = self.panel.tileSelector.tileWidth
                self.workArea.tileMap.getTiles()
            #end if
        elif self.panel.tileSelector.incTileWidth.lblIncrement.rect.collidepoint(self.mousePos):
            self.panel.tileSelector.incTileWidth.increment()
            self.panel.tileSelector.tileWidth = self.panel.tileSelector.incTileWidth.value
            
            if  self.panel.tileSelector.tileWidth > 0:
                self.panel.tileSelector.getTiles()
                self.workArea.tileMap.tileWidth = self.panel.tileSelector.tileWidth
                self.workArea.tileMap.getTiles()
            #end if
        elif self.panel.tileSelector.incTileHeight.lblIncrement.rect.collidepoint(self.mousePos):
            self.panel.tileSelector.incTileHeight.increment()
            self.panel.tileSelector.tileHeight = self.panel.tileSelector.incTileHeight.value
            
            if  self.panel.tileSelector.tileHeight > 0:
                self.panel.tileSelector.getTiles()
                self.workArea.tileMap.tileHeight = self.panel.tileSelector.tileHeight
                self.workArea.tileMap.getTiles()
            #end if
        elif self.panel.tileSelector.incTileHeight.lblDecrement.rect.collidepoint(self.mousePos):
            self.panel.tileSelector.incTileHeight.decrement()
            self.panel.tileSelector.tileHeight = self.panel.tileSelector.incTileHeight.value

            if  self.panel.tileSelector.tileHeight > 0:
                self.panel.tileSelector.getTiles()
                self.workArea.tileMap.tileHeight = self.panel.tileSelector.tileHeight
                self.workArea.tileMap.getTiles()
            #end if
        elif self.panel.tileSelector.tileSetPreview.rect.collidepoint(self.mousePos):
            self.panel.tileSelector.getSelectedTile(self.mousePos)
            self.workArea.tileMap.selectedTile = self.panel.tileSelector.selectedTile
        elif self.panel.tileMapInfo.incTileMapWidth.lblDecrement.rect.collidepoint(self.mousePos):
            self.panel.tileMapInfo.incTileMapWidth.decrement()
            self.workArea.tileMap.tileMapWidth = self.panel.tileMapInfo.incTileMapWidth.value
            self.workArea.tileMap.getTiles()
        elif self.panel.tileMapInfo.incTileMapWidth.lblIncrement.rect.collidepoint(self.mousePos):
            self.panel.tileMapInfo.incTileMapWidth.increment()
            self.workArea.tileMap.tileMapWidth = self.panel.tileMapInfo.incTileMapWidth.value
            self.workArea.tileMap.getTiles()
        elif self.panel.tileMapInfo.incTileMapHeight.lblDecrement.rect.collidepoint(self.mousePos):
            self.panel.tileMapInfo.incTileMapHeight.decrement()
            self.workArea.tileMap.tileMapHeight = self.panel.tileMapInfo.incTileMapHeight.value
            self.workArea.tileMap.getTiles()
        elif self.panel.tileMapInfo.incTileMapHeight.lblIncrement.rect.collidepoint(self.mousePos):
            self.panel.tileMapInfo.incTileMapHeight.increment()
            self.workArea.tileMap.tileMapHeight = self.panel.tileMapInfo.incTileMapHeight.value
            self.workArea.tileMap.getTiles()
        elif self.panel.tileMapInfo.btnExport.rect.collidepoint(self.mousePos):
            print('Export Tile Map Information')
            self.workArea.tileMap.export()
        elif self.workArea.tileMap.rect.collidepoint(self.mousePos):
            self.workArea.tileMap.setTile(self.mousePos)
        #end if
        
        return
    #end onMouseButtonPressed
#end MainState

class Editor(Game):
    def __init__(self) -> None:
        super().__init__('Tile Map Editor', DISPLAY_SIZE)
        self.switchState(MainState())
        
        return
    #end __init__
#end Editor

def main() -> None:
    editor: Editor = Editor()
    
    try:
        editor.run()
    except Exception as e:
        editor.active = False
        print("An Exception Occured:")
        traceback.print_exc()
    
    return
#end main

if __name__ == '__main__':
    argv.append('79da84281ebe07772ddf8000.png')
    main()
#end if
