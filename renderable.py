from base import *

class Renderable(Entity):
    def __init__(self, name:str = 'renderable') -> None:
        super().__init__(name)
        
        return
    #end __init__

    def render(self, buffer: pg.surface.Surface) -> None:

        return
    #end render

    def update(self, dt: float) -> None:
        
        return
    #end update
#end Renderable

class Geometry(Renderable):
    def __init__(
        self
        ,center: pg.math.Vector2|list[int] = pg.math.Vector2(0,0)
        ,numVerts: int = 3
        ,radius: int = 1
        ,lineThickness: int = 1
        ,color: list[int] = (255,255,255)
        ,name: str = 'geometry'
    ) -> None:
        super().__init__(name)
        self.center: pg.math.Vector2 = None

        if isinstance(center, pg.math.Vector2):
            self.center = center
        elif isinstance(center, list) or isinstance(center, tuple):
            if len(center) >= 2:
                self.center = pg.math.Vector2(center[:2])
            #end if
        else:
            self.center = pg.math.Vector2(0,0)
        #end if
        
        self.orientation: float = 0.0
        self.numVerts: int = numVerts

        if self.numVerts < 1:
            self.numVerts = 1
        #end if

        self.radius: int = radius

        if self.radius < 1:
            self.radius = 1
        #end if
        
        self.verts: list[pg.math.Vector2] = [
            pg.math.Vector2.from_polar(
                (self.radius, (360.0 / self.numVerts) * n)
            )
            for n in range(self.numVerts)
        ]

        self.lineThickness: int = lineThickness
        self.color: list[int] = list(color)
        
        return
    #end __init__

    def render(self, buffer: pg.surface.Surface) -> None:
        pg.draw.polygon(
            buffer
            ,self.color
            ,[
                v.rotate(self.orientation) + self.center
                for v in self.verts
            ]
            ,self.lineThickness
        )

        return
    #end render
#end Geometry

class RGBSurface(Renderable):
    def __init__(
        self
        ,img: pg.surface.Surface|str = None
        ,topleft: list[int] = [0,0]
        ,name: str = 'rgbsurface'
    ) -> None:
        super().__init__(name)
        self.img: pg.surface.Surface = None
        
        if isinstance(img,pg.surface.Surface):
            self.img = img
        elif isinstance(img,str):
            try:
                pg.image.load(img)
            except:
                self.img = pg.surface.Surface((1,1))
                self.img.fill((255,0,0))
            #end try
        else:
            self.img = pg.surface.Surface((1,1))
            self.img.fill((255,0,0))
        #end if
            
        self.rect: pg.Rect = self.img.get_rect()
        self.rect.topleft = topleft
        
        return
    #end __init__

    def render(self, buffer: pg.surface.Surface) -> None:
        buffer.blit(self.img,self.rect)

        return
    #end render
#end RGBSurface
    
class Text(Renderable):
    def __init__(self, text: str = '', size: int = 12, color: list[int] = (255,255,255), name: str = 'text') -> None:
        super().__init__(name)
        self.text: str = text
        self.size: int = size
        self.color: list[int] = color
        self.font: pg.font.Font = pg.font.Font(size=self.size)
        self.img: pg.surface.Surface = self.font.render(self.text,False,self.color)
        self.rect: pg.Rect = self.img.get_rect()
        
        return
    #end __init__
    
    def updateText(self, newText: str) -> None:
        center: list[int] = self.rect.center
        self.img = self.font.render(newText,False,self.color)
        self.rect = self.img.get_rect()
        self.rect.center = center
        
        return
    #end updateText
    
    def render(self, buffer: pg.surface.Surface) -> None:
        buffer.blit(self.img,self.rect)
        
        return
    #end render
#end Text

def main() -> None:
    game: Game = Game('Renderable',[800,600])
    game.run()

    return
#end main

if __name__ == '__main__':
    main()
#end if
