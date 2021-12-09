#Driver file, responsabile de,la gestione dell'input utente e di mostare il GameState corrente
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 #in alternativa 400
DIMENSION = 8 #la dimensione della scacchiera è 8x8
SQ_SIZE = HEIGHT // DIMENSION #// è la divisione
MAX_FPS = 15 #Per le animazioni
IMAGES = {}#dizionario delle immagini

'''
il caricamento delle immagine in pygame è un'operazione pesante, di conseguena vogliamo che venga effettuata una sola volta,
all'inizizalizzazione. 
'''
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "bP", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR" ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("pieces_images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Nota: possiamo accedere ad un'immagine tramite 'IMAGES["wP"]', questa variabile mi restituisce l'immagine del pezzo (thx al dizionario)

'''
Da qui creiamo il driver principale che controllerà gli input utente e la visualizzazione del gioco
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Variabile di controllo quando una mossa viene fatta (cambio del GameState)
    loadImages() #Quest'operazione viene eseguita una sola volta, prima del while
    running = True
    sqSelected = ()#Inizialmente nessun quadrato è selezionato,m tiene traccia dell'ultimo clock dell'utente (tuple: (row,column))
    playerClicks = [] #Tiene traccia dei click dell'utente (due tuple: [(6, 4), (4,4)]) posizione iniziale del pezzo mosso  e finale
    

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #controllore del mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #Coordinate (x,y) del mouse quando viene premuto il bottone
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col): #Se l'utente clicca due volte lo stesso quadrato
                    sqSelected = () #Deseleziona
                    playerClicks = [] #Reset dei click dell'utente
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #Mette in coda primo e secondo click
                if len(playerClicks) == 2: #Dopo il secondo click
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)#TODO Fixare click lock del pezzo
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = () #Reset degli input utente
                            playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Se viene premuto il tasto "z" viene riportata la scacchiera alla mossa (t-1)
                    gs.undoMove()
                    moveMade = False
                    gs.whiteToMove = not gs.whiteToMove
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Resposabile per le grafiche nel GameState corrente
'''

def drawGameState(screen, gs):
    drawBoard(screen) #Disegna la scacchiera
    #Qui si possono aggiungere i suggerimenti di mossa, l'highlighting dei pezzi ecc...
    drawPieces(screen, gs.board) #Disegna i pezzi

#Disegna la scacchiera
def drawBoard(screen):
    colors = [p.Color("White"), p.Color("Grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) %2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Disegna i pezzi utilizzando GameState.board (quindi con le modifiche)
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__": #Standard python
    main()