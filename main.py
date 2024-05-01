from pygame import (display, draw, event, font, image, key, mouse, sprite, time, transform,
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, WINDOWRESIZED,
                    KEYDOWN, MOUSEWHEEL, FINGERDOWN, FINGERMOTION, MULTIGESTURE,
                    K_a, K_c, K_d, K_e, K_m, K_o, K_p, K_s, K_w,
                    K_ESCAPE, K_EQUALS, K_MINUS, K_PAUSE,
                    Rect, Surface, Vector2,
                    KMOD_LSHIFT, KMOD_LCTRL,
                    init, quit as Squit,
                    RESIZABLE)
from potaget import c_p_r, log, open_file_as, save_file_as
# from multiprocessing import freeze_support
# from threading import Thread as newThread
from json import dump, load
from random import randint
from typing import Tuple
from math import atan2


class Player:
    def __init__(self, pos: Vector2 = (0, 0), speed: float = 0.5):
        self.pos = Vector2(pos)
        self.speed = speed
        self.vel = Vector2()

    def update(self, keymap: Tuple[bool]):
        if keymap[K_d]:
            self.vel.x += self.speed
        if keymap[K_a]:
            self.vel.x -= self.speed
        if keymap[K_s]:
            self.vel.y += self.speed
        if keymap[K_w]:
            self.vel.y -= self.speed
        self.pos += self.vel
        self.vel *= 0.8


class Entity(sprite.Sprite):
    @property
    def get_pos(self):
        return self.pos

    def __init__(self, pos: Vector2 = (2, 2), type: str = "dagger", angle: int = 0,
                 groups: Tuple[sprite.Group] = [], player: bool = False):
        super().__init__(*groups)
        self.rimage = image.load(f"sprites/units/{type}/body.png").convert_alpha()
        self.player = player
        entitys.append(self)
        self.image = self.rimage.copy()
        self.rpos = Vector2(pos)
        self.pos = self.rpos*distance
        self.vvec = Vector2()
        self.angle = angle
        self.w, self.h = self.image.get_size()
        self.rr = max(self.w, self.h)/2/distance
        self.r = self.rr*distance
        self.collided = 0
        self.type = type
        self.speed = 1
        self.rect = Rect(*(self.pos-(self.w, self.h)), self.w, self.h)

    def __repr__(self):
        return f"<Entity {'Player'if self.player else 'Entity'}(pos = {self.rpos}, force = {self.vvec})>"

    def move_to(self, tox_y: Vector2, ratio: int = 1):
        self.vvec += ((tox_y-self.rpos)/ratio)

    def move_off(self, x_yoff: Vector2):
        self.vvec += x_yoff

    def set_pos(self, x_y: Vector2):
        self.rpos.update(x_y)

    def update(self):
        if self.player:
            if KPrss[K_w]:
                self.vvec.y -= self.speed  # ( self.speed*cosa, self.speed*sina)
            if KPrss[K_s]:
                self.vvec.y += self.speed  # (-self.speed*cosa, -self.speed*sina)
            if KPrss[K_a]:
                self.vvec.x -= self.speed  # ( self.speed*sina, -self.speed*cosa)
            if KPrss[K_d]:
                self.vvec.x += self.speed  # (-self.speed*sina, self.speed*cosa)
            self.angle = (self.angle*0.8+atan2(*(MPos-self.pos).yx)*0.2)
        self.angle = (self.angle*0.9+atan2(*self.vvec.yx)*0.1)
        self.r = self.rr*distance
        self.rpos += self.vvec
        self.pos = self.rpos*distance
        self.rect = Rect(*self.pos-(self.r, self.r), self.r*2, self.r*2)
        self.vvec *= 0.7

    def draw(self):
        pos = -CAM.pos*distance_ratio+self.rect.center+h_sc_res
        draw.circle(win, (self.collided, 0, 255-self.collided), pos.xy, self.r, 1)
        self.image = transform.rotate(Sscale(self.rimage, (int(self.w*distance_ratio),
                                                           int(self.h*distance_ratio))), -self.angle*57.2958-90)
        win.blit(self.image, self.image.get_rect(center=pos))


class Block(sprite.Sprite):
    def __init__(self, groups: sprite.Group, block_id: str, pos: Tuple[int, int]):
        global distance
        super().__init__(groups)
        self.block_id = block_id
        self.pos = Vector2(pos)
        self.rect = Rect((*Vector2(pos)*distance, distance, distance))
        if block_id == "floor_none":
            self.rimage = self.image = Surface((distance, distance))
        else:
            try:
                self.rimage = cached_images[f"{block_id}"][randint(0, len(cached_images[f"{block_id}"])-1)]
                self.image = Sscale(self.rimage, (distance, distance))
            except IndexError as e:
                log(f"Error, image not loaded: {e}")
                self.image = self.rimage = cached_images["floor_error"][0]
        if block_id.split("_", 1)[0] == "wall":
            walls_collider.append(self)
        self.w, self.h = self.rimage.get_size()

    def update(self):
        "resize"
        self.rect = Rect((*self.pos*distance, distance, distance))
        self.image = Sscale(self.rimage, (distance, distance))

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)

    def kill(self):
        super().kill()
        if self in walls_collider:
            walls_collider.remove(self)


