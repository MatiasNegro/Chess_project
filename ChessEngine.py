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