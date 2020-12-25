# raw code to display watermelon board
# future plans will have tokens moving around

import pygame	# the main workhorse
import os		# i KNOW I'll need to detect OS and handle paths, etc
import sys		# for sys.exit
import math 	# for square roots on hex, pi on circles

# allows us to use the == QUIT later instead of pygame.locals.QUIT
from pygame.locals import * 

# fixed colors not in pulse
WH = (255,255,255)	# white
BL = (0,0,0)		# black
GY = (128,128,128)	# grey
RE = (255,0,0)		# red

# this can be adjusted if you like
scale = 40  # 30-80 is probably best scale range

legs = 9			#
leg1 = (legs/6);	# 1.5
leg2 = (leg1) * 2; 	#
leg3 = (leg1) * 3;	#
leg4 = (leg1) * 4;	#
ctr  = leg4;	

# relative game board size
W  = int((3+legs)*scale)
H  = int((3+legs)*scale)

lw = 3            # line width of polygons

# circles just have to be manually made :(
circles = {
	# x, y, size, fill
	10 : [ctr,ctr,leg3,0], # the big Juan
	11 : [ctr,ctr,leg1,0],  # the little Juan
 
	#12 : [ctr,ctr-leg3,leg1,0], # N but can't do full circles, do arcs instead
	#13 : [ctr+leg3,ctr,leg1,0], # E, do arcs instead
	#14 : [ctr,ctr+leg3,leg1,0], # S, do arcs instead
	#15 : [ctr-leg3,ctr,leg1,0], # W, do arcs instead
}

# just circles really, but broken up for logic
# fixme: remove unused data
# fixme: document why I used .167 and .017
# fixme: verify if all of these are required, why comment out 12 and looks same?
dots = {
	#12 : [ctr-leg3,ctr,.1,1], # y-axis
	13 : [leg2,ctr,.1,1], # y-axis cener
	14 : [ctr-leg1,ctr,.1,1], # y-axis
 
	15 : [ctr+leg1,ctr,.1,1], # y-axis
	16 : [ctr+leg2,ctr,.1,1], # y-axis center
	17 : [ctr+leg3,ctr,.1,1], # y-axis
 
	18 : [ctr,ctr,.1,1], #  center
 
	19 : [ctr,ctr-leg3,.1,1], # x-axis
	20 : [ctr,ctr-leg2,.1,1], # x-axis center
	21 : [ctr,ctr-leg1,.1,1], # x-axis
 
	22 : [ctr,ctr+leg1,.1,1], # x-axis
	23 : [ctr,ctr+leg2,.1,1], # x-axis center
	24 : [ctr,ctr+leg3,.1,1], # x-axis
	
	25 : [ctr-leg3+leg1*.167,ctr+leg1-leg1*.017,.1,1], # arc dots, WN
	26 : [ctr-leg3+leg1*.167,ctr-leg1+leg1*.017,.1,1], # arc dots, WS
	27 : [ctr+leg3-leg1*.167,ctr+leg1-leg1*.017,.1,1], # arc dots, EN
	28 : [ctr+leg3-leg1*.167,ctr-leg1+leg1*.017,.1,1], # arc dots, ES 
 
	29 : [ctr-leg1+leg1*.017,ctr-leg3+leg1*.167,.1,1], # arc dots, NW
	30 : [ctr+leg1-leg1*.017,ctr-leg3+leg1*.167,.1,1], # arc dots, NE
	31 : [ctr-leg1+leg1*.017,ctr+leg3-leg1*.167,.1,1], # arc dots, SW
	32 : [ctr+leg1-leg1*.017,ctr+leg3-leg1*.167,.1,1], # arc dots, SE
}

#fixme: we brute force guessed our arc points, bleh
arcs = {
	# x-center,y-center,deg1,deg2
	10 : [ctr,leg1,193,349], # north arc
	11 : [ctr+leg3,ctr,102,260], # east arc
	12 : [ctr,ctr+leg3,12,169], # south arc
	13 : [leg1,ctr,282,78] # west arc
}

