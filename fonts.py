from typing import Tuple
from pygame import Surface
from pygame.font import Font


class MainFont:
    def __init__(self,color:str="BBBBBB",scale:int=6,antialias:bool=1):
        self.Font=Font("gameFont.woff",scale)
        self.antialias=antialias
        self.scale=scale
        self.color=color
    def resize(self,scale2):
        self.font=self.Font.__init__("gameFont.woff",scale2)
    def draw(self,win:Surface,text:str,pos:Tuple[int,int]):
            win.blit(self.Font.render(text,self.antialias,self.color),pos)