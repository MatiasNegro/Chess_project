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
        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Aggiungo la mossa al log delle mosse definito in precedenza
        self.whiteToMove = not self.whiteToMove #Cambio del turno se era bianco ora tocca al nero e viceversa


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
    
    

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
