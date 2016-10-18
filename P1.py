from random import shuffle

class P1(object):
    def __init__(self):
        super(P1, self).__init__()
        
        #name for your bot, make it colourful!
        self.name="Ai's Bot"
        
        #this id allows your code to interpret which places it has already moved to. 
        self.id=1
        
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
        @note:  for consistency, everything uses cartesian coordinates, x=horizontal indexes, y=vertical indexes, (0,0) is the top left, the returned board pos is in format (x,y).
                However, you will notice that to reference positions on the board, we use [y][x], thats because the board is a list of lists,
                so to reference each list use the y axis, to reference an item in a row (list), use the x axes
                python works by referencing the outer axis first, in this case the y axis, or row, then the x axis or col.
                
                to Summarize:
                - return value in the format (x,y)
                - refer to board[y][x] (or board[row][col])
                - x and y are cartesian coordinates
                - top left corner of the board is (0,0)
                
        """
        
        #default test logic, makes a list of available spots, shuffles them and returns the first one
        availableSpots=[]
        for y in range(3):
            for x in range(3):
                if board[y][x]==0:
                    availableSpots.append((x,y))
                    
        shuffle(availableSpots)
        return availableSpots[0]
    