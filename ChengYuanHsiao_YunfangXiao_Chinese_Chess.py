import pygame
import sys
import random
from pygame.locals import *
import time
pygame.init()
#set up window
DISPLAYSURF = pygame.display.set_mode((800,400))
pygame.display.set_caption('cchess')
# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)
#draw board
DISPLAYSURF.fill(WHITE)
for i in range(5):
	pygame.draw.line(DISPLAYSURF, BLACK, [0, 0+i*100], [800, 0+i*100], 1)
for i in range(9):
	pygame.draw.line(DISPLAYSURF, BLACK, [0+i*100, 0], [0+i*100, 400], 1)
#draw grey pieces faced down
for i in range(8):
	pygame.draw.circle(DISPLAYSURF, GREY, [50+i*100, 50], 35, 0)
	pygame.draw.circle(DISPLAYSURF, GREY, [50+i*100, 150], 35, 0)
	pygame.draw.circle(DISPLAYSURF, GREY, [50+i*100, 250], 35, 0)
	pygame.draw.circle(DISPLAYSURF, GREY, [50+i*100, 350], 35, 0)
pygame.display.update()
#shuffle positions
#for each square value (ex. '1R1'), the three digit string represent information about the piece currently in square
#first item: 1 = faced down(grey), 0 = faced up
#second item: R = red, B = black
#third item: hierchy ranging from 1 to 7, 7 is the most powerful hierchy.
ROW1 = ['1R1','1R1','1B1','1B2','1B3','1B4','1B5','1B6']
random.shuffle(ROW1)
ROW2 = ['1R1','1B1','1B1','1B2','1B3','1B4','1B5','1B6']
random.shuffle(ROW2)
ROW3 = ['1R1','1B1','1R2','1R3','1R4','1R5','1R6','1R7']
random.shuffle(ROW3)
ROW4 = ['1R1','1B1','1R2','1R3','1R4','1R5','1R6','1B7']
random.shuffle(ROW4)
POSITION = [ROW1, ROW2, ROW3, ROW4]

#helpers
def switchplayer(): #change value of CURRENTP (CURRENTP represents current player)
	global CURRENTP
	if CURRENTP == 'R':
		CURRENTP = 'B'
	elif CURRENTP == 'B':
		CURRENTP = 'R'

