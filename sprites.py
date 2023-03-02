from pygame.transform import scale as resize
from pygame import image,Surface
from typing import Tuple

TILE_SIZE=16

class Block:
    def __init__(self,block_id:str,pos:Tuple[int,int],
    path:str="environment",ore_id:str=None):
        self.x=pos[0]*TILE_SIZE
        self.y=pos[1]*TILE_SIZE
        self.block_id=block_id
        self.ore_id=ore_id
        self.path=path
        self.image=resize(image.load(
            f"sprites/blocks/{self.path}/{self.block_id}.png"
            ).convert(),(TILE_SIZE,TILE_SIZE)).convert()
        if ore_id!=None:self.image.blit(resize(image.load(
            f"sprites/blocks/environment/ore-{ore_id}.png"
            ).convert(),(0,0)),(TILE_SIZE,TILE_SIZE))
    def draw(self,surface:Surface,offset:Tuple[int,int]):
        surface.blit(self.image,((self.x-offset[0]),
                                 (self.y-offset[1])))
