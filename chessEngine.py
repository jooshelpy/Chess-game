""" 
this class is responsible for storing all the information about the current state of chess game.it will also 
responsible for determing the valid moves of the current state 
"""

class GameState():
    def __init__(self):
        # board is 8*8 2D list, each element of the list has two charcters
        # the first character represents the color "b" or "w"
        # the second character represents the piece "B" , "N", "R", "K", "Q", "p"
        # "--" represents an empty space with no piece
        
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bR", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {"p" : self.getPawnMoves, "R" : self.getRookMoves, "B" : self.getBishopMoves,
                            "N" : self.getKnightMoves, "K" : self.getKingMoves, "Q" : self.getQueenMoves}

        self.whiteToMove = True
        self.moveLog = [] # to store all the moves 

    def makeMove(self, move):
        """Take a move as a parameter and execute it. (it will not work with castling, pawn promotion and en-passant)"""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it
        self.whiteToMove = not self.whiteToMove # swap players

    def undoMove(self):
        if len(self.moveLog) != 0: # if the movlog is not empty
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove    

    def getValidMoves(self) -> list:
        """get all possible moves with considering checks"""
        return self.getAllPossibleMoves() # for now we will not worry about checks

    def getAllPossibleMoves(self) -> list:
        """get all possible moves without considering checks"""
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in a given row
                color = self.board[r][c][0]
                if (color == "w" and self.whiteToMove) or (color == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves 
    
    def getPawnMoves(self, r, c, moves:list):
        """get all the pawn moves for the pawn located at row, col and add these moves to the list"""
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #1 white square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":#2 square pawn advande
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #pawn black moves
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    # print("here")
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))


    def getRookMoves(self, r, c, moves:list):
        """get all the Rook moves for the pawn located at row, col and add these moves to the list"""
        if self.whiteToMove:
            same = "w"
            notSame = "b"
        else:
            same = "b"
            notSame = "w"

        for i in range(7-c): #  right 
            if self.board[r][i+c+1][0] == same:
                break
            if self.board[r][i+c+1][0] == notSame:
                moves.append(Move((r, c), (r, i+c+1), self.board))
                break
            else:
                moves.append(Move((r, c), (r, i+c+1), self.board))

        for i in range(7-r): # bottom 
            if self.board[r+i+1][c][0] == same:
                break
            if self.board[r+i+1][c][0] == notSame:
                moves.append(Move((r, c), (r+i+1, c), self.board))
                break
            else:
                moves.append(Move((r, c), (r+i+1, c), self.board))

        for i in range(r): # top
            if self.board[r-i-1][c][0] != same:
                break
            if self.board[r-i-1][c][0] == notSame:
                moves.append(Move((r, c), (r-i-1, c), self.board))
                break
            else:
                moves.append(Move((r, c), (r-i-1, c), self.board))

        for i in range(c): # left
            if self.board[r][c-i-1][0] != same:
                break
            if self.board[r][c-i-1][0] == notSame:
                moves.append(Move((r, c), (r, c-i-1), self.board))
                break
            else:
                moves.append(Move((r, c), (r, c-i-1), self.board))

    def getBishopMoves(self, r, c, moves:list):
        """get all the Bishop moves for the pawn located at row, col and add these moves to the list"""
        if self.whiteToMove:
            same = "w"
            notSame = "b"
        else:
            same = "b"
            notSame = "w"

        for i in range(min(7-c, r)): # top right moves
            if self.board[r-i-1][c+i+1][0] == same:
                break
            if self.board[r-i-1][c+i+1][0] == notSame:
                moves.append(Move((r, c), (r-i-1, c+i+1), self.board))
                break
            else:
                moves.append(Move((r, c), (r-i-1, c+i+1), self.board))

        for i in range(min(7-c, 7-r)): # bottom right moves
            if self.board[r+i+1][c+i+1][0] == same:
                break
            if self.board[r+i+1][c+i+1][0] == notSame:
                moves.append(Move((r, c), (r+i+1, c+i+1), self.board))
                break
            else:
                moves.append(Move((r, c), (r+i+1, c+i+1), self.board))

        for i in range(min(c, 7-r)): # bottom left moves
            if self.board[r+i+1][c-i-1][0] == same:
                break
            if self.board[r+i+1][c-i-1][0] == notSame:
                moves.append(Move((r, c), (r+i+1, c-i-1), self.board))
                break
            else:
                moves.append(Move((r, c), (r+i+1, c-i-1), self.board))

        for i in range(min(c, r)): # top left moves
            if self.board[r-i-1][c-i-1][0] == same:
                break
            if self.board[r-i-1][c-i-1][0] == notSame:
                moves.append(Move((r, c), (r-i-1, c-i-1), self.board))
                break
            else:
                moves.append(Move((r, c), (r-i-1, c-i-1), self.board))

    def getKnightMoves(self, r, c, moves):
        """get all the Knight moves for the pawn located at row, col and add these moves to the list"""
        pass

    def getQueenMoves(self, r, c, moves):
        """get all the Queen moves for the pawn located at row, col and add these moves to the list"""
        pass

    def getKingMoves(self, r, c, moves):
        """get all the Knight moves for the pawn located at row, col and add these moves to the list"""
        pass    




class Move():
    # maps keys to values
    ranksToRows = {"1" : 7, "2" : 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {val: key for key, val in ranksToRows.items()}

    filesToCols = {"a" : 0, "b" : 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {val: key for key, val in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]       
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 
        # print(self.moveID)

    def __eq__(self, other) -> bool:
        """overriding the equals method"""
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r] # b6 || a5 .....
