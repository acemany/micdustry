from pygame import display,image,init,quit
from sys import argv

init()
display.set_mode((0,0))
a=image.load(argv[1])
a.set_colorkey((255,0,255))
image.save(a.convert_alpha(),f"{argv[1].split('.')[0]}.png")
quit()