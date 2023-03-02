from pygame import time,font,init,event,key,display as dsp,quit
from pygame.constants import K_ESCAPE,QUIT
from random import randint as rdmnt
from classes.entitys import Player
from json import load as jload
from maps.borlay import TXTMAP
from sprites import Block

#INIT
init()
clock=time.Clock()
GameFont=font.SysFont('Comis Sans',24,bold=True)
with open("settings.json") as file:
    jsonData=jload(file)
    FPS_LIMIT=jsonData["display"]["fps"]
    SC_RES=jsonData["display"]["screen_size"]
    TILE_SIZE=16
win=dsp.set_mode(SC_RES)
plr=Player(0,0)
MAP=[[Block("grass1",pos=(x,y))if char=="G" else
      Block("empty", pos=(x,y))if char==" " else
      Block("sand-floor1",(x,y))if char=="S" else
      Block("env-error",pos=(x,y))
      for x,char   in enumerate(string)]
      for y,string in enumerate(TXTMAP)]

while(True):
    keys=key.get_pressed()
    if keys[K_ESCAPE]or event.get(QUIT):break
    plr.update(keys)

    win.fill('black')
    [[tile.draw(win,(-plr.x,-plr.y))for tile in tiles]
                                  for tiles in MAP]
    win.blit(GameFont.render(str(int(clock.get_fps())),0,"#C0FFEE"),(10,10))
    win.blit(GameFont.render(str(int(plr.x)),0,"#C0FFEE"),(10,25))
    win.blit(GameFont.render(str(int(plr.y)),0,"#C0FFEE"),(10,40))
    clock.tick(FPS_LIMIT)
    dsp.flip()
quit()
