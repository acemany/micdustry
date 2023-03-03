from pygame.transform import scale as resize
from pygame import init,display as disp,image,Surface,quit
from typing import Tuple

init()
win=disp.set_mode((50,50))

TILE_SIZE=16
errorimg=resize(image.load(
    "sprites/blocks/bottom/empty.bmp"
    ).convert(),(TILE_SIZE,TILE_SIZE)).convert()
class Block:
    def __init__(self,block_id:str,pos:Tuple[int,int],
    path:str="bottom",ore_id:str=None):
        self.x=pos[0]*TILE_SIZE
        self.y=pos[1]*TILE_SIZE
        self.block_id=block_id
        self.ore_id=ore_id
        self.path=path
        try:self.image=resize(image.load(
            f"sprites/blocks/{self.path}/{self.block_id}.bmp"
            ).convert(),(TILE_SIZE,TILE_SIZE)).convert()
        except FileNotFoundError:self.image=errorimg
        if ore_id!=None:self.image.blit(resize(image.load(
            f"sprites/blocks/environment/ore-{ore_id}.png"
            ).convert(),(0,0)),(TILE_SIZE,TILE_SIZE))
    def draw(self,surface:Surface,offset:Tuple[int,int]):
        surface.blit(self.image,((self.x-offset[0]),
                                 (self.y-offset[1])))

quit()