# finally the lines dict
lines = {
	# x1  y1   x2   y2
	10 : [ctr,ctr-leg3,ctr,ctr+leg3],	# N to S
	11 : [ctr-leg3,ctr,ctr+leg3,ctr]	# E to W
}


def main():
	# can't run pygame without init, just do it
	pygame.init()

	# clock required to limit fps
	FPS = pygame.time.Clock()

	# one of (possibly many) surfaces to draw on
	SURF = pygame.display.set_mode((W,H))

	# the title bar
	pygame.display.set_caption("Watermelon Board")

	# default colors start at black
	r1,g1,b1 = (0,0,0)
	r2,g2,b2 = (0,0,0)

	# used to pulse color
	flip_r1,flip_g1,flip_b1 = (1,1,1)
	flip_r2,flip_g2,flip_b2 = (1,1,1)

	#Game loop begins
	while True:
		# current color of pulse, r,g,b set at bottom of while 
		r1,flip_r1 = get_pulse(flip_r1,r1,1) # mix and match your pulse, red
		b2,flip_b2 = get_pulse(flip_b2,b2,5) # mix and match your pulse, red
		pulse1 = (r1,g1,b1)
		pulse2 = (r2,g2,b2)

		# fill our surface with white
		SURF.fill(GY)

		# event section
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:

				# update where we just clicked
				(x,y) = pygame.mouse.get_pos()

			if event.type == QUIT:
				# pygame has a buggy quit, do both
				pygame.quit()
				sys.exit()

		draw_board(SURF,pulse1,pulse2,lw)
		# update the screen object itself
		pygame.display.update()	# update entire screen if no surface passed

		# tick the fps clock
		FPS.tick(60)

'''
moved out to clean up the main()
can comment on/off to troubleshoot
'''
def draw_board(surf,pulse1,pulse2,lw):

	for xy in circles:
		pygame.draw.circle(surf, pulse1, (
				int(circles[xy][0] * scale), 
				int(circles[xy][1] * scale)
				), 
			int(circles[xy][2] * scale),
			lw
		)

	for xy in arcs:
		drawCircleArc(surf, pulse1, (
			arcs[xy][0],
			arcs[xy][1]),
			leg1,
			arcs[xy][2],
			arcs[xy][3],
			lw
		)

	for xy in lines:
		pass
		pygame.draw.line(surf, pulse1,
			(lines[xy][0] * scale,lines[xy][1] * scale),
			(lines[xy][2] * scale,lines[xy][3] * scale),
			lw
		)

	# placing dots last so they look like they are "on top"
	for xy in dots:
		pygame.draw.circle(surf, pulse2, (
				int(dots[xy][0] * scale), 
				int(dots[xy][1] * scale)
				), 
			lw*2, 
			0
		)

'''
didn't research fully but looks like draw.arc wants radians not deg
'''
def degreesToRadians(deg):
    return deg/180.0 * math.pi

'''
cleaned up the draw board, 
'''
def drawCircleArc(screen,color,center,radius,startDeg,endDeg,thickness):
    (x,y) = center
    x = x * scale
    y = y * scale
    radius = radius * scale
    rect = (x-radius,y-radius,radius*2,radius*2)
    startRad = degreesToRadians(startDeg)
    endRad = degreesToRadians(endDeg)
    pygame.draw.arc(screen,color,rect,startRad,endRad,thickness)

'''
just pulse 255 to 0 back to 255 repeat 
set boundaries so we don't get invalid rgb value
input: state of the flip, and current color code
return: updated flip and color code
'''
def get_pulse(flipped,c,step):

	if flipped:
		if c < 255: c += step
		else:
			c = 255
			flipped = 0
	else:
		if c > step: c -= step
		else:
			c = 0
			flipped = 1

	if c > 255: c = 255
	if c < 0: c = 0

	return (c,flipped)



if __name__ == '__main__':
	# capture ctrl c
	try:
		main()
	except KeyboardInterrupt:
		# pygame has a buggy quit, do both
		pygame.quit()
		sys.exit()



