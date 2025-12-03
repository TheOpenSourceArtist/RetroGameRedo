from SimplerGE import *
from sys import argv

#global vars
DISP_SIZE: list[int] = [900,600]
PANEL_SIZE: list[int] = [int(DISP_SIZE[0] * 0.25),int(DISP_SIZE[1])]
CANVAS_SIZE: list[int] = [int(DISP_SIZE[0] * 0.75),int(DISP_SIZE[1])]
FONT_SIZE: int = 25

#colors
BLACK: list[int] = [0,0,0]
DARK: list[int] = [77,77,77]
MID: list[int] = [123,123,123]
LIGHT: list[int] = [200,200,200]
WHITE: list[int] = [255,255,255]
TRANSPARENT: list[int] = [255,0,255]

class Canvas(Entity):
    def __init__(self) -> None:
        super().__init__((PANEL_SIZE[0],0,CANVAS_SIZE[0],CANVAS_SIZE[1]))
        self.img.fill(LIGHT)
        pg.draw.rect(self.img,BLACK,self.rect.move(-PANEL_SIZE[0],0),1)
        
        return
    #end __init__
#end Panel
    
class TileSelector(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,PANEL_SIZE[0],PANEL_SIZE[1]))
        self.entities: list[Entity] = list()
        self.font: pg.font.Font = pg.font.Font(size = FONT_SIZE)
        textSurf: pg.surface.Surface = self.font.render('Tile Set:',False,WHITE)
        textBG: pg.surface.Surface = pg.surface.Surface(textSurf.get_size())
        textBG.fill(TRANSPARENT)
        textBG.blit(textSurf,(0,0))
        self.lblTileSet: Entity = Entity(textBG.get_rect(),textBG)
        self.lblTileSet.rect.midtop = self.rect.midtop
        
        self.tileSetPreview: Entity = Entity((0,0,int(PANEL_SIZE[0] * 0.75),int(PANEL_SIZE[0] * 0.75)))
        self.tileSetPreview.rect.midtop = self.lblTileSet.rect.midbottom
        self.masterTileSetImg: pg.surface.Surface = pg.image.load(argv[-1])
        self.masterTileSetSize: list[int] = self.masterTileSetImg.get_size()
        self.tileSetPreview.img.blit(pg.transform.scale(self.masterTileSetImg,self.tileSetPreview.rect.size),(0,0))
        
        self.tileWidth: int = 20
        textSurf = self.font.render('Tile Width: %d' % self.tileWidth,False,WHITE)
        textBG = pg.surface.Surface(textSurf.get_size())
        textBG.fill(TRANSPARENT)
        textBG.blit(textSurf,(0,0))
        self.lblTileWidth: Entity = Entity(textBG.get_rect(),textBG)
        self.lblTileWidth.rect.midtop = self.tileSetPreview.rect.midbottom
        
        self.tileHeight: int = 20
        textSurf = self.font.render('Tile Height: %d' % self.tileHeight,False,WHITE)
        textBG = pg.surface.Surface(textSurf.get_size())
        textBG.fill(TRANSPARENT)
        textBG.blit(textSurf,(0,0))
        self.lblTileHeight: Entity = Entity(textBG.get_rect(),textBG)
        self.lblTileHeight.rect.midtop = self.lblTileWidth.rect.midbottom
        
        self.numTileCols: int = int(self.masterTileSetSize[0] / self.tileWidth)
        self.numTileRows: int = int(self.masterTileSetSize[1] / self.tileHeight)
        self.selected: pg.Rect = pg.Rect(
            0
            ,0
            ,int(self.tileSetPreview.rect.w / self.numTileCols)
            ,int(self.tileSetPreview.rect.h / self.numTileRows)
        )
        self.selectedOutline: Entity = Entity(self.selected)
        self.selectedOutline.img.fill(TRANSPARENT)
        pg.draw.rect(self.selectedOutline.img,BLACK,self.selectedOutline.rect,1)
        self.selectedOutline.rect.topleft = self.tileSetPreview.rect.topleft
        
        textSurf = self.font.render('Tile Rows: %d' % self.numTileRows,False,WHITE)
        textBG = pg.surface.Surface(textSurf.get_size())
        textBG.fill(TRANSPARENT)
        textBG.blit(textSurf,(0,0))
        self.lblTileRows: Entity = Entity(textBG.get_rect(),textBG)
        self.lblTileRows.rect.midtop = self.lblTileHeight.rect.midbottom
        
        textSurf = self.font.render('Tile Cols: %d' % self.numTileCols,False,WHITE)
        textBG = pg.surface.Surface(textSurf.get_size())
        textBG.fill(TRANSPARENT)
        textBG.blit(textSurf,(0,0))
        self.lblTileCols: Entity = Entity(textBG.get_rect(),textBG)
        self.lblTileCols.rect.midtop = self.lblTileRows.rect.midbottom
        
        self.entities.append(self.lblTileSet)
        self.entities.append(self.tileSetPreview)
        self.entities.append(self.lblTileWidth)
        self.entities.append(self.lblTileHeight)
        self.entities.append(self.lblTileRows)
        self.entities.append(self.lblTileCols)
        self.entities.append(self.selectedOutline)
        
        return
    #end __init__
    
    def render(self, renderBuffer: pg.surface.Surface) -> None:
        for entity in self.entities:
            entity.render(renderBuffer)
        #end for
        
        return
    #end render
#end TileSelector

class Panel(Entity):
    def __init__(self) -> None:
        super().__init__((0,0,PANEL_SIZE[0],PANEL_SIZE[1]))
        self.img.fill(DARK)
        pg.draw.rect(self.img,BLACK,self.rect,1)
        
        return
    #end __init__
#end Panel

class Editor(GameState):
    def __init__(self) -> None:
        super().__init__(DISP_SIZE)
        self.mousePos: list[int] = [0,0]
        self.panel: Panel = Panel()
        self.tileSelector: TileSelector = TileSelector()
        self.canvas: Canvas = Canvas()
        
        self.entities.append(self.panel)
        self.entities.append(self.tileSelector)
        self.entities.append(self.canvas)
        
        return
    #end __init__
    
    def onMousePosUpdate(self, pos: list[int]) -> None:
        self.mousePos = pos
        
        return
    #end onMousePosUpdate
    
    def onMouseButtonReleased(self, button: int) -> None:
        if self.tileSelector.tileSetPreview.rect.collidepoint(self.mousePos):
            x: int = self.mousePos[0] - self.tileSelector.tileSetPreview.rect.x
            y: int = self.mousePos[1] - self.tileSelector.tileSetPreview.rect.y
            xPerc: float = x / self.tileSelector.tileSetPreview.rect.w
            yPerc: float = y / self.tileSelector.tileSetPreview.rect.h
            xTile: int = int(self.tileSelector.numTileCols * xPerc)
            yTile: int = int(self.tileSelector.numTileRows * yPerc)
            tileW: int = self.tileSelector.selectedOutline.rect.w
            tileH: int = self.tileSelector.selectedOutline.rect.h
            
            self.tileSelector.selectedOutline.rect.topleft = [
                xTile * tileW + self.tileSelector.tileSetPreview.rect.x
                , yTile * tileH + self.tileSelector.tileSetPreview.rect.y
            ]
        
        return
    #end onMouseButtonReleased
#end Editor

def main() -> None:
    TileMapEditor: Game = Game("Tile Map Editor", DISP_SIZE)
    TileMapEditor.state = Editor()
    TileMapEditor.run()
    
    return
#end main

if __name__ == '__main__':
#     argv.append('5723b94c74e7e493af7298474951.png')
    main()
#end if