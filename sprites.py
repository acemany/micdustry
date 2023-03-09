from pygame import image,Surface
from pygame.transform import scale as resizei
from settings import sets
from typing import Tuple



TILE_SIZE=sets["display"]["tile_size"]
class Block:
    def __init__(self,block_id:str,pos:Tuple[int,int],
    path:str="bottom",):
        self.x=pos[0]*TILE_SIZE
        self.y=pos[1]*TILE_SIZE
        self.block_id=block_id
        self.path=path
        try:self.image=resizei(image.load(
            f"sprites/blocks/{self.path}/{self.block_id}.bmp"
            ).convert(),(TILE_SIZE,TILE_SIZE))
        except FileNotFoundError:self.image=resizei(image.load(
            "sprites/blocks/bottom/empty.bmp"
            ).convert(),(TILE_SIZE,TILE_SIZE))
    def draw(self,surface:Surface,offset:Tuple[int,int],distance:int):
        surface.blit(resizei(self.image,(distance,distance)),
            (((self.x-offset[0])*distance/TILE_SIZE),
             ((self.y-offset[1])*distance/TILE_SIZE)))
