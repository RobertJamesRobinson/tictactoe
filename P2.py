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

class Tree(object):
    def __init__(self):
        self.root=Board([[0,0,0],[0,0,0],[0,0,0]])
        self.root.children=self.root.findMoves(1)
        for board in self.root.children:
            board.getChildren(2)
    
    def countNodes(self):
        return self.root.returnNodeLength()
    
    def printNodes(self,depth):
        self.root.printChildren(depth)
        
    def findNode(self,board):
        return self.root.findBoard(board)

class Board(object):
    def __init__(self,board,parent=None):
        self.board=board
        self.children=None
        self.parent=parent
    
    def findBoard(self,board):
        if self.isTransform(board):
            return self
        else:
            if self.children:
                if len(self.children)>0:
                    for child in self.children:
                        result=child.findBoard(board)
                        if result:
                            return result
                        
    
    def printChildren(self,depth):
        if depth>0:
            if self.children:
                if len(self.children)>0:
                    print "---------depth=%i------------" % (depth)
                    for child in self.children:
                        print child
                    
                    for child in self.children:
                        child.printChildren(depth-1)
        
    def returnNodeLength(self):
        count=0
        if self.children:
            if len(self.children)>0:
                count=len(self.children)
                for child in self.children:
                    count+=child.returnNodeLength()
            else:
                return 1
        return count
        
    def getChildren(self,player):
        self.children=self.findMoves(player)
        #switch player
        if player==1:
            player=2
        else:
            player=1
            
        for board in self.children:
            if not board.winner():
                board.getChildren(player)
        
    def findEmptySquares(self):
        results=[]
        for y in range(3):
            for x in range(3):
                if self.board[y][x]==0:
                    results.append((x,y))
        return results
    
    def clone(self):
        result=[[0,0,0],[0,0,0],[0,0,0]]
        for y in range(3):
            for x in range(3):
                result[y][x]=self.board[y][x]
        return result
    
    def winner(self):
        board=self.board
        if board[0][0]==board[0][1] and board[0][1]==board[0][2] and (not board[0][0]==0):
            return board[0][0]
        if board[1][0]==board[1][1] and board[1][1]==board[1][2] and (not board[1][0]==0):
            return board[1][0]
        if board[2][0]==board[2][1] and board[2][1]==board[2][2] and (not board[2][0]==0):
            return board[2][0]
        if board[0][0]==board[1][0] and board[1][0]==board[2][0] and (not board[0][0]==0):
            return board[0][0]
        if board[0][1]==board[1][1] and board[1][1]==board[2][1] and (not board[0][1]==0):
            return board[0][1]
        if board[0][2]==board[1][2] and board[1][2]==board[2][2] and (not board[0][2]==0):
            return board[0][2]
        if board[0][0]==board[1][1] and board[1][1]==board[2][2] and (not board[0][0]==0):
            return board[0][0]
        if board[0][2]==board[1][1] and board[1][1]==board[2][0] and (not board[0][2]==0):
            return board[0][2]
        return False
        
    def findMoves(self,player):
        results=[]
        moves=self.findEmptySquares()
        for pos in moves:
            
            tmpBoard=Board(self.clone(),self)
            tmpBoard.board[pos[1]][pos[0]]=player
            
            if len(results)==0:
                results.append(tmpBoard)
            else:
                test=True
                for board in results:
                    if board.isTransform(tmpBoard):
                        test=False
                if test:
                    results.append(tmpBoard)
        return results
    
    def __str__(self):
        return "%s|%s|%s\n-----\n%s|%s|%s\n-----\n%s|%s|%s\n" % (str(self.board[0][0]),str(self.board[0][1]),str(self.board[0][2]),str(self.board[1][0]),str(self.board[1][1]),str(self.board[1][2]),str(self.board[2][0]),str(self.board[2][1]),str(self.board[2][2]))
    
    def isTransform(self,targ):
        targ=targ.board
        #define the checks
        checks={}
        checks['s']=self.board
        checks['x']=self.mirrorX(self.board)
        checks['y']=self.mirrorY(self.board)
        checks['r']=self.rotate(self.board)
        checks['rx']=self.mirrorX(self.rotate(self.board))
        checks['ry']=self.mirrorY(self.rotate(self.board))
        checks['rr']=self.rotate(self.rotate(self.board))
        checks['rrr']=self.rotate(self.rotate(self.rotate(self.board)))
        
        #run the checks
        for key in ['s','x','y','r','rx','ry','rr','rrr']:
            result=True
            for y in range(3):
                for x in range(3):
                    if not targ[y][x]==checks[key][y][x]:
                        result=False
            if result:
                return key
        return False
    
    def unRotate(self,board):
        result=[[0,0,0],[0,0,0],[0,0,0]]
        for y in range(len(board)):
            for x in range(len(board[0])):
                result[2-x][y]=board[y][x]
        return result    
    
    def rotate(self,board):
        result=[[0,0,0],[0,0,0],[0,0,0]]
        for y in range(len(board)):
            for x in range(len(board[0])):
                result[x][2-y]=board[y][x]
        return result
    
    def mirrorX(self,board):
        result=[[0,0,0],[0,0,0],[0,0,0]]
        for y in range(len(board)):
            for x in range(len(board[0])):
                result[y][2-x]=board[y][x]
        return result
        
    def mirrorY(self,board):
        result=[[0,0,0],[0,0,0],[0,0,0]]
        for y in range(len(board)):
            for x in range(len(board[0])):
                result[2-y][x]=board[y][x]
        return result