class Map:
    def __init__(self, name: str = ""):
        global cached_images, distance
        self.name = name
        with open(f"maps/{name}.msav"if name else open_file_as("msave"), "r")as file:
            txt = file.read()
        categories = txt.split("\n|")
        content = {
            "blocks": [[char for char in row.split(",")]for row in categories[0].split("\n")],
            "enemy spawn": list(map(int, categories[1].split(","))),
            "walls": [[char for char in row.split(",")]for row in categories[2].split("\n")]}
        self.enemy_spawn = content["enemy spawn"]
        self.floor_blocks = sprite.Group()
        self.floor_blocks_grid = [[Block(self.floor_blocks, char, (x, y))for x, char in enumerate(row)]
                                  for y, row in enumerate(content["blocks"])]
        self.wall_blocks = sprite.Group()
        self.wall_blocks_grid = [[Block(self.wall_blocks, char, (x, y))for x, char in enumerate(row)]
                                 for y, row in enumerate(content["walls"])]
        self.rsurfsize = Vector2(len(self.floor_blocks_grid[0])*distance,
                                 len(self.floor_blocks_grid)*distance)
        self.surfsize = Vector2(self.rsurfsize)
        self.rfloor_surface = Surface(self.surfsize)
        self.floor_surface = self.rfloor_surface.copy()
        [[block.draw(self.floor_surface)for block in blocks]for blocks in self.floor_blocks_grid]
        self.rwall_surface = Surface(self.surfsize)
        self.wall_surface = self.rwall_surface.copy()
        [[block.draw(self.wall_surface)for block in blocks]for blocks in self.wall_blocks_grid]
        self.resize()

    def resize(self):
        self.surfsize = self.rsurfsize*distance_ratio
        self.floor_surface.__init__(self.surfsize)
        self.wall_surface.__init__(self.surfsize)
        self.floor_surface.set_colorkey((0, 0, 0))
        self.wall_surface.set_colorkey((0, 0, 0))
        self.floor_blocks.update()
        self.wall_blocks.update()
        self.floor_blocks.draw(self.floor_surface)
        self.wall_blocks.draw(self.wall_surface)

    def place(self, delete: bool = False):
        block_pos = MPos+CAM.pos/BLOCK_SIZE*distance-h_sc_res
        if 0 <= block_pos[0] < self.surfsize[0] and 0 <= block_pos[1] < self.surfsize[1]:
            block_pos = block_pos//distance
            editor_til = "floor_none"if delete else editor_tile
            block = self.floor_blocks_grid[int(block_pos[1])][int(block_pos[0])]if editor_category ==\
                0 else self.wall_blocks_grid[int(block_pos[1])][int(block_pos[0])]
            if editor_til == block.block_id:
                return
            block.kill()
            block.__init__(self.wall_blocks if editor_category == 1 else self.floor_blocks, editor_til, block_pos)
            block.draw(self.wall_surface if editor_category == 1 else self.floor_surface)

    def draw(self):
        pos = -(CAM.pos*distance_ratio-h_sc_res)
        win.blit(self.floor_surface, pos)
        win.blit(self. wall_surface, pos)

    def save(self, name: str = ""):
        with open(f"maps/{name}.msav"if name else save_file_as("msave"), "w")as file:
            txt = ""
            for tiles in self.floor_blocks_grid:
                for tile in tiles:
                    txt += f"{tile.block_id}, "
                txt += "\n"
            txt += f"|{self.enemy_spawn[0]}, {self.enemy_spawn[1]}\n|"
            for tiles in self.wall_blocks_grid:
                for tile in tiles:
                    txt += f"{tile.block_id}, "
                txt += "\n"
            txt = txt.replace(", \n", "\n")[: -1]
            file.write(txt)


