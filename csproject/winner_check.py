import numpy as nmp
from graphics import *

mvm_allowed = True

win = GraphWin("test", 400, 400)
win.setCoords(0.0,0.0,8.0,8.0)


while mvm_allowed:
    for i in range(1):
        point = win.getMouse()
        mx, my = nmp.floor(point.getX()), nmp.floor(point.getY())
        if mx == 7.0 and my == 7.0:
            mvm_allowed = False
    print(mx, my)


    #if self.board[mx][my] != EMPTY:
    ###WHEN THE MOVE IS DONE mvm_allowed switches to 1 and changes apply,
    ###After that, the movement allowed switches back to 0
    ###Opponent move starts
