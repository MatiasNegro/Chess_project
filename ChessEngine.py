#Classe responsabile della gestione delle informazione riguardanti lo stato della partita di scacchi.
# Sarà anche risponsabile per la determinazione delle mosse valide allos tato corrente
#Mantiene anche il log delle mosse

class GameState():
    def __init__(self):
       #La scacchiera è una matrice 8x8, ogni elemento della lista è composto da 2 caratteri, rappresentanti rispettivamente
       # colore e pezzo.
       # "--" rappresenta la casella vuota 
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP" ,"bP" ,"bP" ,"bP" ,"bP" ,"bP" ,"bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP" ,"wP" ,"wP" ,"wP" ,"wP" ,"wP" ,"wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves,
                                'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blacKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #Inizializzazione delle  coordinate del quadrato ove è possibile eseguire l'enpassant
        self.currentCastlingRights = CastleRights( True,True,True,True) #Gestione dell'arrocco
        self.castleRightLog = [CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide, 
                                            self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide)]


    
    '''
    Prende come parametro una mossa e la esegue (Non funziona per l'arrocco, promozione del pedone e en-passant)
    '''
    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Aggiungo la mossa al log delle mosse definito in precedenza
        self.whiteToMove = not self.whiteToMove #Cambio del turno se era bianco ora tocca al nero e viceversa
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blacKingLocation = (move.endRow, move.endCol)

        #Promozione del pedone
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        #Enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #Cattura del pedone con enpassant
            


        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol) 
        else:
            self.enpassantPossible = ()

        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #Dal lato del re
                self.board[move.endRow][move.endCol] = self.board[move.endRow][move.endCol + 1] #Copia la torre nel nuovo quadrato
                self.board[move.endRow][move.endCol + 1] = '--' #Cancello la vecchia torre
            else: #Dal lato della regina
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] #Copia la torre nel nuovo quadrato
                self.board[move.endRow][move.endCol - 2] = '--'
            

        #Aggiornamento della variabile di arrocco, ciò deve avvenire ogni volta ion cui avviene una mossa del re o torre
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide, 
                                            self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide))


                

    #Torna indietro alla mossa eseguita prima di quella attuale
    def undoMove(self):
        if len(self.moveLog) != 0: #Controllo che il log delle mosse non sia vuoto
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #cambia il turno (a quello precedente)
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blacKingLocation = (move.startRow, move.startCol)
        
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #Lascia il quadrato vuoto
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
                print("HO FATTO L'UNDO DELL'ENPASSANT")
            
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            #undo dei diritti di arrocco
            self.castleRightLog.pop() #Togliamo i diritti di arrocco attuali
            self.currentCastlingRights = self.castleRightLog[-1] #mettiamo i diritti di castling all'ultimo elemento della lista,
                                                                 #ergo quello precedente  
            #undo della mossa di arrocco
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #Dal lato del re
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            


    def updateCastleRights(self, move): #Controllare con switch case --> refactor
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.whiteKingSide = False 
            self.currentCastlingRights.whiteQueenSide = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.blackKingSide = False
            self.currentCastlingRights.blackQueenSide = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #Torre sinistra
                    self.currentCastlingRights.whiteQueenSide = False
                elif move.startCol == 7: #Torre destra
                    self.currentCastlingRights.whiteKingSide = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #Torre sinistra
                    self.currentCastlingRights.whiteQueenSide = False
                elif move.startCol == 7: #Torre destra
                    self.currentCastlingRights.whiteKingSide = False

         


    '''
    Mosse di controllo di scacco
    '''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        print("GENERO LE MOSSE DELL'AVVERSARIO")
        tempCastling = CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide,
                                    self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, allyColor='w')
        else:
            self.getCastleMoves(self.blacKingLocation[0], self.blacKingLocation[1], moves, allyColor='b')

        #Utilizziamo l'algoritmo di Naiv
        for i in range(len(moves) - 1, -1, -1):#Scorro la list al contrario per evitare bug di shift degli indici sugli elementi non ancora 
            self.makeMove(moves[i])    #controllati
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                moves.remove(moves[i]) #Se la mossa rende il re in scacco non è valida

            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            

        if len(moves) == 0: #Controllo che non sia scacco matto
            if self.inCheck():
                self.checkMate = True
                print("SCACCO MATTO")
            else:
                self.staleMate = True

        self.currentCastlingRights = tempCastling
        self.enpassantPossible = tempEnpassantPossible


        return moves


    #Controllo se un re è in scacco
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blacKingLocation[0], self.blacKingLocation[1])
    
    #Controllo se l'avversario può spostarsi in posizione (r, c)
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #Controllo che la posizione sia sotto attacco
                self.whiteToMove = not self.whiteToMove
                return True

        self.whiteToMove = not self.whiteToMove
        return False

    '''
    Restanti mosse (non controllanti lo scacco)
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #righe
            for c in range(len(self.board[r])): #colonne
                turn = self.board[r][c][0] #accedo al rpimo carattere della matrice (indicante se il quadrato contiene un pezzo bianco o nero
                if (turn == 'w' and self.whiteToMove) or (turn== 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] #accedo al secondo carattere
                    self.moveFunctions[piece](r, c, moves) #Chiama la funzione corretta per ogni pezzo
        return moves

    '''
    Genero le mosse che un pedone può fare in quella determinata posizione (riga, colonna) ed aggiungo tali mosse alla lista
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #Se la mossa è del bianco ci concentriamo su quest'ultimo
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #Avanzamento del pedone all'inizio
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #Cattura a sinistra
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove = True))
            if c+1 <= 7: #Cattura a destra
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove = True))

        else: #Pezzi neri
            if self.board[r+1][c] == "--": #Avanzamento di una posizione
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #Avanzamento di due posizioni
                    moves.append(Move((r, c), (r+2, c), self.board))
                    
            #Catture
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove = True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove = True))


    '''
    Genero le mosse che una torre può fare in quella determinata posizione (riga, colonna) ed aggiungo tali mosse alla lista
    '''
    def getRookMoves(self,r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #Su, sinistra, giù, destra
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #All'interno della scacchiera
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #casella vuota, mossa valida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Pezzo nemico, mossa valida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Pezzo della stessa squadra, mossa non valida
                        break
                else:   #Fuori scacchiera, mossa non valida
                    break

    def getKnightMoves(self,r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    #Genero tutte le mosse valide della torre per il re in posizione (r,c)
    def getCastleMoves(self, r, c, moves, allyColor):
        if self.squareUnderAttack(r, c):
            return #Non si può fare l'arrocco se il re è in wscacco
        if (self.whiteToMove and self.currentCastlingRights.whiteKingSide) or (not self.whiteToMove and self.currentCastlingRights.blackKingSide):
            self.getKingSideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.currentCastlingRights.whiteQueenSide) or (not self.whiteToMove and self.currentCastlingRights.blackQueenSide):
             self.getQueenSideCastleMoves(r, c, moves, allyColor)

    def getKingSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))

    def getQueenSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))


    
    def getBishopMoves(self,r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #All'interno della scacchiera
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #casella vuota, mossa valida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Pezzo nemico, mossa valida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Pezzo della stessa squadra, mossa non valida
                        break
                else:   #Fuori scacchiera, mossa non valida
                    break



    def getQueenMoves(self,r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self,r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

'''Classe per gestione dell'arrocco, si potrebbe anche effettuare l'arrocco con un parametro interno alla gestione delle mosse dei pezzi 
tramite l'aggiunta di un attributo nella classe Move.
tale soluzione risulta al momento confusionale da implementare, pertanto si considera questo metodo.
Eventualmente controllare tale opzione durante il refactor'''

class CastleRights:
    def __init__(self, whiteKingSide, blackKingSide, whiteQueenSide, blackQueenSide):
        self.whiteKingSide = whiteKingSide
        self.blackKingSide = blackKingSide
        self.whiteQueenSide = whiteQueenSide
        self.blackQueenSide = blackQueenSide 



class Move(): #Nested class -> Move può stare dentro GameState
    #Mappatura dei valori sullo "standard" degli scacchi (di chess.com)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False): #Tutte le informazioni relative ad una mossa vengono definite e contenute qui
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        #Arrocco
        self.isCastleMove =  isCastleMove
        #ID Mossa
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
      

    '''
    Override equals __ -> indican l'override
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
            
    

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


