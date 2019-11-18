import pygame,sys
pygame.init()
screen=pygame.display.set_caption('hello world!')
screen=pygame.display.set_mode([640,480])
screen.fill([255,255,255])

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:sys.exit()
    pygame.draw.circle(screen,[255,0,0],[200,200],10,1)  #(surface color  center radius width )
    pygame.draw.line(screen,[255,0,0],[0,0],[200,200],1) #line(surface, color, start_pos, end_pos, width=1)
    pygame.display.flip()