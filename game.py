from P1 import *
from P2 import *
import time,math
import pygame
from random import randint

class GameManager(object):
    #===========================================================================
    # __init__
    #===========================================================================
    def __init__(self):
        super(GameManager, self).__init__()
        self.numberOfGames=1000000
        self.startWarnings=10       #seconds
        self.maxGameTime=600        #seconds
        self.gameFailThreshold=10   #seconds
        
    #===========================================================================
    # run
    #===========================================================================
    def run(self):
        """
        @summary: The main function of this app, the driver for the whole game
        
        """
        #setup our stat counters
        stat1={}
        stat2={}
        stats=[stat1,stat2]
        
        #load bot 1
        ticks=time.time()
        p1=P1()
        elapsed=time.time()-ticks
        stats[0]['Bot Loading Time']=elapsed
        stats[0]['Number of Wins']=0
        stats[0]['Game Fails']=0
        stats[0]['Number of Draws']=0
        stats[0]['Player']=p1
        stats[0]['Average Move Time']=None
        stats[0]['Best Move Time']=None
        stats[0]['Worst Move Time']=None
        
        #load bot 2
        ticks=time.time()
        p2=P2()
        elapsed=time.time()-ticks
        stats[1]['Bot Loading Time']=elapsed
        stats[1]['Number of Wins']=0
        stats[1]['Game Fails']=0
        stats[1]['Number of Draws']=0
        stats[1]['Player']=p2
        stats[1]['Average Move Time']=None
        stats[1]['Best Move Time']=None
        stats[1]['Worst Move Time']=None
        
        #main runs start here
        thisRound=1
        timeToRunInWarnings=0
        
        totalGameTime=time.time()
        for i in range(self.numberOfGames):
            #check that the whole process isn't taking too long
            if time.time()-totalGameTime>self.startWarnings:
                if timeToRunInWarnings==0:
                    timeToRunInWarnings=i
                if i%timeToRunInWarnings==0:
                    secs=int((self.numberOfGames-i)/float((timeToRunInWarnings/float(self.startWarnings))))
                    hours,minutes,seconds=self.convertTime(secs)
                    print "Taking a while.... %i games have been calculated so far" % (i)
                    if secs>self.maxGameTime:
                        ch,cm,cs=self.convertTime(self.maxGameTime-(time.time()-totalGameTime))
                        print "At this rate it would take a further %ih:%im:%is to finish. We will be cut off in %ih:%im:%is\n" % (hours,minutes,seconds,ch,cm,cs)
                    else:
                        print "At this rate it will take a further %ih:%im:%is to finish\n" % (hours,minutes,seconds)
                    
            if time.time()-totalGameTime>self.maxGameTime:
                print "Too long, game %i is the last to be calculated\n" % (i)
                break
            
            #setup the board and player markers
            p1Map=thisRound
            board=[[0,0,0],[0,0,0],[0,0,0]]
            
            #switch the round for the next game
            thisRound=self.switchPlayer(thisRound)
               
            #setup this games variables
            running=True
            winner=0
            failed=False
            
            #randomly place the first piece
            board[randint(0,2)][randint(0,2)]=p1Map
            
            #switch player
            p1Map=self.switchPlayer(p1Map)
                
            while(running):
                #if there are no more moves, crash out
                if self.boardFull(board):
                    running=False
                else:
                    #time the players move
                    ticks=time.time()
                    move=stats[p1Map-1]['Player'].move(board)
                    elapsed=time.time()-ticks
                    
                    #save the players timings
                    if not stats[p1Map-1]['Average Move Time']:
                        stats[p1Map-1]['Average Move Time']=elapsed
                    else:
                        stats[p1Map-1]['Average Move Time']=(stats[p1Map-1]['Average Move Time']+elapsed)/float(2)
                    
                    #Best move Time
                    if not stats[p1Map-1]['Best Move Time']:
                        stats[p1Map-1]['Best Move Time']=elapsed
                    elif stats[p1Map-1]['Best Move Time']>elapsed:
                        stats[p1Map-1]['Best Move Time']=elapsed
                    
                    #Worst move Time
                    if not stats[p1Map-1]['Worst Move Time']:
                        stats[p1Map-1]['Worst Move Time']=elapsed
                    elif stats[p1Map-1]['Worst Move Time']<elapsed:
                        stats[p1Map-1]['Worst Move Time']=elapsed
                    
                    #see if the player took too long
                    if elapsed>self.gameFailThreshold:
                        stats[p1Map-1]['Game Fails']+=1
                        stats[self.switchPlayer(p1Map)-1]['Number of Wins']+=1
                        running=False
                        failed=True
                    
                    #check the move and if its valid, enter it into the board, otherwise chalk up a fail to the player
                    if self.validateMove(move, board):
                        board[move[1]][move[0]]=p1Map
                    else:
                        #game over player forfeits
                        stats[p1Map-1]['Game Fails']+=1
                        running=False
                    
                    #check for winner
                    winner=self.findWinner(board)
                    if not winner==0:
                        #someone won!
                        running=False
                   
                    #switch player for next move
                    p1Map=self.switchPlayer(p1Map)
            
            #game over, add up stats                
            if not winner==0:
                stats[winner-1]['Number of Wins']+=1
            elif failed:
                failed=False
            else:
                for stat in stats:
                    stat['Number of Draws']+=1
            
        #print the game results
        self.printStatsToConsole(stats)
    
    def convertTime(self,secs):
        hrs=secs/float(3600)
        hours=math.floor(hrs)
        mins=(hrs-hours)*60
        minutes=math.floor(mins)
        secs=(mins-minutes)*60
        seconds=math.floor(secs)
        return hours,minutes,seconds
     
    def printStatsToConsole(self,stats):
        print "Game Results:\n"
        for i in range(1,len(stats)+1):
            
            print "Player: %s" % (stats[i-1]['Player'].name)
            for key in stats[i-1].keys():
                if not key=="Player":
                    if key=="Average Move Time" or key=="Bot Loading Time" or key=="Worst Move Time" or key=="Best Move Time":
                        print "%s: %0.10f" % (key,stats[i-1][key])
                    else:
                        print "%s: %s" % (key,str(stats[i-1][key]))
            print
        
        #organise a list of winners
        newList = sorted(stats, key=lambda k: k['Number of Wins'])
        newList.reverse()
        
        #print the stats
        if newList[0]['Number of Wins']==newList[1]['Number of Wins']:
            print "ITS A DRAW!!!!"
        else:
            count=1
            for item in newList:
                print "%s finished in place %s" % (item['Player'].name, str(count))
                count+=1
            print "\n%s IS THE WINNER!!!" % (newList[0]['Player'].name)
       
       
    def switchPlayer(self,player):
        if player==1:
            return 2
        else:
            return 1
    def validateMove(self,pos,board):
        if board[pos[1]][pos[0]]==0:
            return True
        else:
            return False
        
    def boardFull(self,board):
        for x in range(3):
            for y in range(3):
                if board[y][x]==0:
                    return False
        return True
    
    def findWinner(self,board):
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
    
    def printBoard(self,board):
        print "%s|%s|%s" % (str(board[0][0]),str(board[0][1]),str(board[0][2]))
        print "-----"
        print "%s|%s|%s" % (str(board[1][0]),str(board[1][1]),str(board[1][2]))
        print "-----"
        print "%s|%s|%s" % (str(board[2][0]),str(board[2][1]),str(board[2][2]))
    
       
