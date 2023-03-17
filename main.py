from pygame.constants import (KEYDOWN,QUIT,
    K_ESCAPE,K_LCTRL,K_MINUS,K_EQUALS,
    K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,
    K_w,K_e,K_u,K_p,K_a,K_s,K_d,K_l,K_m)
from pygame import (init,quit,time,image,Surface,font,
    transform,event,key,mouse,display)
from random import randint
from typing import Tuple

from settings import sets

SC_RES=sets["display"]["screen_size"]
TILE_LIST={
    "environment":
        ("empty","sand","grass","stone")}
TILE_SIZE=distanc=int(sets["display"]["tile_size"])

class Player:
    def __init__(self,pos:Tuple[int,int]=(0,0)):
        self.xv=self.yv=0
        self.x=pos[0]
        self.y=pos[1]
    @property
    def pos(self):return list(map(int,(self.x,self.y)))
    @property
    def velocity(self):return list(map(int,(self.xv,self.yv)))
    def update(self,keys):
        if keys[K_w]:self.yv-=1
        if keys[K_a]:self.xv-=1
        if keys[K_s]:self.yv+=1
        if keys[K_d]:self.xv+=1
        self.x+=self.xv
        self.y+=self.yv
        self.xv*=0.9
        self.yv*=0.9
class Block:
    def __init__(self,block_id:str,pos:Tuple[int,int],
    variants:int=3,path:str="bottom"):
        self.x=pos[0]*TILE_SIZE
        self.y=pos[1]*TILE_SIZE
        self.block_id=block_id
        self.path=path
        try:self.image=self.rimage=transform.scale(image.load(
            f"sprites/blocks/{self.path}/{self.block_id}{randint(1,variants)}.bmp"
            ).convert(),(TILE_SIZE,TILE_SIZE))
        except FileNotFoundError:
            self.image=self.rimage=transform.scale(image.load(
            "sprites/blocks/bottom/empty.bmp"
            ).convert(),(TILE_SIZE,TILE_SIZE))
    def resize(self,size2):self.image=transform.scale(self.rimage,(size2,size2))
    def draw(self,surface:Surface,offset:Tuple[int,int],distanc:int):
        surface.blit(self.image,
            (((self.x-offset[0])*distanc/TILE_SIZE),
            ((self.y-offset[1])*distanc/TILE_SIZE)))
class Font:
    class Main:
        def __init__(self,color:str="BBBBBB",scale:int=6):
            self.Font=font.Font("gameFont.woff",scale)
            self.color=color
        def draw(self,win:Surface,text:str,antialians:int,pos:Tuple[int,int]):
                win.blit(self.Font.render(text,antialians,self.color),pos)
class Map:
    def __init__(self,filename:str):
        global current_state
        with open(f"maps/{filename}.msav","r")as file:txt=file.read()
        self.bottom_map=[[
            Block(char,(x,y))if char!="empty"else Block(char,(x,y),1)
            for x,char in enumerate(row.split(","))]
            for y,row  in enumerate(txt.split("\n"))]
        current_state="Loaded"
    def resize(self,size:int):
        [[tile.resize(size)
        for tile in tiles]for tiles in self.bottom_map]
    def draw(self,win:Surface,offset:Tuple[int,int],dist:int):
        [[tile.draw(win,offset,dist)
        for tile in tiles]for tiles in self.bottom_map]
    def save(self,filename:str):
        with open(f"maps/{filename}.msav","w")as file:
            txt=""
            for tiles in self.bottom_map:
                for tile in tiles:txt+=f"{tile.block_id},"
                txt+="\n"
            txt+="j"
            file.write(txt.replace(",\n","\n").replace("\nj",""))
        global current_state
        current_state="Saved"

if __name__=="__main__":
    CLOCK=time.Clock()
    current_state="loading"
    WIN=display.set_mode(SC_RES)
    display.set_icon(image.load("icon.bmp").convert())

    #INIT
    init()
    mous=1
    debug=0
    pause=0
    editor=1
    PLR=Player()
    current_tile=1
    font_antialias=1
    current_map_name="map0"
    state_x_pos=SC_RES[0]*0.5
    tilemap=Map(current_map_name)
    current_category="environment"
    MAINFONT=Font.Main(sets["colors"]["font"],16)
    current_state="Game"if not editor else"Editor"
    CURSOR=image.load("sprites/cursors/cursor.bmp").convert()
    CURSOR.set_colorkey((255,0,255))
    mouse.set_visible(not mous)

    while(True):
        keys=key.get_pressed()
        if keys[K_ESCAPE]or event.get(QUIT):break
        if keys[K_LCTRL]:
            if   keys[K_s]:tilemap.save(current_map_name)
            elif keys[K_l]:tilemap= Map(current_map_name)
        elif keys[K_EQUALS]and distanc<64:distanc+=1;tilemap.resize(distanc)
        elif keys[K_MINUS ]and distanc>5 :distanc-=1;tilemap.resize(distanc)
        if keys[K_m] and event.get(KEYDOWN):
                mouse.set_visible(mous)
                mous=not mous
        if keys[K_p] and event.get(KEYDOWN):
                pause=not pause
                current_state="Paused"if pause else "Unpaused"
        if keys[K_e] and event.get(KEYDOWN):
                editor=not editor
                current_state="Editor"if editor else"Game"
                
        if not pause:
            PLR.update(keys)
            if all((keys[K_l],keys[K_u],keys[K_a],event.get(KEYDOWN))):
                debug=not debug
        if editor:
            if mouse.get_pressed()[0]:
                tilex=int(mouse.get_pos()[0]+int(PLR.x)*distanc/TILE_SIZE)//distanc
                tiley=int(mouse.get_pos()[1]+int(PLR.y)*distanc/TILE_SIZE)//distanc
                if tilex>=0 and tiley>=0:
                    try:
                        if TILE_LIST[current_category][current_tile
                            ]!=tilemap.bottom_map[tiley][tilex].block_id:
                            tilemap.bottom_map[tiley][tilex]=Block(
                            TILE_LIST[current_category][current_tile],(tilex,tiley))
                    except IndexError:pass
            elif keys[K_0]:current_tile=0
            elif keys[K_1]:current_tile=1
            elif keys[K_2]:current_tile=2
            elif keys[K_3]:current_tile=3
            elif keys[K_4]:current_tile=4
            elif keys[K_5]:current_tile=5
            elif keys[K_6]:current_tile=6
            elif keys[K_7]:current_tile=7
            elif keys[K_8]:current_tile=8
            elif keys[K_9]:current_tile=9

        tilemap.draw(WIN,PLR.pos,distanc)
        MAINFONT.draw(WIN,f"{current_state}",font_antialias,(state_x_pos,5))
        try:MAINFONT.draw(WIN,f"""{TILE_LIST[
                current_category][current_tile]}""",font_antialias,(5,5))
        except Exception as e:current_state=f"{e}";current_tile=0
        if debug:
            MAINFONT.draw(WIN,f"{int(CLOCK.get_fps())}",font_antialias,(5,20))
            MAINFONT.draw(WIN,f"{PLR.pos             }",font_antialias,(5,35))
            MAINFONT.draw(WIN,f"{PLR.velocity        }",font_antialias,(5,50))
        if mous:WIN.blit(CURSOR,(mouse.get_pos()[0]-29,mouse.get_pos()[1]-29))
        CLOCK.tick(120)
        display.flip()
        WIN.fill((15,15,15))
    quit()
