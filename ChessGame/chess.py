'''
Hoang Dinh Nguyen
Taken from a Github page and modified to be Chinese Chess
TODO: Add a condition to end the game (get the Kings to attack each other and end the game when there is no king)
'''

"""CONVENTIONS:
positions are done row-column from the bottom left and are both numbers. This corresponds to the alpha-number system in traditional chess while being computationally useful. they are specified as tuples
"""
from random import shuffle
import itertools
WHITE = "white"
BLACK = "black"

class Game:
    #ive decided since the number of pieces is capped but the type of pieces is not (pawn transformations), I've already coded much of the modularity to support just using a dictionary of pieces
    def __init__(self):
        self.playersturn = BLACK
        self.message = "this is where prompts will go"
        self.gameboard = {} # maps from tuples to Piece Objects
        self.placePieces()
        print("chess program. enter moves in algebraic notation separated by space")
        self.main()

        
    def placePieces(self):

        for i in range(0,9,2):
            self.gameboard[(i,3)] = Pawn(WHITE,"?")
            self.gameboard[(i,6)] = Pawn(BLACK,"?")

        self.gameboard[(1,2)] = Cannon(WHITE,"?")
        self.gameboard[(7,2)] = Cannon(WHITE,"?")
        self.gameboard[(1,7)] = Cannon(BLACK,"?")
        self.gameboard[(7,7)] = Cannon(BLACK,"?")
        placers = [Rook,Knight,Bishop,AdvisorBegin,King,AdvisorBegin,Bishop,Knight,Rook]
        
        for i in range(0,9):
            self.gameboard[(i,0)] = placers[i](WHITE,"?")
            self.gameboard[((8-i),9)] = placers[i](BLACK,"?")
        placers.reverse()
        self.gameboard[(4,0)] = King(WHITE,uniDict[WHITE][King])
        self.gameboard[(4,9)] = King(BLACK,uniDict[BLACK][King])

        
    def main(self):
        placers = [Rook,Knight,Bishop,Advisor,Advisor,Bishop,Knight,Rook,Cannon,Cannon,Pawn,Pawn,Pawn,Pawn,Pawn]        
        insertListWhite = [i(WHITE, uniDict[WHITE][i]) for i in placers]
        insertListBlack = [i(BLACK, uniDict[BLACK][i]) for i in placers]
        while True:
            self.printBoard()
            print(self.message)
            self.message = ""
            startpos,endpos = self.parseInput()
            try:
                target = self.gameboard[startpos]
            except:
                self.message = "could not find piece; index probably out of range"
                target = None
                
            if target:
                print("found "+str(target))
                if target.Color != self.playersturn:
                    self.message = "you aren't allowed to move that piece this turn"
                    continue
                if target.isValid(startpos,endpos,target.Color,self.gameboard):
                    self.message = "that is a valid move"
                    self.gameboard[endpos] = self.gameboard[startpos]
                    del self.gameboard[startpos]
                    if(self.gameboard[endpos].name == "?" and self.gameboard[endpos].Color == BLACK):
                        shuffle(insertListBlack)
                        self.gameboard[endpos] = insertListBlack.pop()
                    elif(self.gameboard[endpos].name == "?" and self.gameboard[endpos].Color == WHITE):
                        shuffle(insertListWhite)
                        self.gameboard[endpos] = insertListWhite.pop()
                    self.isCheck()
                    if self.playersturn == BLACK:
                        self.playersturn = WHITE
                    else : self.playersturn = BLACK
                else : 
                    self.message = "invalid move" + str(target.availableMoves(startpos[0],startpos[1],self.gameboard))
                    print(target.availableMoves(startpos[0],startpos[1],self.gameboard))
            else : self.message = "there is no piece in that space"
                    
    def isCheck(self):
        #ascertain where the kings are, check all pieces of opposing color against those kings, then if either get hit, check if its checkmate
        king = King
        kingDict = {}
        pieceDict = {BLACK : [], WHITE : []}
        for position,piece in self.gameboard.items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece,position))
        #WHITE
        if self.canSeeKing(kingDict[WHITE],pieceDict[BLACK]):
            self.message = "White player is in check"
        if self.canSeeKing(kingDict[BLACK],pieceDict[WHITE]):
            self.message = "Black player is in check"
        
        
    def canSeeKing(self,kingpos,piecelist):
        #checks if any pieces in piece list (which is an array of (piece,position) tuples) can see the king in kingpos
        for piece,position in piecelist:
            if piece.isValid(position,kingpos,piece.Color,self.gameboard):
                return True
                
    def parseInput(self):
        try:
            a,b = input().split()
            a = ((ord(a[0])-97), int(a[1:len(a)])-1)
            b = (ord(b[0])-97, int(b[1:len(b)])-1)
            print(a,b)
            return (a,b)
        except:
            print("error decoding input. please try again")
            return((-1,-1),(-1,-1))

    def printBoard(self):
        print("    1   2   3   4   5   6   7   8   9   10")
        for i in range(0, 8):
            print(chr(i+97) , end="   " + str(self.gameboard.get((i, 0), " ")))
            for j in range(1, 10):
                item = self.gameboard.get((i, j), " ")
                if(j != 5):
                    print("___" + str(item), end="")
                else:
                    print("   " + str(item), end="")
            print()
            print("    |   |   |   |   |   |   |   |   |   |")

        print(chr(8+97) , end="   " + str(self.gameboard.get((8, 0), " ")))
        for j in range(1, 10):
            item = self.gameboard.get((8, j), " ")
            if(j != 5):
                print("___" + str(item), end="")
            else:
                print("   " + str(item), end="")
        print()
            
    """game class. contains the following members and methods:
    two arrays of pieces for each player
    8x8 piece array with references to these pieces
    a parse function, which turns the input from the user into a list of two tuples denoting start and end points
    a checkmateExists function which checks if either players are in checkmate
    a checkExists function which checks if either players are in check (woah, I just got that nonsequitur)
    a main loop, which takes input, runs it through the parser, asks the piece if the move is valid, and moves the piece if it is. if the move conflicts with another piece, that piece is removed. ischeck(mate) is run, and if there is a checkmate, the game prints a message as to who wins
    """

