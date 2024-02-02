"""
this is our main driver file. it will be responsible for handling user input and displaying the current gameState object
"""

import pygame as p
import chessEngine 

Width = Height = 512
Dimension = 8   # dimension of the chess board 8*8
SQ_size = Height // Dimension
Max_FPS = 15     # for animation
Images = {}

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_size, SQ_size))

def main():
    """this main driver for out code. this will handle user input and updating the grapics."""
    p.init()
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))     
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMode = False # flag variable for when a move is made
    # print(gs.board)
    loadImages() # it is called only once
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of the user clicks (two tuples: [(6,4), (4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of the mouse
                # print(location)
                col = location[0] // SQ_size
                row = location[1] // SQ_size
                if sqSelected == (row, col): # if the user clicked the same square twice
                    sqSelected = () # deSelect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both the 1st and second click
                if len(playerClicks) == 2: # after the second click
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move) # make changes in the game state board
                        moveMode = True
                    sqSelected = () # reset your clicks
                    playerClicks = [] # clear player clicks

            # keyboard handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()

        if moveMode: 
            validMoves = gs.getValidMoves() # it called only once every time a move is made 
            moveMode = False
        
        drawGameState(screen, gs)
        clock.tick(Max_FPS)   
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_size, r*SQ_size, SQ_size, SQ_size))


def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--": #not empty
                screen.blit(Images[piece], p.Rect(c*SQ_size, r*SQ_size, SQ_size, SQ_size))


if __name__ == "__main__":
    main()       

