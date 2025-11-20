import pygame as pg
from PIL import Image
from random import randint

def dist(p1: list[float], p2: list[float]) -> float:
    
    return sum([(p1[i] - p2[i])**2 for i in range(len(p1))]) ** 0.5
#end dist

def norm(v: list[float]) -> list[float]:
    t: float = sum(v)
    return [x / t for x in v]
#end norm

def colorToHex(color: list[int]) -> str:
    return hex(color[0])[2:] + hex(color[1])[2:] + hex(color[2])[2:]

def main() -> None:
    pg.init()
    displaySize: list[int] = [800,800]
    display: pg.surface.Surface = pg.display.set_mode(displaySize)
    renderSize: list[int] = [100,100]
    renderBuffer: pg.surface.Surface = pg.surface.Surface(renderSize)
    running: bool = True
    
    #set up help UI
    helpText: str = "i=Invert Colors; d=Make Center Dark; l=Make Center Light; n=New Random Gradient" 
    helpUI: pg.surface.Surface = pg.font.Font(None,25).render(helpText,False,(255,255,255))
    
    #set up random gradient
    numPoints: int = 5
    points: list[list[int]] = [
        [0,0]
        ,[renderSize[0]-1,0]
        ,[renderSize[0]-1,renderSize[1]-1]
        ,[0,renderSize[1]-1]
        ,[int(renderSize[0] / 2),int(renderSize[1] / 2)]
    ]
    colors: list[list[int]] = [[randint(0,255),randint(0,255),randint(0,255)] for x in range(numPoints)]
    inverseDist: list[float] = [0.0 for x in range(numPoints)]
    
    for y in range(renderSize[1]):
        for x in range(renderSize[0]):
            pixelColor: list[float] = [0,0,0]
            
            for i in range(numPoints):
                inverseDist[i] = 1.0 / (dist([x,y], points[i]) + 0.001)
            #end for
                
            inverseDist = norm(inverseDist)
            pixelColor[0] = sum([colors[i][0] * inverseDist[i] for i in range(numPoints)])
            pixelColor[1] = sum([colors[i][1] * inverseDist[i] for i in range(numPoints)])
            pixelColor[2] = sum([colors[i][2] * inverseDist[i] for i in range(numPoints)])
            renderBuffer.set_at([x,y], pixelColor)
        #end for
    #end for
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYUP:
                if event.key == pg.K_n:
                    #set up random gradient
                    colors = [[randint(0,255),randint(0,255),randint(0,255)] for x in range(numPoints)]
                    
                    for y in range(renderSize[1]):
                        for x in range(renderSize[0]):
                            pixelColor: list[float] = [0,0,0]
                            
                            for i in range(numPoints):
                                inverseDist[i] = 1.0 / (dist([x,y], points[i]) + 0.001)
                            #end for
                                
                            inverseDist = norm(inverseDist)
                            pixelColor[0] = sum([colors[i][0] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[1] = sum([colors[i][1] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[2] = sum([colors[i][2] * inverseDist[i] for i in range(numPoints)])
                            renderBuffer.set_at([x,y], pixelColor)
                        #end for
                    #end for
                elif event.key == pg.K_l:
                    #set up random gradient with white in the middle
                    colors[-1] = [255,255,255]
                    
                    for y in range(renderSize[1]):
                        for x in range(renderSize[0]):
                            pixelColor: list[float] = [0,0,0]
                            
                            for i in range(numPoints):
                                inverseDist[i] = 1.0 / (dist([x,y], points[i]) + 0.001)
                            #end for
                                
                            inverseDist = norm(inverseDist)
                            pixelColor[0] = sum([colors[i][0] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[1] = sum([colors[i][1] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[2] = sum([colors[i][2] * inverseDist[i] for i in range(numPoints)])
                            renderBuffer.set_at([x,y], pixelColor)
                        #end for
                    #end for
                elif event.key == pg.K_d:
                    #set up random gradient with black in the middle
                    colors[-1] = [0,0,0]
                    
                    for y in range(renderSize[1]):
                        for x in range(renderSize[0]):
                            pixelColor: list[float] = [0,0,0]
                            
                            for i in range(numPoints):
                                inverseDist[i] = 1.0 / (dist([x,y], points[i]) + 0.001)
                            #end for
                                
                            inverseDist = norm(inverseDist)
                            pixelColor[0] = sum([colors[i][0] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[1] = sum([colors[i][1] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[2] = sum([colors[i][2] * inverseDist[i] for i in range(numPoints)])
                            renderBuffer.set_at([x,y], pixelColor)
                        #end for
                    #end for
                elif event.key == pg.K_i:
                    #set up random gradient with colors inverted
                    colors = [[255 - c for c in color] for color in colors]
                    
                    for y in range(renderSize[1]):
                        for x in range(renderSize[0]):
                            pixelColor: list[float] = [0,0,0]
                            
                            for i in range(numPoints):
                                inverseDist[i] = 1.0 / (dist([x,y], points[i]) + 0.001)
                            #end for
                                
                            inverseDist = norm(inverseDist)
                            pixelColor[0] = sum([colors[i][0] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[1] = sum([colors[i][1] * inverseDist[i] for i in range(numPoints)])
                            pixelColor[2] = sum([colors[i][2] * inverseDist[i] for i in range(numPoints)])
                            renderBuffer.set_at([x,y], pixelColor)
                        #end for
                    #end for
                elif event.key == pg.K_SPACE:
                    strimg: str = pg.image.tostring(renderBuffer,'RGB',False)
                    img: Image.Image = Image.frombytes('RGB',renderSize,strimg)
                    img.save(
                        "%s%s%s%s%s.png" % (
                            colorToHex(colors[0])
                            ,colorToHex(colors[1])
                            ,colorToHex(colors[2])
                            ,colorToHex(colors[3])
                            ,colorToHex(colors[4])
                        )
                    )
                #end if
            #end if
        #end for
                
        #render the gradient to the display
        pg.transform.scale(renderBuffer, displaySize, display)
        
        display.blit(helpUI,(0,0))
        
        #present the display
        pg.display.flip()
    #end while
    
    pg.quit()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if