class Piece:
    
    def __init__(self,color,name):
        self.name = name
        self.position = None
        self.Color = color
    def isValid(self,startpos,endpos,Color,gameboard):
        if endpos in self.availableMoves(startpos[0],startpos[1],gameboard, Color = Color):
            return True
        return False
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def availableMoves(self,x,y,gameboard):
        print("ERROR: no movement for base class")
        
    def AdNauseum(self,x,y,gameboard, Color, intervals):
        """repeats the given interval until another piece is run into. 
        if that piece is not of the same color, that square is added and
         then the list is returned"""
        answers = []
        for xint,yint in intervals:
            xtemp,ytemp = x+xint,y+yint
            while self.isInBounds(xtemp,ytemp):
                #print(str((xtemp,ytemp))+"is in bounds")
                
                target = gameboard.get((xtemp,ytemp),None)
                if target is None: answers.append((xtemp,ytemp))
                elif target.Color != Color:
                    answers.append((xtemp,ytemp))
                    break
                else:
                    break
                
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return answers
                
    def isInBounds(self,x,y):
        "checks if a position is on the board"
        if y >= 0 and y < 10 and x >= 0 and x < 9:
            return True
        return False

    def isInBoundsHalf(self, x, y, Color):
        "checks if a position is on the half board"
        if Color == WHITE:
            if y >= 0 and y <= 4 and x >= 0 and x < 9:
                return True
            return False
        elif Color == BLACK:
            if y >= 5 and y <= 9 and x >= 0 and x < 9:
                return True
            return False

    def isInBoundsPalace(self, x, y, Color):
        "checks if a position is on the half board"
        if Color == WHITE:
            if y >= 0 and y <= 2 and x >= 3 and x <= 5:
                return True
            return False
        elif Color == BLACK:
            if y >= 7 and y <= 9 and x >= 3 and x <= 5:
                return True
            return False
            
    
    def noConflict(self,gameboard,initialColor,x,y):
        "checks if a single position poses no conflict to the rules of chess"
        if self.isInBounds(x,y) and (((x,y) not in gameboard) or gameboard[(x,y)].Color != initialColor) : return True
        return False
        
        
chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)]
chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]
bishopMoves = [(2,2),(-2,2),(2,-2),(-2,-2)]

def knightList(x,y, gameboard):
    answer = []
    if((x+1,y) not in gameboard): 
        answer.append((x+2,y+1))
        answer.append((x+2,y-1))
    if((x-1,y) not in gameboard): 
        answer.append((x-2,y+1))
        answer.append((x-2,y-1))
    if((x,y+1) not in gameboard): 
        answer.append((x+1,y+2))
        answer.append((x-1,y+2))
    if((x,y-1) not in gameboard): 
        answer.append((x+1,y-2))
        answer.append((x-1,y-2))
    return answer


class Knight(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return [(xx,yy) for xx,yy in knightList(x,y,gameboard) if self.noConflict(gameboard, Color, xx, yy)]
        
class Rook(Piece):
    def availableMoves(self,x,y,gameboard ,Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals)
        
class Advisor(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        for xint,yint in chessDiagonals:
            xtemp,ytemp = x+xint,y+yint
            if(self.isInBounds(xtemp, ytemp)):
                target = gameboard.get((xtemp,ytemp),None)
                if (target is None) or (target.Color != Color):
                    answers.append((xtemp,ytemp))
        return answers

class AdvisorBegin(Advisor):
    def availableMoves(self,x,y,gameboard, Color = None):
        moves = super(AdvisorBegin, self).availableMoves(x,y,gameboard, Color = None)
        return [(x_ans, y_ans) for (x_ans, y_ans) in moves if self.isInBoundsPalace(x_ans, y_ans, Color)]

class Bishop(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        for xint,yint in bishopMoves:
            xtemp,ytemp = x+xint,y+yint
            if(self.isInBounds(xtemp, ytemp)):
                target = gameboard.get((xtemp,ytemp),None)
                if (target is None) or (target.Color != Color):
                    answers.append((xtemp,ytemp))
        return answers
        
class Cannon(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        for xint,yint in chessCardinals:
            xtemp,ytemp = x+xint,y+yint
            while self.isInBounds(xtemp,ytemp):
                target = gameboard.get((xtemp,ytemp),None)
                if target is None: answers.append((xtemp,ytemp))
                else:
                    xtemp,ytemp = xtemp + xint,ytemp + yint
                    target = gameboard.get((xtemp,ytemp),None)
                    while (target is None) and (self.isInBounds(xtemp,ytemp)):
                        xtemp,ytemp = xtemp + xint,ytemp + yint
                        target = gameboard.get((xtemp,ytemp),None)
                    if (target is not None) and (target.Color != Color):
                        answers.append((xtemp,ytemp))
                    break
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return answers
        
class King(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return [(xx,yy) for xx,yy in [(x+1,y),(x,y+1),(x,y-1),(x-1,y)] if self.isInBoundsPalace(xx, yy, Color)]
        
class Pawn(Piece):
    def __init__(self,color,name):
        self.name = name
        self.Color = color
        if color == WHITE : self.direction = 1 
        else : self.direction = -1
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        if (x,y+self.direction) in gameboard and self.noConflict(gameboard, Color, x, y+self.direction) : answers.append((x,y+self.direction))
        if (x,y+self.direction) not in gameboard and Color == self.Color : answers.append((x,y+self.direction))
        if (not self.isInBoundsHalf(x,y,Color)):
            if self.noConflict(gameboard, Color, x+1, y) : answers.append((x+1,y))
            if self.noConflict(gameboard, Color, x-1, y) : answers.append((x-1,y))
        return answers

uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "T", King : "♔", Cannon : "P", Advisor : "A", AdvisorBegin : "A" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "T", King : "♚", Cannon : "P", Advisor : "A", AdvisorBegin : "A" }}
        


Game()
