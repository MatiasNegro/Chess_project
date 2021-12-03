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
    loadImages() #Quest'operazione viene eseguita una sola volta, prima del while
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

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