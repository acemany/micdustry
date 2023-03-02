from pygame.constants import K_w,K_a,K_s,K_d

class Player():
    def __init__(self,x:int,y:int):
        self.xv=0
        self.yv=0
        self.x=x
        self.y=y
    def update(self,keys):
        if keys[K_w]:self.yv-=1
        if keys[K_a]:self.xv-=1
        if keys[K_s]:self.yv+=1
        if keys[K_d]:self.xv+=1
        self.x+=self.xv;self.xv*=0.9
        self.y+=self.yv;self.yv*=0.9
