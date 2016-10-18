from random import shuffle
import time

class P2(object):
    def __init__(self):
        super(P2, self).__init__()
        
        #name for your bot, make it colourful!
        self.name="Robbos Bot"
        
        #this id allows your code to interpret which places it has already moved to.
        #ie this constant is your moves on the board 
        self.id=2
        
        #rest of "loading" can be done here, no penalty for extended loading times
        # code
        # code
        
    #===========================================================================
    # move
    #===========================================================================
    def move(self,board):
        """
        @summary: take a board state, and returns a valid board position as the intended move
        @param board: a 2d list of numbers
        @return: x,y coordinates of this bots move, ie col,row; top left 0 referenced; eg 0,0 = top left, 2,1=far right, middle row
        
        """
        
        #default test logic, makes a list of available spots, shuffles them and returns the first one
        #time.sleep(1)
        killPos=self.spotWins(board)
        if killPos:
            return killPos
        else:
            availableSpots=[]
            mySpots=[]
            for x in range(3):
                for y in range(3):
                    if board[y][x]==0:
                        availableSpots.append((x,y))
                    if board[y][x]==self.id:
                        mySpots.append((x,y))
                        
            
            shuffle(availableSpots)
            count=0
            tmpPos=availableSpots[count]
            tmpSurrounds=self.surrounds(tmpPos)
            for val in tmpSurrounds:
                if board[val[1]][val[0]] == self.id:
                    return tmpPos
            return availableSpots[0]
            
            
    def spotWins(self,board):
        result=False
        if board[1][1]==self.id:
            if board[0][0]==self.id and board[2][2]==0:
                result=(2,2)
            if board[1][0]==self.id and board[1][2]==0:
                result=(2,1)
            if board[2][0]==self.id and board[0][2]==0:
                result=(2,0)
            if board[0][1]==self.id and board[2][1]==0:
                result=(1,2)
            if board[0][2]==self.id and board[2][0]==0:
                result=(0,2)
            if board[1][2]==self.id and board[1][0]==0:
                result=(0,1)
            if board[2][2]==self.id and board[0][0]==0:
                result=(0,0)
            if board[2][1]==self.id and board[0][1]==0:
                result=(1,0)
        return result
            
    def sameBoard(self,b1,b2):
        pass
    
    def identicalBoard(self,b1,b2):
        for y in range(len(b1)):
            for x in range(len(b1[0])):
                if not b1[y][x]==b2[y][x]:
                    return False
        return True
    
    def rotateBoard(self,b1):
        result=[[0,0,0],[0,0,0],[0,0,0]]
        for y in range(len(b1)):
            for x in range(len(b1[0])):
                result[x][2-y]=b1[y][x]
        return result
        
    def surrounds(self,pos):
        results=[]
        xVals=[]
        yVals=[]
        if pos[0]==0:xVals=[1]
        if pos[0]==1:xVals=[0,2]
        if pos[0]==2:xVals=[1]
        if pos[1]==0:yVals=[1]
        if pos[1]==1:yVals=[0,2]
        if pos[1]==2:yVals=[1]
        for x in xVals:
            for y in yVals:
                results.append((x,y))
        return results