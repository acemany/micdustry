from pygame import time,font,init,event,key,mouse,display,quit
from pygame.constants import (KEYDOWN,QUIT,
    K_ESCAPE,
    K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,
    K_l,K_k)
from sprites import Block,TILE_SIZE
from classes.entitys import Player
from maps import borlay
from json import load as jload
from typing import List

def mapToTxt(map:List[List[object]]):
    txt=""
    for tiles in map:
        for tile in tiles:
            txt+=f"{tile.block_id},"
        txt+="\n"
    txt+="j"
    return txt.replace(",\n","\n").replace("\nj","")
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
TILE_LIST=["env-error","sand","gr","empty"]
with open("maps/map_test.msav")as file:
    bottom_map=txtToMap(Block,file.read())

while(True):
    keys=key.get_pressed()
    if keys[K_ESCAPE]or event.get(QUIT):break
    elif keys[K_0]:tile_current=0
    elif keys[K_1]:tile_current=1
    elif keys[K_2]:tile_current=2
    elif keys[K_3]:tile_current=3
    elif keys[K_4]:tile_current=4
    elif keys[K_5]:tile_current=5
    elif keys[K_6]:tile_current=6
    elif keys[K_7]:tile_current=7
    elif keys[K_8]:tile_current=8
    elif keys[K_9]:tile_current=9
    if   keys[K_l]:
        with open("maps/map_test.msav","w")as file:
            file.write(mapToTxt(bottom_map))
    if keys[K_k]:
        with open("maps/map_test.msav")as file:
            bottom_map=txtToMap(Block,file.read())
    plr.update(keys)
    if mouse.get_pressed()[0]:
        tilex=int(mouse.get_pos()[0]+plr.x)//TILE_SIZE
        tiley=int(mouse.get_pos()[1]+plr.y)//TILE_SIZE
        if tilex>=0 and tiley>=0:
            try:bottom_map[tiley][tilex]=Block(
                TILE_LIST[tile_current],(tilex, tiley))
            except IndexError:pass

    win.fill((0,0,0))
    [[tile.draw(win,(plr.x,plr.y))
    for tile in tiles]for tiles in bottom_map]
    win.blit(GameFont.render(f"{int(clock.get_fps())}",0,"#C0FFEE"),(10,10))
    win.blit(GameFont.render(f"{int(plr.x          )}",0,"#C0FFEE"),(10,25))
    win.blit(GameFont.render(f"{int(plr.y          )}",0,"#C0FFEE"),(10,40))
    clock.tick(FPS_LIMIT)
    display.flip()
quit()