class GFXManager(object):
    #===========================================================================
    # __init__
    #===========================================================================
    def __init__(self):
        super(GFXManager, self).__init__()
        self.numberOfGames=1000000
        self.startWarnings=10       #seconds
        self.maxGameTime=600        #seconds
        self.gameFailThreshold=10   #seconds
        pygame.init()
        self.screen=pygame.display.set_mode((800,800))
    
    
    #===========================================================================
    # run
    #===========================================================================
    def run(self):
        menu=0
        running=True
        screen=self.screen
        hvbOpponent=None
        opponents={}
        p1=P1()
        p2=P2()
        opponents[p1.name]=p1
        opponents[p2.name]=p2
        scores=[0,0]
        # QUIT           none
        # ACTIVEEVENT      gain, state
        # KEYDOWN           unicode, key, mod
        # KEYUP           key, mod
        # MOUSEMOTION      pos, rel, buttons
        # MOUSEBUTTONUP    pos, button
        # MOUSEBUTTONDOWN  pos, button
        # JOYAXISMOTION    joy, axis, value
        # JOYBALLMOTION    joy, ball, rel
        # JOYHATMOTION     joy, hat, value
        # JOYBUTTONUP      joy, button
        # JOYBUTTONDOWN    joy, button
        # VIDEORESIZE      size, w, h
        # VIDEOEXPOSE      none
        # USEREVENT        code
        
        while running:
            menuActive=True
            if menu==0:
                #draw the main menu
                screen.fill((0,0,0))
                rects={}
                rects['heading']=pygame.Rect(120,120,560,140)
                rects['hvh']=pygame.Rect(120,280,560,120)
                rects['hvb']=pygame.Rect(120,420,560,120)
                rects['bvb']=pygame.Rect(120,560,560,120)
                rects['quit']=pygame.Rect(500,720,280,60)
                
                screen.fill((0,0,255),(100,100,600,600))
                screen.fill((127,127,127),rects['heading'])
                screen.fill((127,127,127),rects['hvh'])
                screen.fill((127,127,127),rects['hvb'])
                screen.fill((127,127,127),rects['bvb'])
                screen.fill((0,0,255),(rects['quit'][0]-3,rects['quit'][1]-3,rects['quit'][2]+6,rects['quit'][3]+6))
                screen.fill((127,127,127),rects['quit'])
                
                self.write(rects['quit'],'quit',(200,200,200),75)
                self.write(rects['heading'],"Game Mode",(255,255,0),100)
                self.write(rects['hvh'],"Human Vs Human",(255,0,0),65)
                self.write(rects['hvb'],"Human Vs Bot",(255,0,0),65)
                self.write(rects['bvb'],"Bot Vs Bot",(255,0,0),65)
                
                pygame.display.flip()
                
                selected=False
                while menuActive:
                    #assess mouse clicks n shit
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            running=False
                            menu=0
                            menuActive=False
                            
                        #capture mouse clicks
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            for key in rects.keys():
                                if rects[key].collidepoint(event.pos):
                                    selected=key
                        
                        #capture key strokes
                        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                            running=False
                            menuActive=False
                            menu=0        
                    
                    #logic for menu from the button clicks    
                    if selected:
                        if not selected=="heading":
                            menuActive=False
                            if selected=="hvh":
                                menu=1
                            if selected=="hvb":
                                menu=2
                            if selected=="bvb":
                                menu=4
                            if selected=="quit":
                                menu=0
                                running=False
                                menuActive=False
                    
            menuActive=True
            if menu==1:
                scores=[0,0]
                #draw the human vs human menu and play accordingly
                #draw the main screen
                board=[[0,0,0],[0,0,0],[0,0,0]]
                screen.fill((0,0,0))
                rects={}
                rects['1']=pygame.Rect(103,501,196,196)
                rects['2']=pygame.Rect(302,501,196,196)
                rects['3']=pygame.Rect(501,501,196,196)
                rects['4']=pygame.Rect(103,302,196,196)
                rects['5']=pygame.Rect(302,302,196,196)
                rects['6']=pygame.Rect(501,302,196,196)
                rects['7']=pygame.Rect(103,103,196,196)
                rects['8']=pygame.Rect(302,103,196,196)
                rects['9']=pygame.Rect(501,103,196,196)
                rects['quit']=pygame.Rect(500,720,280,60)
                
                screen.fill((0,0,255),(100,100,600,600))
                for key in rects.keys():
                    if key=="quit":
                        screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
                        screen.fill((127,127,127),rects[key])
                        self.write(rects[key],key,(200,200,200),75)
                    else:
                        screen.fill((127,127,127),rects[key])
                        self.write(rects[key],key,(200,200,200),100)
                        
                #draw the player names
                self.drawPlayers(0)
                self.drawScores(scores)
                
                pygame.display.flip()
                player=1
                self.drawPlayers(player)
                winner=0
                selected=False
                while menuActive:
                    #assess mouse clicks n shit
                    for event in pygame.event.get():
                        
                        #quit events
                        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                            running=False
                            menu=0
                            menuActive=False
                        
                        #capture mouse clicks
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            for key in rects.keys():
                                if rects[key].collidepoint(event.pos):
                                    selected=key
                        
                        #capture key strokes
                        if event.type==pygame.KEYDOWN:
                            validKeys='123456789'
                            if event.unicode in validKeys:
                                selected=event.unicode
                            
                    #logic for menu from the button clicks    
                    if selected:
                        if selected=="quit":
                            menuActive=False
                            menu=0
                        else:
                            pos=self.convertIndexToPos(int(selected))
                            #print pos,selected,rects[selected]
                            if self.validateMove(pos, board):
                                board[pos[1]][pos[0]]=player
                                self.drawMove(selected,player,rects)
                                pygame.display.update(rects[selected])
                                if self.findWinner(board):
                                    winner=player
                                else:
                                    player=self.switchPlayer(player)
                                    if not self.boardFull(board):
                                        self.drawPlayers(player)
                            selected=False
                
                    if (not winner==0) or self.boardFull(board):
                        if not winner==0:
                            self.drawPlayers(winner+2)
                            scores[winner-1]+=1
                            self.drawScores(scores)
                        else:
                            #draw
                            self.drawPlayers(5)
                            winner=1
                            
                        #reset game
                        player=winner
                        screen.fill((0,0,255),(100,100,600,600))
                        for key in rects.keys():
                            if key=="quit":
                                screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
                                screen.fill((127,127,127),rects[key])
                                self.write(rects[key],key,(200,200,200),75)
                            else:
                                screen.fill((127,127,127),rects[key])
                                self.write(rects[key],key,(200,200,200),100)
                        pygame.display.flip()
                        winner=0
                        board=[[0,0,0],[0,0,0],[0,0,0]]
                        self.drawPlayers(player)
                        selected=False
                        
                    
            menuActive=True
            if menu==2:
                #draw the choose bot for human to play against menu
                #define the rects
                rects={}
                cursor=420
                for key in opponents.keys():
                    rects[key]=pygame.Rect(120,cursor,560,120)
                    cursor+=140
                
                #draw the elements
                screen.fill((0,0,0))
                self.write((100,100,600,150), "Choose Your", (255,255,255), 80)
                self.write((100,250,600,150), "Opponent", (255,255,255), 80)
                screen.fill((0,0,255),(100,400,600,300))
                for key in rects.keys():
                    screen.fill((120,120,120),rects[key])
                    self.write(rects[key], key, (255,255,255), 45)
                pygame.display.flip()
                selected=False
                #process user input
                while menuActive:
                    for event in pygame.event.get():
                        
                        #quit events
                        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                            running=False
                            menu=0
                            menuActive=False
                        
                        #capture mouse clicks
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            for key in rects.keys():
                                if rects[key].collidepoint(event.pos):
                                    selected=key
                           
                    #logic for menu from the button clicks    
                    if selected:
                        hvbOpponent=opponents[selected]
                        menuActive=False
                        menu=3
                        
            menuActive=True
            if menu==3:
                scores=[0,0]
                #draw the bot vs human play
                #draw the main screen
                board=[[0,0,0],[0,0,0],[0,0,0]]
                screen.fill((0,0,0))
                rects={}
                rects['1']=pygame.Rect(103,501,196,196)
                rects['2']=pygame.Rect(302,501,196,196)
                rects['3']=pygame.Rect(501,501,196,196)
                rects['4']=pygame.Rect(103,302,196,196)
                rects['5']=pygame.Rect(302,302,196,196)
                rects['6']=pygame.Rect(501,302,196,196)
                rects['7']=pygame.Rect(103,103,196,196)
                rects['8']=pygame.Rect(302,103,196,196)
                rects['9']=pygame.Rect(501,103,196,196)
                rects['quit']=pygame.Rect(500,720,280,60)
                
                screen.fill((0,0,255),(100,100,600,600))
                for key in rects.keys():
                    if key=="quit":
                        screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
                        screen.fill((127,127,127),rects[key])
                        self.write(rects[key],key,(200,200,200),75)
                    else:
                        screen.fill((127,127,127),rects[key])
                        self.write(rects[key],key,(200,200,200),100)
                        
                #draw the player names
                self.drawPlayers(0,hvbOpponent.name)
                self.drawScores(scores)
                
                pygame.display.flip()
                player=1
                self.drawPlayers(player,hvbOpponent.name)
                winner=0
                selected=False
                
                while menuActive:
                    #assess mouse clicks n shit
                    for event in pygame.event.get():
                        
                        #quit events
                        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                            running=False
                            menu=0
                            menuActive=False
                        
                        if player==1:
                            #capture mouse clicks
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                for key in rects.keys():
                                    if rects[key].collidepoint(event.pos):
                                        selected=key
                            
                            #capture key strokes
                            if event.type==pygame.KEYDOWN:
                                validKeys='123456789'
                                if event.unicode in validKeys:
                                    selected=event.unicode
                                
                    #logic for menu from the button clicks    
                    if player==2:
                        selected=str(self.pos2Selected(hvbOpponent.move(board)))
                    if selected:
                        if selected=="quit":
                            menuActive=False
                            menu=0
                        else:
                            pos=self.convertIndexToPos(int(selected))
                            #print pos,selected,rects[selected]
                            if self.validateMove(pos, board):
                                board[pos[1]][pos[0]]=player
                                self.drawMove(selected,player,rects)
                                pygame.display.update(rects[selected])
                                if self.findWinner(board):
                                    winner=player
                                else:
                                    player=self.switchPlayer(player)
                                    if not self.boardFull(board):
                                        self.drawPlayers(player,hvbOpponent.name)
                            selected=False
                
                    if (not winner==0) or self.boardFull(board):
                        if not winner==0:
                            self.drawPlayers(winner+2,hvbOpponent.name)
                            scores[winner-1]+=1
                            self.drawScores(scores)
                        else:
                            #draw
                            self.drawPlayers(5,hvbOpponent.name)
                            winner=1
                            
                        #reset game
                        player=winner
                        screen.fill((0,0,255),(100,100,600,600))
                        for key in rects.keys():
                            if key=="quit":
                                screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
                                screen.fill((127,127,127),rects[key])
                                self.write(rects[key],key,(200,200,200),75)
                            else:
                                screen.fill((127,127,127),rects[key])
                                self.write(rects[key],key,(200,200,200),100)
                        pygame.display.flip()
                        winner=0
                        board=[[0,0,0],[0,0,0],[0,0,0]]
                        self.drawPlayers(player,hvbOpponent.name)
                        selected=False
            
            menuActive=True
            if menu==4:
                scores=[0,0]
                #draw the bot vs bot game
                #draw the main screen
                board=[[0,0,0],[0,0,0],[0,0,0]]
                screen.fill((0,0,0))
                rects={}
                rects['1']=pygame.Rect(103,501,196,196)
                rects['2']=pygame.Rect(302,501,196,196)
                rects['3']=pygame.Rect(501,501,196,196)
                rects['4']=pygame.Rect(103,302,196,196)
                rects['5']=pygame.Rect(302,302,196,196)
                rects['6']=pygame.Rect(501,302,196,196)
                rects['7']=pygame.Rect(103,103,196,196)
                rects['8']=pygame.Rect(302,103,196,196)
                rects['9']=pygame.Rect(501,103,196,196)
                rects['quit']=pygame.Rect(500,720,280,60)
                
                screen.fill((0,0,255),(100,100,600,600))
                for key in rects.keys():
                    if key=="quit":
                        screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
                        screen.fill((127,127,127),rects[key])
                        self.write(rects[key],key,(200,200,200),75)
                    else:
                        screen.fill((127,127,127),rects[key])
                        self.write(rects[key],key,(200,200,200),100)
                        
                #draw the player names
                opponentNames=[]
                for key in opponents.keys():
                    opponentNames.append(key)
                #self.drawPlayers(0,hvbOpponent.name)
                self.drawBots(0,opponentNames)
                self.drawScores(scores)
                
                pygame.display.flip()
                player=1
                self.drawBots(player,opponentNames,1)
                winner=0
                selected=False
                move=0
                
                while menuActive:
                    #assess mouse clicks n shit
                    for event in pygame.event.get():
                        
                        #quit events
                        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                            running=False
                            menu=0
                            menuActive=False
                        
                        #capture mouse clicks
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            if rects['quit'].collidepoint(event.pos):
                                selected='quit'
                            
                    #logic for menu from the button clicks    
                    if selected=="quit":
                        menuActive=False
                        menu=0
                        
                    if move==0:
                        selected=str(randint(1,9))
                    else:
                        selected=str(self.pos2Selected(opponents[opponentNames[player-1]].move(board)))
                    move+=1
                    pos=self.convertIndexToPos(int(selected))
                    if self.validateMove(pos, board):
                        board[pos[1]][pos[0]]=player
                        self.drawMove(selected,player,rects)
                        pygame.display.update(rects[selected])
                        if self.findWinner(board):
                            winner=player
                        else:
                            player=self.switchPlayer(player)
                            if not self.boardFull(board):
                                self.drawBots(player,opponentNames,1)
                    selected=False
            
                    if (not winner==0) or self.boardFull(board):
                        if not winner==0:
                            self.drawBots(winner+2,opponentNames,500)
                            scores[winner-1]+=1
                            self.drawScores(scores)
                        else:
                            #draw
                            self.drawBots(5,opponentNames,500)
                            winner=1
                            
                        #reset game
                        player=winner
                        screen.fill((0,0,255),(100,100,600,600))
                        for key in rects.keys():
                            if key=="quit":
                                screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
                                screen.fill((127,127,127),rects[key])
                                self.write(rects[key],key,(200,200,200),75)
                            else:
                                screen.fill((127,127,127),rects[key])
                                self.write(rects[key],key,(200,200,200),100)
                        pygame.display.flip()
                        winner=0
                        board=[[0,0,0],[0,0,0],[0,0,0]]
                        move=0
                        self.drawBots(player,opponentNames,1)
                        selected=False
                
    def write(self,posRect,text,colour,fontSize):
        myFont=pygame.font.Font("WHITRABT.TTF",fontSize)
        mySize=myFont.size(text)
        cursor=(posRect[2]/2)-(mySize[0]/2)+posRect[0],(posRect[3]/2)-(mySize[1]/2)+posRect[1]
        self.screen.blit(myFont.render(text,True,colour),cursor)
    
    def drawBots(self,code,opponentNames,delay=None):
        p1=opponentNames[0]
        p2=opponentNames[1]
        
            
        rects={}
        rects[p1]=pygame.Rect(20,20,200,60)
        rects[p2]=pygame.Rect(580,20,200,60)
        for key in rects.keys():
            self.screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
            self.screen.fill((120,120,120),rects[key])
            self.write(rects[key], key, (0,0,0), 25)
            pygame.display.update(rects[key])
        if code==0:
            pass
        else:
            timeStart=pygame.time.get_ticks()
            if code==1:
                if delay:
                    delayer=delay
                else:
                    delayer=300
                
                while (pygame.time.get_ticks()-timeStart<=delayer):
                    timeNow=pygame.time.get_ticks()-timeStart
                    rectToUpdate=pygame.Rect(rects[p1][0],rects[p1][1],rects[p1][2],int((rects[p1][3]/float(delayer))*timeNow))
                    pygame.draw.rect(self.screen, (0,255,0),rectToUpdate)
                    self.write(rects[p1], p1, (0,0,0), 25)
                    pygame.display.update(rectToUpdate)
                pygame.draw.rect(self.screen, (0,255,0),rects[p1])
                self.write(rects[p1], p1, (0,0,0), 25)
                pygame.display.update(rects[p1])
            if code==2:
                if delay:
                    delayer=delay
                else:
                    delayer=300
                
                while (pygame.time.get_ticks()-timeStart<=delayer):
                    timeNow=pygame.time.get_ticks()-timeStart
                    rectToUpdate=pygame.Rect(rects[p2][0],rects[p2][1],rects[p2][2],int((rects[p2][3]/float(delayer))*timeNow))
                    pygame.draw.rect(self.screen, (0,255,0),rectToUpdate)
                    self.write(rects[p2], p2, (0,0,0), 25)
                    pygame.display.update(rectToUpdate)
                pygame.draw.rect(self.screen, (0,255,0),rects[p2])
                self.write(rects[p2], p2, (0,0,0), 25)
                pygame.display.update(rects[p2])
            if code==3:
                if delay:
                    delayer=delay
                else:
                    delayer=1000
                while (pygame.time.get_ticks()-timeStart<=delayer):
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p1])
                    self.write(rects[p1], p1, (0,0,0), 25)
                    pygame.display.update(rects[p1])
            if code==4:
                if delay:
                    delayer=delay
                else:
                    delayer=1000
                while (pygame.time.get_ticks()-timeStart<=delayer):
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p2])
                    self.write(rects[p2], p2, (0,0,0), 25)
                    pygame.display.update(rects[p2])
            if code==5:
                if delay:
                    delayer=delay
                else:
                    delayer=1000
                while (pygame.time.get_ticks()-timeStart<=delayer):
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p1])
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p2])
                    self.write(rects[p1], p1, (0,0,0), 25)
                    self.write(rects[p2], p2, (0,0,0), 25)
                    pygame.display.update((rects[p2],rects[p1]))
            
    def drawPlayers(self,code,bot=None):
        """
        @summary: draws the player labels at the top of the play screen, for hvh games
        @param code:
        @return: Void, draws to the screen
        @note: 0=draw both player symbols, 1=draw player one's turn, 2=draw player two's turn, 3=draw player one's win, 4=draw player two's win, 5 draw a draw
        
        """
        p1='Player 1'
        p2='Player 2'
        if bot:
            p2=bot
            
        rects={}
        rects[p1]=pygame.Rect(20,20,200,60)
        rects[p2]=pygame.Rect(580,20,200,60)
        for key in rects.keys():
            self.screen.fill((0,0,255),(rects[key][0]-3,rects[key][1]-3,rects[key][2]+6,rects[key][3]+6))
            self.screen.fill((120,120,120),rects[key])
            self.write(rects[key], key, (0,0,0), 25)
            pygame.display.update(rects[key])
        if code==0:
            pass
        else:
            timeStart=pygame.time.get_ticks()
            if code==1:
                delay=300
                while (pygame.time.get_ticks()-timeStart<=delay):
                    timeNow=pygame.time.get_ticks()-timeStart
                    rectToUpdate=pygame.Rect(rects[p1][0],rects[p1][1],rects[p1][2],int((rects[p1][3]/float(delay))*timeNow))
                    pygame.draw.rect(self.screen, (0,255,0),rectToUpdate)
                    self.write(rects[p1], p1, (0,0,0), 25)
                    pygame.display.update(rectToUpdate)
                pygame.draw.rect(self.screen, (0,255,0),rects[p1])
                self.write(rects[p1], p1, (0,0,0), 25)
                pygame.display.update(rects[p1])
            if code==2:
                delay=300
                while (pygame.time.get_ticks()-timeStart<=delay):
                    timeNow=pygame.time.get_ticks()-timeStart
                    rectToUpdate=pygame.Rect(rects[p2][0],rects[p2][1],rects[p2][2],int((rects[p2][3]/float(delay))*timeNow))
                    pygame.draw.rect(self.screen, (0,255,0),rectToUpdate)
                    self.write(rects[p2], p2, (0,0,0), 25)
                    pygame.display.update(rectToUpdate)
                pygame.draw.rect(self.screen, (0,255,0),rects[p2])
                self.write(rects[p2], p2, (0,0,0), 25)
                pygame.display.update(rects[p2])
            if code==3:
                delay=1000
                while (pygame.time.get_ticks()-timeStart<=delay):
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p1])
                    self.write(rects[p1], p1, (0,0,0), 25)
                    pygame.display.update(rects[p1])
            if code==4:
                delay=1000
                while (pygame.time.get_ticks()-timeStart<=delay):
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p2])
                    self.write(rects[p2], p2, (0,0,0), 25)
                    pygame.display.update(rects[p2])
            if code==5:
                delay=1000
                while (pygame.time.get_ticks()-timeStart<=delay):
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p1])
                    self.screen.fill((randint(0,255),randint(0,255),randint(0,255)),rects[p2])
                    self.write(rects[p1], p1, (0,0,0), 25)
                    self.write(rects[p2], p2, (0,0,0), 25)
                    pygame.display.update((rects[p2],rects[p1]))
                    
    def convertIndexToPos(self,index):
        myIndex=index-1
        y=2-int(math.floor(myIndex/float(3)))
        x=myIndex%3
        return x,y
    
    def pos2Selected(self,pos):
        return ((2-pos[1])*3)+(pos[0]+1)
    
    def drawMove(self,selected,player,rects):
        if player==1:
            pygame.draw.line(self.screen, (255,255,255), (rects[selected][0]+10,rects[selected][1]+10), (rects[selected][0]+10+rects[selected][2]-20,rects[selected][1]+10+rects[selected][3]-20), 8)
            pygame.draw.line(self.screen, (255,255,255), (rects[selected][0]+10,rects[selected][1]+10+rects[selected][3]-20),(rects[selected][0]+10+rects[selected][2]-20,rects[selected][1]+10),8)
        if player==2:
            pygame.draw.circle(self.screen, (255,255,255), (rects[selected][0]+rects[selected][2]/2,rects[selected][1]+rects[selected][3]/2), rects[selected][3]/2, 8)
        
        
    def convertTime(self,secs):
        hrs=secs/float(3600)
        hours=math.floor(hrs)
        mins=(hrs-hours)*60
        minutes=math.floor(mins)
        secs=(mins-minutes)*60
        seconds=math.floor(secs)
        return hours,minutes,seconds
     
    def printStatsToConsole(self,stats):
        print "Game Results:\n"
        for i in range(1,len(stats)+1):
            
            print "Player: %s" % (stats[i-1]['Player'].name)
            for key in stats[i-1].keys():
                if not key=="Player":
                    if key=="Average Move Time" or key=="Bot Loading Time" or key=="Worst Move Time" or key=="Best Move Time":
                        print "%s: %0.10f" % (key,stats[i-1][key])
                    else:
                        print "%s: %s" % (key,str(stats[i-1][key]))
            print
        
        #organise a list of winners
        newList = sorted(stats, key=lambda k: k['Number of Wins'])
        newList.reverse()
        
        #print the stats
        if newList[0]['Number of Wins']==newList[1]['Number of Wins']:
            print "ITS A DRAW!!!!"
        else:
            count=1
            for item in newList:
                print "%s finished in place %s" % (item['Player'].name, str(count))
                count+=1
            print "\n%s IS THE WINNER!!!" % (newList[0]['Player'].name)
       
       
    def switchPlayer(self,player):
        if player==1:
            return 2
        else:
            return 1
    def validateMove(self,pos,board):
        if board[pos[1]][pos[0]]==0:
            return True
        else:
            return False
    
    def drawScores(self,scores):
        rects={}
        rects[0]=pygame.Rect(220,20,180,60)
        rects[1]=pygame.Rect(400,20,180,60)
        for key in rects.keys():
            self.screen.fill((0,0,0),rects[key])
            self.write(rects[key], str(scores[key]), (120,120,120), 40)
    
    def boardFull(self,board):
        for x in range(3):
            for y in range(3):
                if board[y][x]==0:
                    return False
        return True
    
    def findWinner(self,board):
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
    
    def printBoard(self,board):
        print "%s|%s|%s" % (str(board[0][0]),str(board[0][1]),str(board[0][2]))
        print "-----"
        print "%s|%s|%s" % (str(board[1][0]),str(board[1][1]),str(board[1][2]))
        print "-----"
        print "%s|%s|%s" % (str(board[2][0]),str(board[2][1]),str(board[2][2]))
    
       
       