class Switch:
    def __init__(self, truth: bool = False, swithable: bool = True, name: str = "boolean"):
        self.switchable = swithable
        self.truth = truth
        self.name = name

    @property
    def switch(self):
        self.truth = not self.truth
        return self.truth

    def draw(self, pos: Tuple[int, int]):
        if self.truth:
            if self.switchable:
                if c_p_r(*MPos, *pos, *sw_size):
                    win.blit(sw_on_over, pos)
                else:
                    win.blit(sw_on, pos)
            else:
                win.blit(sw_on_disabled, pos)
        else:
            if self.switchable:
                if c_p_r(*MPos, *pos, *sw_size):
                    win.blit(sw_off_over, pos)
                else:
                    win.blit(sw_off, pos)
            else:
                win.blit(sw_off_disabled, pos)
        return MAINFONT.render(self.name, font_antialias, Ctext), (pos[0]+sw_size[0]+4, pos[1]+(sw_size[1]-font_height)/2)


class Slider:
    def __init__(self, num: int = 0, name: str = "variable"):
        self.name = name
        self.on = False
        self.num = num

    def draw(self):
        out = Surface((h_width+slid_pw, slid_h))
        out.set_colorkey((0, 0, 0))
        draw.rect(out, (69, 69, 69), (0, 0, h_width+slid_pw, slid_h), slid_bw)
        draw.rect(out, (255, 255, 255) if self.on else (69, 69, 69), (self.num*slid_SC, 0, slid_pw, slid_h))
        out.blits(((MAINFONT.render(f"{self.num}", font_antialias, Ctext),
                    (h_width-MAINFONT.size(f"{self.num}")[0]-slid_bw, (slid_h-font_height)/2)),
                   (MAINFONT.render(self.name, font_antialias, Ctext),
                    (slid_bw+slid_pw, (slid_h-font_height)/2))))
        return out


def make_button(size: Tuple[int, int], over: bool = False):
    size = (max(size[0], butw), max(size[1], buth))
    out = Surface(Vector2(36, 27)+size)
    out.fill((255, 0, 255))
    out.set_colorkey((255, 0, 255))
    color = (255, 255, 255) if over else (69, 69, 69)
    draw.polygon(out, (0, 0, 0), ((1, buth2-4),
                                  (butw2-9, 1),
                                  (size[0]-butw2+9, 1),
                                  (size[0]-1, buth2-4),
                                  (size[0]-1, size[1]-buth2+4),
                                  (size[0]-butw2+9, size[1]-1),
                                  (butw2-9, size[1]-1),
                                  (1, size[1]-buth2+4)))
    draw.lines(out, color, 1, ((1, buth2-4),
                               (butw2-9, 1),
                               (size[0]-butw2+9, 1),
                               (size[0]-1, buth2-4),
                               (size[0]-1, size[1]-buth2+4),
                               (size[0]-butw2+9, size[1]-1),
                               (butw2-9, size[1]-1),
                               (1, size[1]-buth2+4)), 4)
    draw.line(out, color, (1, buth2-4), (butw2-9, 1), 6)
    draw.line(out, color, (size[0]-butw2+8, 1), (size[0]-1, buth2-3), 5)
    draw.line(out, color, (size[0]-1, size[1]-buth2+4), (size[0]-butw2+8, size[1]), 5)
    draw.line(out, color, (butw2-8, size[1]), (1, size[1]-buth2+4), 6)
    return out