def find_centercoord (pos): #ex.pos: (50,150), return center coordinates of square
	return ((pos[0]//100)*100+50, (pos[1]//100)*100+50)

def find_square(pos): #output is (row,column) of the inputed coordinates
	return ((find_centercoord(pos)[1]+50)//100-1, (find_centercoord(pos)[0]+50)//100-1)

def squarevalue(pos): #return value '1R3' for example
	global POSITION
	return POSITION[find_square(pos)[0]][find_square(pos)[1]]

def piecehidden(pos): #boolean, returns whether the piece is hidden
	global POSITION
	if POSITION[find_square(pos)[0]][find_square(pos)[1]][0] == '1':
		return True
	else:
		return False

def adjacent(mouse1, mouse2): #boolean, return if the second piece is adjacent to the first piece
	if len(mouse1) == 2 and len(mouse2) == 2:
		x = find_square(mouse1)
		y = find_square(mouse2)
		if x[0] == y[0] and x[1] == y[1]+1:
			return True
		elif x[0] == y[0] and x[1] == y[1]-1:
			return True
		elif x[1] == y[1] and x[0] == y[0]-1:
			return True
		elif x[1] == y[1] and x[0] == y[0]+1:
			return True
		else:
			return False
	else:
		return False

def neighbors(x, y): #input(row,column) output list of all adjacent squares
	NEIGHBOR = []
	if x == 0 and y == 0:
		return [[1,0], [0,1]]
	if x == 0 and y == 7:
		return [[1,7], [0,6]]
	if x == 3 and y == 7:
		return [[3,6], [2,7]]
	if x == 3 and y == 0:
		return [[3,1], [2,0]]
	for x2 in range(x-1, x+2):
		for y2 in range(y-1, y+2):
			if (-1 < x <= 3 and -1 < y <= 7 and (x != x2 or y != y2)):
				if ((not (x != x2 and y != y2)) and (0 <= x2 <= 3) and (0 <= y2 <= 7)):
					NEIGHBOR += [[x2, y2]]
	return NEIGHBOR

def movable(coord): #helper for legal_click1
	global POSITION
	MOVABLE = False
	for item in neighbors(find_square(coord)[0], find_square(coord)[1]):
		if POSITION[item[0]][item[1]][2] <= POSITION[find_square(coord)[0]][find_square(coord)[1]][2]:
			if POSITION[item[0]][item[1]][1] == Opponent(CURRENTP) and POSITION[item[0]][item[1]][0] == '0':
				MOVABLE = True
		if POSITION[item[0]][item[1]] == '000':
			MOVABLE = True
	return MOVABLE

def legal_click1(coord): #boolean, if first click is legal(eg: current player's piece is clicked or hidden piece is clicked)
	global POSITION
	if len(coord) == 2:
		if POSITION[find_square(coord)[0]][find_square(coord)[1]][0] == '1': #if piece is hidden
			return True
		if POSITION[find_square(coord)[0]][find_square(coord)[1]][0] == '0' and POSITION[find_square(coord)[0]][find_square(coord)[1]][1] == CURRENTP: #revealed and current player
			return movable(coord)
		else:
			return False
	else:
		return False

def legal_click2(mouse1, mouse2): #boolean, if second click is legal (different color piece)
	global POSITION
	if len(mouse1) == 2 and len(mouse2) == 2:
		if POSITION[find_square(mouse2)[0]][find_square(mouse2)[1]] == '000': #if square empty
			return True
		if POSITION[find_square(mouse2)[0]][find_square(mouse2)[1]][1] != CURRENTP: #if mouse2 is opponent's piece
			if POSITION[find_square(mouse2)[0]][find_square(mouse2)[1]][2] <= POSITION[find_square(mouse1)[0]][find_square(mouse1)[1]][2]: #hierchy requirement
				return True
			else:
				return False
	else:
		return False

def color(pos): #color of the piece for graphics
	global RED
	global BLACK
	global POSITION
	if POSITION[find_square(pos)[0]][find_square(pos)[1]][1] == "R":
		return RED
	else:
		return BLACK

def thickness(pos): #thickness of circle for graphics, thicker colored ring means higher hierarchy
	global POSITION
	return int(POSITION[find_square(pos)[0]][find_square(pos)[1]][2]) * 4

def Opponent(current): #returns opponent's color
	if current == 'R':
		return 'B'
	if current == 'B':
		return 'R'

def endgame(position): #boolean, return whether the game has ended
	remain = []
	for row in range(0,4):
		for item in range(0,8):
			if position[row][item] != '000':
				remain.append(position[row][item])
	length = len(remain)
	kept_r = len([x for x in remain if x[1] == 'R'])
	kept_b = len([x for x in remain if x[1] == 'B'])
	if length == kept_b or length == kept_r:
		return True
	else:
		return False

#main
CURRENTP = "-"
MOUSE1 = [] #coordinates of first click
MOUSE2 = [] #coordinates of second click
FINISHMOVE = False
SCORER = 16 #scoreboard
SCOREB = 16
#first move
while not legal_click1(MOUSE1): #wait till legal click
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			MOUSE1 = pygame.mouse.get_pos()
			print ("mouse1", MOUSE1)
pygame.draw.circle(DISPLAYSURF, WHITE, find_centercoord(MOUSE1), 35, 0)
pygame.draw.circle(DISPLAYSURF, color(MOUSE1), find_centercoord(MOUSE1), 35, thickness(MOUSE1))
pygame.display.update()
CURRENTP = squarevalue(MOUSE1)[1]
#change position
POSITION[find_square(MOUSE1)[0]][find_square(MOUSE1)[1]]= '0' + squarevalue(MOUSE1)[1] + squarevalue(MOUSE1)[2]
print ("player 1 is", CURRENTP, 'next player')
print('Score for black is', SCOREB)
print('Score for red is', SCORER)
print (POSITION)
switchplayer()
MOUSE1 = []
MOUSE2 = []
#main game control
while not endgame(POSITION):
	#repeat till move is finished and valid
	while not FINISHMOVE:
		FINISHMOVE = False
		#make first click
		while not legal_click1(MOUSE1):
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					MOUSE1 = pygame.mouse.get_pos()
					print ("mouse1", MOUSE1)
		#if clicked piece is hidden then move is finished
		if piecehidden(MOUSE1):
			pygame.draw.circle(DISPLAYSURF, WHITE, find_centercoord(MOUSE1), 35, 0)
			pygame.draw.circle(DISPLAYSURF, color(MOUSE1), find_centercoord(MOUSE1), 35, thickness(MOUSE1))#flipover pieces
			pygame.display.update()
			#change position
			POSITION[find_square(MOUSE1)[0]][find_square(MOUSE1)[1]]= '0' + squarevalue(MOUSE1)[1] + squarevalue(MOUSE1)[2]
			switchplayer()
			print (POSITION)
			MOUSE1 = []
			MOUSE2 = []
			print('next player is', CURRENTP)
			print('Score for black is', SCOREB)
			print('Score for red is', SCORER)
			FINISHMOVE = True
		#if first click is a revealed current player piece
		elif squarevalue(MOUSE1)[1] == CURRENTP and squarevalue(MOUSE1)[0] == '0':
			# then make second click
			while not (legal_click2(MOUSE1, MOUSE2) and adjacent(MOUSE1, MOUSE2)):
				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN:
						MOUSE2 = pygame.mouse.get_pos()
						print ("mouse2", MOUSE2)
			# if 2nd click is opponent player's piece or 2nd click is empty
			if (squarevalue(MOUSE2)[1] == Opponent(CURRENTP) and squarevalue(MOUSE2)[0] == '0') or squarevalue(MOUSE2) == '000':
				pygame.draw.circle(DISPLAYSURF, WHITE, find_centercoord(MOUSE1), 35, 0)
				pygame.display.update()
				pygame.draw.circle(DISPLAYSURF, color(MOUSE1), find_centercoord(MOUSE2), 35, thickness(MOUSE1))
				pygame.display.update()
				#if made a capture then change scoreboard
				if not squarevalue(MOUSE2) == '000':
					if CURRENTP == 'R':
						SCOREB -= 1
					else:
						SCORER -= 1
				#change position accordingly
				POSITION[find_square(MOUSE2)[0]][find_square(MOUSE2)[1]] = '0' + CURRENTP + squarevalue(MOUSE1)[2]
				POSITION[find_square(MOUSE1)[0]][find_square(MOUSE1)[1]] = '000'
				print (POSITION)
				switchplayer()
				MOUSE1 = []
				MOUSE2 = []
				print('next player is', CURRENTP)
				print('Score for black is', SCOREB)
				print('Score for red is', SCORER)
				FINISHMOVE = True
	FINISHMOVE = False #switchplayer and start next move
print("game over")
if SCOREB == 0:
	print ('red wins')
else:
	print ('black wins')
time.sleep(3)
pygame.quit()
sys.exit()
