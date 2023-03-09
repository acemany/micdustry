from pygame.constants import (KEYDOWN,QUIT,
K_ESCAPE,K_LCTRL,K_EQUALS,K_MINUS,
    K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,
    K_w,K_a,K_s,K_d,K_l,K_e,K_x,K_k,K_p)
from pygame import (
    init,quit,time,image,Surface,
    event,key,mouse,display as disp)
from typing import List

from settings import sets
from sprites import Block
from fonts import MainFont

FPS_LIMIT=sets["display"]["fps"]
SC_RES=sets["display"]["screen_size"]
TILE_LIST=["error","sand","grass","empty"]
class Player():
    def __init__(self,x:int,y:int):
        self.xv=self.yv=0
        self.x=x
        self.y=y
    @property
    def pos(self):return self.x,self.y
    @property
    def velocity(self):return self.xv,self.yv
    def update(self,keys):
        if keys[K_w]:self.yv-=1
        if keys[K_a]:self.xv-=1
        if keys[K_s]:self.yv+=1
        if keys[K_d]:self.xv+=1
        self.x+=self.xv
        self.y+=self.yv
        self.xv-=self.xv*0.0625
        self.yv-=self.yv*0.0625

class Map:
    def __init__(self,filename:str,load=True):
        if load:
            with open(f"maps/{filename}.msav","r")as file:
                txt=file.read()
                self.bottom_map=[[Block(char,(x,y))
                for x,char in enumerate(row.split(","))]
                for y,row  in enumerate(txt.split("\n"))]
        global current_state
        current_state="Loaded"
    def draw(self,win:Surface,offset:List[int],dist:int):
        [[tile.draw(win,offset,dist)
        for tile in tiles]for tiles in self.bottom_map]
    def save(self):
        with open("maps/map_test.msav","w")as file:
            txt=""
            for tiles in self.bottom_map:
                for tile in tiles:txt+=f"{tile.block_id},"
                txt+="\n"
            txt+="j"
            file.write(txt.replace(",\n","\n").replace("\nj",""))
        global current_state
        current_state="Saved"

def main():
    win=disp.set_mode(SC_RES)
    current_state="loading"

    #INIT
    init()
    debug=False
    editor=False
    pause=False
    current_tile=1
    clock=time.Clock()
    tilemap=Map("map_test")
    mouse.set_visible(False)
    statetextoff=SC_RES[0]*0.5
    plr=Player(SC_RES[0]*0.5,SC_RES[1]*0.5)
    TILE_SIZE=distance=int(sets["display"]["tile_size"])
    mainFont=MainFont(sets["colors"]["font"],16)
    disp.set_icon(image.load("icon.bmp").convert())
    cursor=image.load("sprites/cursors/cursor.bmp").convert()
    cursor.set_colorkey((255,0,255))
    current_state="Game" if not editor else "Editor"

    while(True):
        keys=key.get_pressed()

        if keys[K_ESCAPE]and event.get(KEYDOWN)or event.get(QUIT):break
        elif keys[K_p]and event.get(KEYDOWN):
            pause=not pause
            if pause:current_state="pause"
            else:current_state="Game"
        elif keys[K_e]and event.get(KEYDOWN):
            editor=not editor
            if editor:current_state="Editor"
            else:current_state="Game"
        if not pause:
            if all((keys[K_l],keys[K_e])):
                conf_debug=True;current_state="press Esc."
            if all((keys[K_x],keys[K_e],keys[K_k])):
                if conf_debug:debug=not debug;conf_debug=False;current_state="LOL)"
            if editor:
                if   keys[K_LCTRL]and keys[K_s]and event.get(KEYDOWN):
                    tilemap.save()
                elif keys[K_LCTRL]and keys[K_l]and event.get(KEYDOWN):
                    tilemap=Map("map_test")
                #FIXME
                #elif keys[K_LCTRL]and keys[K_n]and event.get(KEYDOWN):
                #    key.set_text_input_rect((0,0,SC_RES[0],SC_RES[1]))
                #    current_state="Name of new map:__________"
                #    statetextoff=SC_RES[0]*0.35
                #    key.start_text_input()
                #    key.stop_text_input()
                #    tilemap=Map(name,False);current_state="Created"
                #    statetextoff=SC_RES[0]*0.5

                elif keys[K_0]and event.get(KEYDOWN):current_tile=0
                elif keys[K_1]and event.get(KEYDOWN):current_tile=1
                elif keys[K_2]and event.get(KEYDOWN):current_tile=2
                elif keys[K_3]and event.get(KEYDOWN):current_tile=3
                elif keys[K_4]and event.get(KEYDOWN):current_tile=4
                elif keys[K_5]and event.get(KEYDOWN):current_tile=5
                elif keys[K_6]and event.get(KEYDOWN):current_tile=6
                elif keys[K_7]and event.get(KEYDOWN):current_tile=7
                elif keys[K_8]and event.get(KEYDOWN):current_tile=8
                elif keys[K_9]and event.get(KEYDOWN):current_tile=9

                if mouse.get_pressed()[0]:
                    if False:...
                    else:
                        tilex=(mouse.get_pos()[0]+int(plr.x)*distance//TILE_SIZE)//distance
                        tiley=(mouse.get_pos()[1]+int(plr.y)*distance//TILE_SIZE)//distance
                        if tilex>=0 and tiley>=0:
                            try:tilemap.bottom_map[tiley][tilex]=Block(
                                TILE_LIST[current_tile],(tilex,tiley))
                            except IndexError:pass
            if keys[K_EQUALS]and distance<64:distance+=distance//4
            if keys[K_MINUS]and distance>5:distance-=distance//4
            plr.update(keys)

            win.fill((32,32,32))
            tilemap.draw(win,plr.pos,distance)
            mainFont.draw(win,f"{current_state}",(statetextoff,5))
            try:mainFont.draw(win,f"{TILE_LIST[current_tile]}",(5,5))
            except Exception as e:current_state=f"{e}";current_tile=0
            if debug:
                mainFont.draw(win,f"{int(clock.get_fps(       ))}",(5,20))
                mainFont.draw(win,f"{list(map(int,plr.pos     ))}",(5,35))
                mainFont.draw(win,f"{list(map(int,plr.velocity))}",(5,50))
            win.blit(cursor,(mouse.get_pos()[0]-29,mouse.get_pos()[1]-29))
        clock.tick(FPS_LIMIT)
        disp.flip()
    quit()

if __name__=="__main__":main()
