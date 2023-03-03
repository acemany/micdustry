from pygame import time,font,init,event,key,mouse,display,quit
from pygame.constants import (KEYDOWN,QUIT,K_ESCAPE)
from sprites import Block,TILE_SIZE
from classes.entitys import Player
from maps import borlay
from json import load as jload
from typing import List

def txtToMap(func,txt:str):
    txt=txt.replace("\n","|")
    return [[func(char,(x,y))
    for x,char in enumerate(row.split(","))]
    for y,row  in enumerate(txt.split("|"))]

#INIT
init()
tile_current=1
plr=Player(0,0)
SC_RES=(800,600)
clock=time.Clock()
win=display.set_mode(SC_RES)
with open("settings.json")as file:
    jsonData=jload(file)
    FPS_LIMIT=jsonData["display"]["fps"]
GameFont=font.SysFont('Comis Sans',24,bold=True)
with open("maps/map_test.msav")as file:
    bottom_map=txtToMap(Block,file.read())

while(True):
    keys=key.get_pressed()
    if keys[K_ESCAPE]or event.get(QUIT):break
    plr.update(keys)

    win.fill((0,0,0))
    [[tile.draw(win,(plr.x,plr.y))
    for tile in tiles]for tiles in bottom_map]
    win.blit(GameFont.render(f"{int(clock.get_fps())}",0,"#C0FFEE"),(10,10))
    win.blit(GameFont.render(f"{int(plr.x          )}",0,"#C0FFEE"),(10,25))
    win.blit(GameFont.render(f"{int(plr.y          )}",0,"#C0FFEE"),(10,40))
    clock.tick(FPS_LIMIT)
    display.flip()
quit()
