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
            ["--", "--", "bP", "--", "--", "--", "--", "--"],
            ["wP", "wP" ,"wP" ,"wP" ,"wP" ,"wP" ,"wP" ,"wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves,
                                'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
    
    '''
    Prende come parametro una mossa e la esegue (Non funziona per l'arrocco, promozione del pedone e en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Aggiungo la mossa al log delle mosse definito in precedenza
        self.whiteToMove = not self.whiteToMove #Cambio del turno se era bianco ora tocca al nero e viceversa

    #Torna indietro alla mossa eseguita prima di quella attuale
    def undoMove(self):
        if len(self.moveLog) != 0: #Controllo che il log delle mosse non sia vuoto
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #cambia il turno (a quello precedente)

    '''
    Mosse di controllo di scacco
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() 

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
            if c+1 <= 7: #Cattura a destra
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            pass

    '''
    Genero le mosse che una torre può fare in quella determinata posizione (riga, colonna) ed aggiungo tali mosse alla lista
    '''
    def getRookMoves(self,r, c, moves):
        pass

    def getKnightMoves(self,r, c, moves):
        pass

    def getBishopMoves(self,r, c, moves):
        pass

    def getQueenMoves(self,r, c, moves):
        pass

    def getKingMoves(self,r, c, moves):
        pass

class Move(): #Nested class -> Move può stare dentro GameState
    #Mappatura dei valori sullo "standard" degli scacchi (di chess.com)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board): #Tutte le informazioni relative ad una mossa vengono definite e contenute qui
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
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