def reinit_textures():
    global win, sc_res, width, height, h_sc_res, h_width, h_height, q_sc_res, q_width, q_height, Stitle, Sinfo, Sexit, \
        sw_on_disabled, sw_on_over, sw_on, sw_off_disabled, sw_off_over, sw_off, menu_gap, mbuth, mbutw, butw, \
        buth, butw2, buth2, slid_pw, slid_h, slid_bw, slid_SC, sw_size, TB_pos, TB_x, TB_y, TOOLBAR_SURFACES, \
        icon_defense, icon_secret, icon_break
    win = display.set_mode((max(300, a.x), max(300, a.y))
                           if not Gf11 else (0, 0), RESIZABLE, vsync=Gvsync)
    sc_res = width,  height = Vector2(win.get_size())
    h_sc_res = h_width, h_height = sc_res/2
    q_sc_res = q_width, q_height = sc_res/4

    Stitle = Sscale(Srtitle, (int(width*0.96), int(width*0.13375)))
    Sinfo = Sscale(Srinfo, (int(width*0.105), int(width*0.05625)))
    Sexit = Sscale(Srexit, (int(width*0.04), int(width*0.04)))
    sw_on_disabled = Sscale(rsw_on_disabled, (int(width*0.03), int(width*0.03)))
    sw_on_over = Sscale(rsw_on_over, (int(width*0.03), int(width*0.03)))
    sw_on = Sscale(rsw_on, (int(width*0.03), int(width*0.03)))
    sw_off_disabled = Sscale(rsw_off_disabled, (int(width*0.03), int(width*0.03)))
    sw_off_over = Sscale(rsw_off_over, (int(width*0.03), int(width*0.03)))
    sw_off = Sscale(rsw_off, (int(width*0.03), int(width*0.03)))
    icon_defense = Sscale(ricon_defense, (distance, distance))
    icon_secret = Sscale(ricon_secret, (distance, distance))
    icon_break = Sscale(ricon_break, (distance, distance))
    menu_gap = width*0.04
    mbuth, mbutw = width*0.06, width*0.32
    butw, buth = 36, 27
    butw2, buth2 = butw//2, buth//2
    slid_pw = h_width/20
    slid_h = width*0.03
    slid_bw = int(slid_h//6)
    slid_SC = h_width/100
    sw_size = sw_on.get_size()
    TB_pos = TB_x, TB_y = h_sc_res+q_sc_res
    TOOLBAR_SURFACES = [Surface(q_sc_res)for a in range(2)]
    [(draw.rect(a, (69,  69,   69), (0, 0, q_width, q_height)),
      draw.rect(a, (103, 103, 103), (2, 2, q_width, q_height)))for a in TOOLBAR_SURFACES]
    [(TOOLBAR_SURFACES)[a].blits([(Sscale(surf, (distance, distance)), ((pos % ((q_width-24)//24))*24+6,
                                                                        pos // ((q_width-24)//24)*24+6))
     for pos, surf in enumerate(surfs)])
        for a, surfs in enumerate(to_toolbar)]

    [(draw.lines(surf, (69, 69, 69), False, ((q_width-24, 0), (q_width-24, q_height-24), (0, q_height-24)), 2),
        surf.blits(((icon_defense, (q_width-distance-4, 6)),
                    (icon_secret, (q_width-distance-4, 30)),
                    (icon_break, (6, q_height-distance-4)))))
        for surf in TOOLBAR_SURFACES]


def leave():
    with open("settings.json", "w")as f:
        dump({"font_antialias": font_antialias,
              "antialias": Sscale == transform.smoothscale,
              "fullscreen": Gf11,
              "vsync": Gvsync,
              "devpop": dev,
              "mouse": mous,
              "max_fps": max_FPS,
              "mobile_ui": Gmobui,
              "font_size": int(SLfont_size.num)}, f)
    Squit()
    quit()


init()
# freeze_support()

with open("settings.json", "r")as f:
    json_data = load(f)
    dev = json_data["devpop"]
    mous = json_data["mouse"]
    Gvsync = json_data["vsync"]
    max_FPS = json_data["max_fps"]
    Gf11 = json_data["fullscreen"]
    Gmobui = json_data["mobile_ui"]
    BLOCK_SIZE = distance = 16
    font_antialias = json_data["font_antialias"]
    Sscale = transform.smoothscale if json_data["antialias"] else transform.scale
    win = display.set_mode((800, 600) if not Gf11 else (0, 0), flags=RESIZABLE, vsync=Gvsync)
    MAINFONT = font.Font("gameFont.woff", json_data["font_size"])
    font_height = json_data["font_size"]
    Ctext = (127, 127, 127)

try:
    Srtitle = image.load("sprites/logo.png").convert_alpha()
    Srinfo = image.load("sprites/ui/info.png").convert_alpha()
    Srexit = image.load("sprites/ui/exit.png").convert_alpha()
    ricon_defense = image.load("sprites/ui/defense.png").convert_alpha()
    ricon_secret = image.load("sprites/ui/secret.png").convert_alpha()
    ricon_break = image.load("sprites/ui/break.png").convert_alpha()
    CURSOR = image.load("sprites/cursors/cursor.png").convert_alpha()
    rsw_on_disabled = image.load("sprites/ui/switch-on-disabled.png").convert_alpha()
    rsw_on_over = image.load("sprites/ui/switch-on-over.png").convert_alpha()
    rsw_on = image.load("sprites/ui/switch-on.png").convert_alpha()
    rsw_off_disabled = image.load("sprites/ui/switch-off-disabled.png").convert_alpha()
    rsw_off_over = image.load("sprites/ui/switch-off-over.png").convert_alpha()
    rsw_off = image.load("sprites/ui/switch-off.png").convert_alpha()
    files_to_cache = {
        "floor_char": ["floor_char1", "floor_char2", "floor_char3"],
        "floor_dark-panel": ["floor_dark-panel1", "floor_dark-panel2", "floor_dark-panel3", "floor_dark-panel4",
                             "floor_dark-panel5", "floor_dark-panel6"],
        "floor_error": ["floor_error1"],
        "floor_grass": ["floor_grass1", "floor_grass2", "floor_grass3"],
        "floor_none": ["floor_none1"],
        "floor_sand": ["floor_sand1", "floor_sand2", "floor_sand3"],
        "floor_stone": ["floor_stone1", "floor_stone2", "floor_stone3", "floor_stone4", "floor_stone5", "floor_stone6",
                        "floor_stone7", "floor_stone8", "floor_stone9"],
        "wall_char": ["wall_char1", "wall_char2"],
        "wall_copper": ["wall_copper1"],
        "wall_dark-panel": ["wall_dark-panel1", "wall_dark-panel2"],
        "wall_grass": ["wall_grass1", "wall_grass2"],
        "wall_sand": ["wall_sand1", "wall_sand2"],
        "wall_stone": ["wall_stone1", "wall_stone2"]}
    cached_images = {a: [image.load(f"sprites/blocks/{b}.png").convert()
                         for b in files_to_cache[a]]
                     for a in files_to_cache}
    to_toolbar = [[]for a in range(2)]
    for a in cached_images:
        path = a.split("_", 1)
        if path[1] == "none" or path[1] == "error":
            continue
        to_toolbar[0 if path[0] == "floor"else
                   1 if path[0] == "wall" else 2].append(Sscale(cached_images[a][0], (24, 24)))
except Exception as e:
    log(f"Error while preparing textures: {e}")
    raise e

reinit_textures()

MPos = Vector2()

CLOCK = time.Clock()
SWpicAA = Switch(Sscale == transform.smoothscale, name="linear filtering")
SWvsync = Switch(Gvsync, name="vertical synchronization*")
SWfontAA = Switch(font_antialias, name="font antialias")
SWmobui = Switch(Gmobui, name="mobile ui")
SWdev = Switch(dev, name="dev mode???!?!?")
SWmouse = Switch(mous, name="in-game mouse")
SLfont_size = Slider(font_height, name="font size*")
SLmax_FPS = Slider(max_FPS, name="max FPS")
menu_page = 0  # menu, settings

while 1:
    win.fill((31, 31, 31))

    KPrss = key  .get_pressed()
    MPrss = mouse.get_pressed()
    MPos.update(mouse.get_pos())

    for a in event.get(QUIT, WINDOWRESIZED):
        if a.type == QUIT:
            leave()
        elif a.type == WINDOWRESIZED:
            reinit_textures()
    if menu_page == 0:
        if KPrss[K_ESCAPE]:
            leave()
        win.blits(((Sinfo, (0, height-Sinfo .get_height())),
                   (Stitle, (h_width-Stitle.get_width()/2, 0))))
        win.blits(((make_button((mbutw, mbuth), c_p_r(*MPos, h_width-width/6, Stitle.get_height(),             mbutw, mbuth)), (h_width-width/6, Stitle.get_height())),
                   (make_button((mbutw, mbuth), c_p_r(*MPos, h_width-width/6, Stitle.get_height()+mbuth+4,     mbutw, mbuth)), (h_width-width/6, Stitle.get_height()+mbuth+4)),
                   (make_button((mbutw, mbuth), c_p_r(*MPos, h_width-width/6, Stitle.get_height()+(mbuth+4)*2, mbutw, mbuth)), (h_width-width/6, Stitle.get_height()+(mbuth+4)*2))))
        win.blits(((MAINFONT.render("load",     font_antialias, Ctext), ((width-MAINFONT.size("load")[0])/2, Stitle.get_height()+mbuth/3)),
                   (MAINFONT.render("settings", font_antialias, Ctext), ((width-MAINFONT.size("settings")[0])/2, Stitle.get_height()+mbuth/3+mbuth+4)),
                   (MAINFONT.render("quit",     font_antialias, Ctext), ((width-MAINFONT.size("quit")[0])/2, Stitle.get_height()+mbuth/3+mbuth*2+8))))
        for a in event.get(MOUSEBUTTONDOWN):
            if c_p_r(*a.pos, h_width-width/6, Stitle.get_height(), mbutw, mbuth):
                CAM = Player()
                BLOCK_SIZE = distance = 16
                TB_pos = TB_x, TB_y = h_sc_res+q_sc_res

                MMove = False
                pause = False
                editor = True
                drawing = False
                erasing = False
                MResized = False
                ucontrol = False
                clearing = False
                u_purpos = Vector2()
                MPos = Vector2()

                editor_tile = "floor_none"
                mouse_world_pos = Vector2()
                editor_category = 0  # floor, wall
                entitys = [Entity()for a in []]
                walls_collider = [Block()for a in []]
                distance_ratio = distance/BLOCK_SIZE
                display.set_icon(image.load("icon.png"))
                MAP = Map("map1")
                if mouse:
                    mouse.set_visible(0)
                [Entity((16, 16))for a in range(10)]
                # wall_char, wall_copper, wall_dark-panel, wall_grass, wall_sand, wall_stone
                # floor_char, floor_dark-panel, floor_grass, floor_sand, floor_stone
                # error, none

                # PREDRAW
                # floor, walls
                TOOLBAR_SURFACES = [Surface(q_sc_res)for a in range(2)]
                [(draw.rect(a, (69,  69,   69), (0, 0, q_width, q_height)),
                  draw.rect(a, (103, 103, 103), (2, 2, q_width, q_height)))for a in TOOLBAR_SURFACES]

                [(TOOLBAR_SURFACES)[a].blits(((Sscale(surf, (distance, distance)), ((pos % (win.get_width()//24))*24+6,
                                                                                    pos // (win.get_width()//24)*24+6))
                                              for pos, surf in enumerate(surfs)))
                 for a, surfs in enumerate(to_toolbar)]

                [(draw.lines(surf, (49, 49, 49), False,
                             ((q_width-24, 0), (q_width-24, q_height-24), (0, q_height-24)), 2),
                    surf.blits(((icon_defense, (q_width-distance-4, 6)),
                                (icon_secret,  (q_width-distance-4, 30)),
                                (icon_break,   (6,  q_height-distance-4)))))
                    for surf in TOOLBAR_SURFACES]

                while 1:
                    win.fill((0, 0, 0))

                    KPrss = key  .get_pressed()
                    MPrss = mouse.get_pressed()
                    MDwns = event.get(MOUSEBUTTONDOWN, 0)
                    MMovs = event.get(MOUSEMOTION, 0)
                    MPos.update(mouse.get_pos())
                    FDwns = event.get(FINGERDOWN, 0)
                    FMovs = event.get(FINGERMOTION, 0)

                    if KPrss[K_ESCAPE]:
                        leave()
                    for a in event.get():
                        if a.type == QUIT:
                            leave()
                        elif a.type == WINDOWRESIZED:
                            reinit_textures()
                        elif a.type == KEYDOWN:
                            if a.mod == KMOD_LCTRL+KMOD_LSHIFT:
                                if KPrss[K_s]:
                                    target = MAP.save()
                                elif KPrss[K_o]:
                                    walls_collider = []
                                    target = MAP.__init__()
                            elif a.mod == KMOD_LCTRL:
                                if KPrss[K_s]:
                                    target = MAP.save("map1")
                                elif KPrss[K_o]:
                                    target = MAP.__init__("map1")
                            if KPrss[K_c]:
                                ucontrol = not ucontrol
                            if KPrss[K_m]:
                                mouse.set_visible(mous)
                                mous = not mous
                            if KPrss[K_p] or KPrss[K_PAUSE]:
                                pause = not pause
                            if KPrss[K_e]:
                                editor = not editor
                            if KPrss[K_EQUALS] and distance < 64:
                                distance += 1
                                distance_ratio = distance/BLOCK_SIZE
                                Map.resize(MAP)
                            elif KPrss[K_MINUS] and distance > 4:
                                distance -= 1
                                distance_ratio = distance/BLOCK_SIZE
                                Map.resize(MAP)
                        elif a.type == MOUSEWHEEL:
                            mouse_wheel_motion = int(distance+a.y)
                            if 8 <= mouse_wheel_motion <= 64:
                                distance = mouse_wheel_motion
                                MResized = True
                        elif a.type == FINGERMOTION:
                            if a.finger_id == 0:
                                dpos = Vector2(a.dx*width, a.dy*height)
                            if a.finger_id == 1 and MMovs:
                                MMove = True
                                dpos += Vector2(a.dx*width, a.dy*height)
                        elif a.type == MULTIGESTURE:
                            MResized = True
                            distance += a.pinched*16
                        if a.type == MOUSEBUTTONDOWN:
                            _dict = a.__dict__
                            if _dict["button"] == 1:
                                if c_p_r(*MPos, TB_x, TB_y, q_width, q_height):
                                    if editor_category == 0:
                                        if c_p_r(*MPos,   TB_x+6, TB_y+6, 24, 24):
                                            editor_tile = "floor_char"
                                        elif c_p_r(*MPos, TB_x+30, TB_y+6, 24, 24):
                                            editor_tile = "floor_dark-panel"
                                        elif c_p_r(*MPos, TB_x+54, TB_y+6, 24, 24):
                                            editor_tile = "floor_grass"
                                        elif c_p_r(*MPos, TB_x+78, TB_y+6, 24, 24):
                                            editor_tile = "floor_sand"
                                        elif c_p_r(*MPos, TB_x+102, TB_y+6, 24, 24):
                                            editor_tile = "floor_stone"
                                    elif editor_category == 1:
                                        if c_p_r(*MPos,   TB_x+6, TB_y+6, 24, 24):
                                            editor_tile = "wall_char"
                                        elif c_p_r(*MPos, TB_x+30, TB_y+6, 24, 24):
                                            editor_tile = "wall_copper"
                                        elif c_p_r(*MPos, TB_x+54, TB_y+6, 24, 24):
                                            editor_tile = "wall_dark-panel"
                                        elif c_p_r(*MPos, TB_x+78, TB_y+6, 24, 24):
                                            editor_tile = "wall_grass"
                                        elif c_p_r(*MPos, TB_x+102, TB_y+6, 24, 24):
                                            editor_tile = "wall_sand"
                                        elif c_p_r(*MPos, TB_x+126, TB_y+6, 24, 24):
                                            editor_tile = "wall_stone"
                                    if c_p_r(*MPos,   TB_x+q_width-distance-4, TB_y+30,                  24, 24):
                                        editor_category = 0
                                    elif c_p_r(*MPos, TB_x+q_width-distance-4, TB_y+6,                   24, 24):
                                        editor_category = 1
                                    elif c_p_r(*MPos, TB_x+6,                  TB_y+q_height-distance-4, 24, 24):
                                        erasing = not erasing
                                elif Gmobui and c_p_r(*MPos, 0, height-width*0.04, width*0.12, width*0.04):
                                    ucontrol = not ucontrol
                                else:
                                    if ucontrol:
                                        u_purpos = Vector2(mouse_world_pos[:])/distance
                                    else:
                                        drawing = True
                            elif _dict["button"] == 3:
                                clearing = True
                        elif a.type == MOUSEBUTTONUP:
                            drawing = False
                            clearing = False
                        if MMove:
                            for b in MMovs:
                                dpos += b.rel
                            MMove = False
                            CAM.pos -= dpos/(len(MMovs)+1)
                        if MResized:
                            MResized = False
                            distance_ratio = distance/BLOCK_SIZE
                            for a in entitys:
                                a.r = a.rr*BLOCK_SIZE/distance_ratio
                            MAP.resize()
                    if not pause:
                        CAM.update(KPrss)
                        if editor:
                            if drawing:
                                MAP.place(erasing)
                            elif clearing:
                                MAP.place(True)
                    MAP.draw()
                    for a, en in enumerate(entitys):
                        if not pause:
                            en.collided = 0
                            if ucontrol and u_purpos != (0, 0) and not en.player:
                                pto = (u_purpos-en.rpos)/16
                                if pto == (0, 0):
                                    pto = (0, 1e-8)
                                elif abs(pto[0])+abs(pto[1]) < 5:
                                    en.vvec += pto.normalize()/32
                                else:
                                    en.vvec += pto.normalize()/16
                            en.update()
                            for cub in walls_collider:
                                if cub.pos.x-en.w/2 < en.pos.x < cub.pos.x+cub.w+en.w/2:
                                    if cub.pos.y-en.h/2 < en.pos.y < cub.pos.y+cub.h+en.h/2:
                                        collided_pos = Vector2(
                                            max(cub.pos.x, min(en.pos.x, cub.pos.x+cub.w))-en.pos.x,
                                            max(cub.pos.y, min(en.pos.y, cub.pos.y+cub.h))-en.pos.y)
                                        if collided_pos.length() < en.r:
                                            if collided_pos.length() < 1:
                                                en.vvec -= (Vector2(randint(-1, 1), randint(-1, 1))/4+(0.5, 0.5))*en.speed
                                            else:
                                                en.vvec -= collided_pos/cub.w*en.speed/16
                                            en.collided = 255
                            for fn in entitys[a+1: len(entitys)]:
                                distxy = distx, disty = fn.rpos-en.rpos
                                dist = (distx**2+disty**2)**0.5
                                if dist >= fn.rr+en.rr:
                                    continue
                                if dist < 1:
                                    dist = 10
                                    force = Vector2(randint(-1, 1), randint(-1, 1))/20
                                else:
                                    force = distxy*(1/dist**2)/dist
                                en.vvec -= force
                                fn.vvec += force
                                en.collided = 255
                                fn.collided = 255
                        en.draw()

                    if Gmobui:
                        draw.rect(win, (69, 69, 69) if ucontrol else (49, 49, 49),
                                  (0, height-width*0.04, width*0.12, width*0.04))
                        draw.rect(win, (69, 69, 69), (0, height-width*0.04, width*0.12, width*0.04), slid_bw)
                        win.blit(MAINFONT.render("control", font_antialias, Ctext),
                                 ((width*0.12-MAINFONT.size("control")[0])/2,
                                  height-(width*0.04+font_height)/2))
                    win.blit(TOOLBAR_SURFACES[editor_category], h_sc_res+q_sc_res)
                    if dev:
                        win.blits(((MAINFONT.render(i, font_antialias, Ctext), (5, 5 + font_height*j))
                                  for j, i in enumerate((f"TILE: {editor_tile}",
                                                         f"FPS: {int(CLOCK.get_fps())}",
                                                         f"POS: {CAM.pos}",
                                                         f"SPEED: {CAM.vel}",
                                                         f"VIEWING RANGE: {distance}"))))
                    if mous:
                        win.blit(CURSOR, (MPos[0]-2, MPos[1]-2))
                    display.update()
                    CLOCK.tick(max_FPS)
                mouse.set_visible(True)
                KPrss = []
            elif c_p_r(*a.pos, h_width-width/6, Stitle.get_height()+mbuth+4,   mbutw, mbuth):
                menu_page = 1
            elif c_p_r(*a.pos, h_width-width/6, Stitle.get_height()+mbuth*2+8, mbutw, mbuth):
                leave()
    elif menu_page == 1:
        if KPrss[K_ESCAPE]:
            menu_page = 0
        if MPrss[0]:
            if SLfont_size.on:
                SLfont_size.num = min(max((MPos[0]-q_width-slid_pw/2)/slid_SC//0.25*0.25,   0), 100)
            if SLmax_FPS.on:
                SLmax_FPS  .num = max_FPS = min(max((MPos[0]-q_width-slid_pw/2)/slid_SC//1, 0), 100)
        for a in event.get(MOUSEBUTTONDOWN):
            if a.button == 1:
                SLfont_size.on = c_p_r(*MPos, q_width+SLfont_size.num*slid_SC, height/48,          slid_pw, slid_h)
                SLmax_FPS  .on = c_p_r(*MPos, q_width+SLmax_FPS  .num*slid_SC, height/48+menu_gap, slid_pw, slid_h)
                if c_p_r(*MPos, width/64, height/48, *Sexit.get_size()):
                    menu_page = 0
                if c_p_r(*MPos, q_width, height/48+menu_gap*2, *sw_size):
                    font_antialias = SWfontAA.switch
                if c_p_r(*MPos, q_width, height/48+menu_gap*3, *sw_size):
                    Sscale = transform.smoothscale if SWpicAA.switch else transform.scale
                    Stitle = Sscale(Srtitle, (int(width*0.96), int(width*0.13375)))
                    Sinfo = Sscale(Srinfo, (int(width*0.105), int(width*0.05625)))
                    Sexit = Sscale(Srexit, (int(width*0.04), int(width*0.04)))
                    sw_on_disabled = Sscale(rsw_on_disabled, (int(width*0.03), int(width*0.03)))
                    sw_on_over = Sscale(rsw_on_over, (int(width*0.03), int(width*0.03)))
                    sw_on = Sscale(rsw_on, (int(width*0.03), int(width*0.03)))
                    sw_off_disabled = Sscale(rsw_off_disabled, (int(width*0.03), int(width*0.03)))
                    sw_off_over = Sscale(rsw_off_over, (int(width*0.03), int(width*0.03)))
                    sw_off = Sscale(rsw_off, (int(width*0.03), int(width*0.03)))
                if c_p_r(*MPos, q_width, height/48+menu_gap*4, *sw_size):
                    Gvsync = SWvsync.switch
                if c_p_r(*MPos, q_width, height/48+menu_gap*5, *sw_size):
                    Gmobui = SWmobui.switch
                if c_p_r(*MPos, q_width, height/48+menu_gap*6, *sw_size):
                    mous = SWmouse.switch
                if c_p_r(*MPos, q_width, height/48+menu_gap*7, *sw_size):
                    dev = SWdev.switch
        for i in event.get(MOUSEBUTTONUP):
            SLfont_size.on = SLmax_FPS.on = False
        for b, a in enumerate(event.get(MULTIGESTURE)):
            x = a.x*width
            y = a.y*height
            win.blit(MAINFONT.render(f"{a.__dict__}", font_antialias, Ctext), (8, 8+30*b))
            draw.circle(win, (255, 191, 255), (x, y), 20)

        win.blits(((Sexit,              (width/64, height/48)),
                   (SLfont_size.draw(), (q_width, height/48)),
                   (SLmax_FPS  .draw(), (q_width, height/48+menu_gap)),
                   SWfontAA.draw((q_width, height/48+menu_gap*2)),
                   SWpicAA .draw((q_width, height/48+menu_gap*3)),
                   SWvsync .draw((q_width, height/48+menu_gap*4)),
                   SWmobui .draw((q_width, height/48+menu_gap*5)),
                   SWmouse .draw((q_width, height/48+menu_gap*6)),
                   SWdev   .draw((q_width, height/48+menu_gap*7)),
                   (MAINFONT.render("*: Применяется после перезапуска", font_antialias, Ctext), (8, height-font_height-8))))

    display.update()
    CLOCK.tick(max_FPS)
leave()
