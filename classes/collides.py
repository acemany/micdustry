class collided:
    def circles(x1,y1,r1,x2,y2,r2)->bool:
        return ((x2-x1)**2+(y2-y1)**2)**0.5<r1+r2
    def boxes(x1,y1,w1,h1,x2,y2,w2,h2)->bool:
        return (x1+w1>x2-w2 and
                x1-w1<x2+w2 and
                y1+h1>y2-h2 and
                y1-h1<y2+h2)
