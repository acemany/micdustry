from pygame import (KEYDOWN, FINGERDOWN, FINGERMOTION, MULTIGESTURE,
                    display, draw, event, mouse, font, time,
                    QUIT, MOUSEMOTION,
                    init, quit,
                    Vector2)
from sys import exit as sys_exit

init()
win = display.set_mode()
width, height = win.get_size()
MFont = font.SysFont("Arial", 15)
clock = time.Clock()

pos = Vector2(width//2, height//2)
dpos = Vector2()
tpinched = 0.01
MMove = False

while 1:
    win.fill((0, 0, 0))
    FDwns = event.get(FINGERDOWN)
    FMovs = event.get(FINGERMOTION)
    MMovs = event.get(MOUSEMOTION)
    MPos = mouse.get_pos()

    if event.get(QUIT):
        break
    for a in FMovs:
        ddpos = Vector2()
        if a.finger_id == 0:
            ddpos = a.dx*width, a.dy*height
        if a.finger_id == 1 and MMovs:
            MMove = True
            dpos = ddpos+(a.dx*width, a.dy*height)
    if MMove:
        for b in MMovs:
            dpos += b.rel
        MMove = False
        dpos /= 2
        pos += dpos

    win.blits([(MFont.render(f"{a.dict}", 1, (128, 128, 128)), (0, 15*b))for b, a in enumerate(event.get(KEYDOWN))])

    for a in event.get(MULTIGESTURE):
        tpinched += a.pinched*2

    draw.circle(win, (255, 191, 255), pos, abs(width*tpinched), 2)
    display.flip()
    clock.tick(1)

quit()
sys_exit()
