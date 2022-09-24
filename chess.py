"""
This program is coded by Alexander Zhan. This is a chess program with two methods of playing: single player vs computer or two players. 
If one player checkmates the other, the game ends. Each player is allowed one move per turn, if the move is illegal, tell the player that their move is illegal. 
If the move is legal, move the piece to the desired square, if there is an enemy piece on that square, capture the piece and display all the pieces captured 
by the player. If the move causes a check (The king is under attack), tell the player all their possible moves to stop the check. 
Rules of chess: https://en.wikipedia.org/wiki/Rules_of_chess 
"""


import math
import pip._vendor.requests
singlePlayer = False 

# INITIAL CHESS BOARD
row = "----------------------------------"
column8 = "8| ♖ | ♘ | ♗ | ♕ | ♔ | ♗ | ♘ | ♖ |     "
column7 = "7| ♙ | ♙ | ♙ | ♙ | ♙ | ♙ | ♙ | ♙ |     "
column6 = "6|   |   |   |   |   |   |   |   |     "
column5 = "5|   |   |   |   |   |   |   |   |     "
column4 = "4|   |   |   |   |   |   |   |   |     "
column3 = "3|   |   |   |   |   |   |   |   |     "
column2 = "2| ♟ | ♟ | ♟ | ♟ | ♟ | ♟ | ♟ | ♟ |     "
column1 = "1| ♜ | ♞ | ♝ | ♛ | ♚ | ♝ | ♞ | ♜ |     "

whitecastlingqueen = whitecastlingking = blackcastlingqueen = blackcastlingking = True
white_pieces = ["♜", "♞", "♝", "♛", "♚", "♟"]
black_pieces = ["♕", "♔", "♗", "♘", "♖", "♙"]

# DICTIONARY TO TRANSLATE PIECES TO THEIR NAMES
pieceNameDictionary = {
"♜":"rook",
"♞":"knight", 
"♝":"bishop",
"♛":"queen",
"♚":"king",
"♟":"white_pawn",
"♖":"rook",
"♘":"knight", 
"♗":"bishop",
"♕":"queen",
"♔":"king",
"♙":"black_pawn"}

whitePromotionPieceNameDictionary = {
"rook":"♜",
"knight":"♞", 
"bishop":"♝",
"queen":"♛",
}
blackPromotionPieceNameDictionary = {
"rook":"♖",
"knight":"♘", 
"bishop":"♗",
"queen":"♕",
}

white_captures = []
black_captures = []
recordedMoves = []

j = [column1, column2, column3, column4, column5, column6, column7, column8] # CREATE CHESS BOARD WITHOUT HORIZONTAL SEPERATORS

l = [
    row,"\n",j[7],"\n",row,"\n",j[6],"\n",row,"\n",j[5],"\n",row,"\n",j[4],"\n",row,"\n",j[3],"\n",row,"\n",j[2],"\n",row,"\n",j[1],"\n",row,"\n",j[0],"\n",row,"\n   a   b   c   d   e   f   g   h",
] # CREATE THE CHESS BOARD
print(''' 
\033[32m
 ██████╗██╗  ██╗███████╗███████╗███████╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
██║     ███████║█████╗  ███████╗███████╗
██║     ██╔══██║██╔══╝  ╚════██║╚════██║
╚██████╗██║  ██║███████╗███████║███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
 Rules of Chess:
 The King (♚ ) can move exactly one square horizontally, vertically, or diagonally. At most once in every game, each king is allowed to make a special move, known as castling.
 The Queen (♛ ) can move any number of vacant squares diagonally, horizontally, or vertically.
 The Rook (♜ ) can move any number of vacant squares vertically or horizontally. It also is moved while castling.
 The Bishop (♝ ) can move any number of vacant squares in any diagonal direction.
 The Knight (♞ ) can move one square along any rank or file and then at an angle. The knight´s movement can also be viewed as an “L” or “7″ laid out at any horizontal or vertical angle.
 The Pawns (♟ ) can move forward one square, if that square is unoccupied. If it has not yet moved, the pawn has the option of moving two squares forward provided both squares in front of the pawn are unoccupied. A pawn cannot move backward. Pawns are the only pieces that capture differently from how they move. They can capture an enemy piece on either of the two spaces adjacent to the space in front of them (i.e., the two squares diagonally in front of them) but cannot move to these spaces if they are vacant. The pawn is also involved in the two special moves en passant and promotion.
 \033[4m
 TO MOVE, ENTER THE STARTING SQUARE THAT YOUR PIECE IS ON FOLLOWED BY THE DESIRED SQUARE YOU WANT TO MOVE TO ON THE SAME LINE (eg. e2 e4, 0-0 for king side castle, 0-0-0 for queen side castle)
 
 See Here For all Rules: https://en.wikipedia.org/wiki/Rules_of_chess 
 \033[m\033[4m''')
while True:
  try:
    if int(input("How Many Players:\033[m "))==1: 
      singlePlayer = True
      break
    else: break
  except ValueError: pass

print("".join(l)) # PRINT THE INITIAL CHESSBOARD

dictionary = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    " ": 0,
    " ": 0,
}
letterList = ["a", "b", "c", "d", "e", "f", "g", "h", " ", " ", " "]
strNumberList = ["1", "2", "3", "4", "5", "6", "7", "8"]

def white_pawn(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # WHITE PAWN FUNCTION
  
  possibleAttackingSquares=[]
  possibleAttackingSquares.extend([f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])+1}", f"{letterList[dictionary[p1[0]]]} {int(p1[1])+1}"])

  for y in possibleAttackingSquares:
    try:
      if (int(y.split()[1]))<=0 or y.split()[0]==" " or y.split()[0].isdigit(): continue
      attackingSquares.append(y)
    except IndexError: continue

  if (j[int(p1[1])])[4 * dictionary[p1[0]] - 5] in black_pieces:
    possibleMovesList.append(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])+1}")
    possibleCaptures.append(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])+1}")

  if (j[int(p1[1])])[4 * dictionary[p1[0]] + 3] in black_pieces:

    possibleMovesList.append(f"{letterList[dictionary[p1[0]]]} {int(p1[1])+1}")
    possibleCaptures.append(f"{letterList[dictionary[p1[0]]]} {int(p1[1])+1}")
  try:
    if abs(int(lastMove[1]) - int(lastMove[3]))==2 and (pieceNameDictionary[(j[int(lastMove[3]) - 1])[4 * dictionary[lastMove[2]] - 1]]) == enemyPawn and f"{letterList[dictionary[lastMove[2]]-2]} {int(lastMove[3])}" == " ".join(p1[0:2]): 
      possibleMovesList.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])+1}")
      possibleCaptures.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])+1} EP")
  except IndexError: pass
  try:
    if abs(int(lastMove[1]) - int(lastMove[3]))==2 and (pieceNameDictionary[(j[int(lastMove[3]) - 1])[4 * dictionary[lastMove[2]] - 1]]) == enemyPawn and f"{letterList[dictionary[lastMove[2]]]} {int(lastMove[3])}" == " ".join(p1[0:2]): 
      possibleMovesList.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])+1}")
      possibleCaptures.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])+1} EP")
  except IndexError: pass
  if (j[int(p1[1])])[4 * dictionary[p1[0]] - 1] == " ":
    possibleMovesList.append(f"{p1[0]} {int(p1[1])+1}")
  else: return possibleMovesList,possibleCaptures,attackingSquares

  if p1[1] == "2":
      if (j[int(p1[1]) + 1])[4 * (dictionary[p1[0]])-1] == " ":
        possibleMovesList.append(f"{p1[0]} {int(p1[1])+2}")
  

  return possibleMovesList,possibleCaptures,attackingSquares

def black_pawn(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # BLACK PAWN FUNCTION
  possibleAttackingSquares=[]
  possibleAttackingSquares.extend([f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])-1}", f"{letterList[dictionary[p1[0]]]} {int(p1[1])-1}"])

  for y in possibleAttackingSquares:
    try:
      if (int(y.split()[1]))<=0 or y.split()[0]==" " or y.split()[0].isdigit(): continue
      attackingSquares.append(y)
    except IndexError: continue

  if (j[int(p1[1]) - 2])[4 * dictionary[p1[0]] - 5] in white_pieces:
    possibleMovesList.append(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])-1}")
    possibleCaptures.append(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])-1}")

  if (j[int(p1[1]) - 2])[4 * dictionary[p1[0]] + 3] in white_pieces:

    possibleMovesList.append(f"{letterList[dictionary[p1[0]]]} {int(p1[1])-1}")
    possibleCaptures.append(f"{letterList[dictionary[p1[0]]]} {int(p1[1])-1}")

  try:
    if (abs(int(lastMove[1]) - int(lastMove[3]))==2 and (pieceNameDictionary[(j[int(lastMove[3]) - 1])[4 * dictionary[lastMove[2]] - 1]]) == enemyPawn and f"{letterList[dictionary[lastMove[2]]-2]} {int(lastMove[3])}" == " ".join(p1[0:2])):
      
      possibleMovesList.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])-1}")
      possibleCaptures.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])-1} EP")
  except IndexError: pass
  try:
    if (abs(int(lastMove[1]) - int(lastMove[3]))==2 and (pieceNameDictionary[(j[int(lastMove[3]) - 1])[4 * dictionary[lastMove[2]] - 1]]) == enemyPawn and f"{letterList[dictionary[lastMove[2]]]} {int(lastMove[3])}" == " ".join(p1[0:2])): 
      
      possibleMovesList.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])-1}")
      possibleCaptures.append(f"{letterList[dictionary[lastMove[2]]-1]} {int(lastMove[3])-1} EP")
  except IndexError: pass

  if (j[int(p1[1]) - 2])[4 * dictionary[p1[0]] - 1] == " ":
    possibleMovesList.append(f"{p1[0]} {int(p1[1])-1}")
  else: return possibleMovesList,possibleCaptures,attackingSquares
  if p1[1] == "7":
      if (j[int(p1[1]) - 3])[4 * dictionary[p1[0]] - 1] == " ":
        possibleMovesList.append(f"{p1[0]} {int(p1[1])-2}")
  

  return possibleMovesList,possibleCaptures,attackingSquares

def bishop(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # BISHOP FUNCTION
  dur = dul = ddr = ddl = True
  
  possibleCaptures = []
  for i in range(1,8,1):
    try:
      if dur == True:
        if letterList[dictionary[p1[0]]+i-1]==" ": 

          dur = False
        else:
          position = (j[int(p1[1]) + i - 1])[(4 * (dictionary[p1[0]] + i)) - 1]
          if position in teamPieces:
            attackingSquares.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])+i}")
            dur = False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])+i}")
            dur = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])+i}")
    except IndexError:
          dur = False

    try:
      if dul == True:
        if letterList[dictionary[p1[0]]-i-1]==" ":dul = False
        elif int(p1[1])+i == 0: dul = False
        else:
          position = (j[int(p1[1]) + i - 1])[(4 * (dictionary[p1[0]] - i)) - 1]
          if position in teamPieces:
            attackingSquares.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])+i}")
            dul = False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])+i}")
            dul = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])+i}")
    except IndexError:
      dul=False


    try:
      if ddr == True:
        if letterList[dictionary[p1[0]]+i-1]==" ": ddr = False
        elif int(p1[1])-i == 0: ddr = False
          
        else:
          position = (j[int(p1[1]) - i - 1])[(4 * (dictionary[p1[0]] + i)) - 1]
          if position in teamPieces:
            attackingSquares.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])-i}")
            ddr = False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])-i}")
            ddr = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])-i}")
    except IndexError:
      ddr=False

    try:
      if ddl == True:
        if letterList[dictionary[p1[0]]-i-1]==" ": 

          ddl = False
        elif int(p1[1])-i <= 0: ddr = False
        else:
          position = (j[int(p1[1]) - i - 1])[(4 * (dictionary[p1[0]] - i)) - 1]
          if position in teamPieces:
            attackingSquares.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])-i}")
            ddl = False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])-i}")
            ddl = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])-i}")
    except IndexError:
      ddl=False

  return possibleMovesList,possibleCaptures,attackingSquares

def rook(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # ROOK FUNCTION
  du = dl = dr = dd = True
  
  possibleCaptures = []
  for i in range(1,8,1):
    try:
      if du == True:
        if letterList[dictionary[p1[0]]+i-1]==" ":du=False
        else:
          position = (j[int(p1[1]) - 1])[(4 * (dictionary[p1[0]] + i)) - 1]
          if position in teamPieces: 
            attackingSquares.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])}")
            du=False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])}")
         
            du = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]+i-1]} {int(p1[1])}")
    except IndexError: du = False
    try:
      if dd == True:
        if letterList[dictionary[p1[0]]-i-1]==" ":dd=False
        else:
          position = (j[int(p1[1]) - 1])[(4 * (dictionary[p1[0]] - i)) - 1]
          if position in teamPieces: 
            attackingSquares.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])}")
            dd=False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])}")
            dd = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-i-1]} {int(p1[1])}")
    except IndexError: dd = False
    try:
      if dr == True:
        if letterList[dictionary[p1[0]]-1]==" ": dr=False
        
        else:
          position = (j[int(p1[1]) + i - 1])[(4 * (dictionary[p1[0]])) - 1]
          if position in teamPieces: 
            attackingSquares.append(f"{letterList[dictionary[p1[0]]-1]} {int(p1[1])+i}")
            dr=False
          elif position in enemyPieces:
            for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-1]} {int(p1[1])+i}")
            dr = False
          else:
            for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-1]} {int(p1[1])+i}")

    except IndexError: dr = False

    try:
      if dl == True:
        if int(p1[1])-i > 0:
          if letterList[dictionary[p1[0]]-1]==" ": dl=False
          
          else:
            position = (j[int(p1[1]) - i - 1])[(4 * (dictionary[p1[0]])) - 1]
            if position in teamPieces: 
              attackingSquares.append(f"{letterList[dictionary[p1[0]]-1]} {int(p1[1])-i}")
              dl=False
            elif position in enemyPieces:
              for p in (possibleMovesList,possibleCaptures,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-1]} {int(p1[1])-i}")
              dl = False
            else: 
              for p in (possibleMovesList,attackingSquares):p.append(f"{letterList[dictionary[p1[0]]-1]} {int(p1[1])-i}")

    except IndexError: dl = False

  return possibleMovesList,possibleCaptures,attackingSquares

def queen(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # QUEEN FUNCTION
  possibleMoves = []
  possibleQueenCapture = []
  possibleAttackSquares = []
  possibleMoves.extend(rook(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn)[0])
  possibleMoves.extend(bishop(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn)[0])    

  possibleQueenCapture.extend(rook(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn)[1])
  possibleQueenCapture.extend(bishop(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn)[1])

  possibleAttackSquares.extend(rook(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn)[2])
  possibleAttackSquares.extend(bishop(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn)[2])

  return possibleMoves,possibleQueenCapture,possibleAttackSquares

def knight(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # KNIGHT FUNCTION
  knightMoves = []

 
  knightMoves.extend([(f"{letterList[dictionary[p1[0]]]} {int(p1[1])+2}"),(f"{letterList[dictionary[p1[0]]]} {int(p1[1])-2}"),(f"{letterList[dictionary[p1[0]]+1]} {int(p1[1])+1}"),(f"{letterList[dictionary[p1[0]]+1]} {int(p1[1])-1}"),(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])+2}"),(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])-2}"),(f"{letterList[dictionary[p1[0]]-3]} {int(p1[1])+1}"),(f"{letterList[dictionary[p1[0]]-3]} {int(p1[1])-1}")])
  
    
  for i in knightMoves:
    try:
      if (int(i.split()[1]))<=0 or i.split()[0]==" " or i.split()[0].isdigit(): continue
        
      if (j[int(i.split()[1]) - 1])[(4*dictionary[i.split()[0]])-1] in teamPieces: 
        attackingSquares.append(i)
        continue
      else: 
        for p in (possibleMovesList,attackingSquares):p.append(i)
        if (j[int(i.split()[1]) - 1])[(4*dictionary[i.split()[0]])-1] in enemyPieces:
          possibleCaptures.append(i)
    except IndexError:continue
  return possibleMovesList, possibleCaptures,attackingSquares

def checkProtectedSquares(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,protectedsquares,test,lastMove,enemyPawn): # FUNCTION TO CHECK ALL SQUARES THAT A CERTAIN SIDE IS PROTECTING 
  for i in range(len(j)):
        for h in range(len(test[i])):       
          if test[i][h] in enemyPieces:     
            piecePosition = (f"{letterList[math.trunc((h+1)/4-1)]} {i+1}").split()
            protectedsquares.extend(list(set(eval(f"{pieceNameDictionary[test[i][h]]}(piecePosition,possibleMovesList,possibleCaptures,{enemyPieces},{teamPieces},[],{test},lastMove,enemyPawn)[2]"))))

  return protectedsquares

def checkAllPossible(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,protectedsquares,test,lastMove,enemyPawn): # FUNCTION TO CHECK EVERY SINGLE POSSIBLE MOVE THAT A CERTAIN SIDE CAN MOVE
  for i in range(len(j)):
        for h in range(len(test[i])):
          if test[i][h] in enemyPieces:
            piecePosition = (f"{letterList[math.trunc((h+1)/4-1)]} {i+1}").split()
            a = eval(f"{pieceNameDictionary[test[i][h]]}(piecePosition,[],possibleCaptures,enemyPieces,teamPieces,[],test,lastMove,enemyPawn)[0]")
            if len(a)>0:
              protectedsquares[' '.join(piecePosition)]=a
              
  return protectedsquares

def king(p1,possibleMovesList,possibleCaptures,teamPieces,enemyPieces,attackingSquares,j,lastMove,enemyPawn): # KING FUNCTION
  kingMoves = []
  kingMoves.extend([(f"{letterList[dictionary[p1[0]]]} {int(p1[1])+1}"),(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])+1}"),(f"{letterList[dictionary[p1[0]]]} {int(p1[1])-1}"),(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])-1}"),(f"{p1[0]} {int(p1[1])+1}"),(f"{letterList[dictionary[p1[0]]]} {int(p1[1])}"),(f"{p1[0]} {int(p1[1])-1}"),(f"{letterList[dictionary[p1[0]]-2]} {int(p1[1])}")])
  for i in kingMoves:
    try:
      if (int(i.split()[1]))<=0 or i.split()[0]==" " or i.split()[0].isdigit(): 
        continue
      if (j[int(i.split()[1]) - 1])[(4*dictionary[i.split()[0]])-1] in teamPieces: 
        attackingSquares.append(i)
        continue
      else: 
        for p in (possibleMovesList,attackingSquares):p.append(i)
        if (j[int(i.split()[1]) - 1])[(4*dictionary[i.split()[0]])-1] in enemyPieces:
          possibleCaptures.append(i)
    except IndexError:continue

  return possibleMovesList, possibleCaptures,attackingSquares
  
def checkamte(test2,EL,enemyPieces,teamPieces,kingPiece,check,lastMove,enemyPawn): # FUNCTION TO CHECK IF A CHECKMATE HAS OCCURED
  protectedSquares=sorted(list(set(checkProtectedSquares([],[],[],teamPieces,enemyPieces,[],[],test2,lastMove,enemyPawn))))
  for ge in range(len(test2)):
    for he in range(len(test2[ge])):
      if test2[ge][he] == kingPiece and " ".join((f"{letterList[math.trunc((he+1)/4-1)]} {ge+1}").split()) in protectedSquares :
        check = True
        PossibleSquares=(checkAllPossible([],[],[],enemyPieces,teamPieces,[],{},test2,lastMove,enemyPawn))
        for i in range(len(PossibleSquares)):
          for t in range(len(PossibleSquares[list(PossibleSquares)[i]])):
            sim = []
            ts = (list(PossibleSquares)[i].split())
            
            pi = (j[int(ts[1]) - 1])[4 * dictionary[ts[0]] - 1]
            
            ts2 = (PossibleSquares[list(PossibleSquares)[i]][t].split())     
            for it in j:
              sim.append(it)
            v = list(sim[int(ts2[1]) - 1])
            v[4 * dictionary[ts2[0]] - 1] = pi
            sim[int(ts2[1]) - 1] = "".join(v)
            var = list(sim[int(ts[1]) - 1])
            var[4 * dictionary[ts[0]] - 1] = " "
            sim[int(ts[1]) - 1] = "".join(var)
            protectedSquares=sorted(list(set(checkProtectedSquares([],[],[],teamPieces,enemyPieces,[],[],sim,lastMove,enemyPawn))))
            for g in range(len(sim)):
              for h in range(len(sim[g])):
                if sim[g][h] == kingPiece:
                  if " ".join((f"{letterList[math.trunc((h+1)/4-1)]} {g+1}").split()) in protectedSquares:
                    continue
                  else: EL.append(f"{' '.join(ts)} → {' '.join(ts2)}")
  return EL,check

def castle(test,kingNew,rookNew,kingOld,rookOld,teamKing,teamRook,team,enemy,enemyPawn,square,addOrSubtract,rowNumber,squares,loop,numberofSquares): # FUNCTION TO CHECK IF A SIDE CAN CASTLE
  for i in range(1,loop,1):
    piece = eval(f"(j[rowNumber])[4 *(dictionary[square]{addOrSubtract})-1]")
    if i < numberofSquares:
      if piece in team:
        return False
      continue
    elif piece != teamKing: return False
    protectedSquares=sorted(list(set(checkProtectedSquares([],[],[],team,enemy,[],[],test,"",enemyPawn))))
    for ie in squares:
      if ie in protectedSquares: return False
    v = list(j[rowNumber])
    v[kingNew],v[rookNew] = teamKing,teamRook
    v[kingOld] = v[rookOld] = " "
    j[rowNumber] = "".join(v)
    l = [
    row,"\n",j[7],"\n",row,"\n",j[6],"\n",row,"\n",j[5],"\n",row,"\n",j[4],"\n",row,"\n",j[3],"\n",row,"\n",j[2],"\n",row,"\n",j[1],"\n",row,"\n",j[0],"\n",row,"\n   a   b   c   d   e   f   g   h",
    ]
    return l

    

def white_move(blackLastMove,whitecastlingking,whitecastlingqueen): # FUNCTION THAT EXECUTES WHEN IT IS THE WHITE SIDES TURN
  check = ENPASSANT = False
  test = []
  test2 = []
  EL = []
  for i in j:
    test.append(i)
    test2.append(i)

  ifCheck = checkamte(test2,EL,black_pieces,white_pieces,"♚",check,blackLastMove,"black_pawn")
  if ifCheck[1]:
    if (len(ifCheck[0])) == 0:
      return "CHECKMATE"
    else: 
      temp = list(set(ifCheck[0]))
      for je in range(len(temp)):print(temp[je],end=" | ")
  try:
    p1 = list(input("White Move: ").replace(" ","").lower())

    if "".join(p1)=="0-0":
      if whitecastlingking:
        ifCastle = castle(test,27,23,19,31,"♚","♜",white_pieces,black_pieces,"black_pawn",'h','-i',0, ["e 1","f 1", "g 1"],4,3)
        if ifCastle == False: return False
        else: 
          whitecastlingking = whitecastlingqueen = False
          return ("".join(ifCastle)),["e","1","g","1"],whitecastlingking,whitecastlingqueen,white_captures
      else: return False

    if "".join(p1)=="0-0-0":
      if whitecastlingqueen:
        ifCastle = castle(test,11,15,19,3,"♚","♜",white_pieces,black_pieces,"black_pawn",'a','+i',0, ["e 1","d 1","c 1","b 1"],5,4)
        if ifCastle == False: return False
        else: 
          whitecastlingking = whitecastlingqueen = False
          return ("".join(ifCastle)),["e","1","c","1"],whitecastlingking,whitecastlingqueen,white_captures
      else: return False

  
    piece = (j[int(p1[1]) - 1])[4 * dictionary[p1[0]] - 1]
  except ValueError: return False
  except KeyError: return False
  except IndexError: return False
  if piece not in white_pieces: return False
  else:
    global possibleMovesListt, possibleCaptures
    possibleMovesList = []
    possibleMovesListt = []
    possibleCaptures = []
  
    possibleMovesListt = sorted(list(set(eval(f"{pieceNameDictionary[piece]}(p1,possibleMovesList,possibleCaptures,white_pieces,black_pieces,[],j,blackLastMove,'black_pawn')[0]"))))
    possibleCaptures = sorted(eval(f"{pieceNameDictionary[piece]}(p1,possibleMovesList,possibleCaptures,white_pieces,black_pieces,[],j,blackLastMove,'black_pawn')[1]"))
    attackingSquares = sorted(list(set(eval(f"{pieceNameDictionary[piece]}(p1,possibleMovesList,possibleCaptures,white_pieces,black_pieces,[],j,blackLastMove,'black_pawn')[2]"))))


    if " ".join(p1[2:]) not in possibleMovesListt:return False
    else:

      v = list(test[int(p1[3]) - 1])
      v[4 * dictionary[p1[2]] - 1] = piece
      test[int(p1[3]) - 1] = "".join(v)
      var = list(test[int(p1[1]) - 1])
      var[4 * dictionary[p1[0]] - 1] = " "
      test[int(p1[1]) - 1] = "".join(var)
      protectedSquares=sorted(list(set(checkProtectedSquares([],[],[],white_pieces,black_pieces,[],[],test,blackLastMove,'black_pawn'))))
      for i in range(len(test)):
        for h in range(len(test[i])):
          if test[i][h] == "♚" and " ".join((f"{letterList[math.trunc((h+1)/4-1)]} {i+1}").split()) in protectedSquares :
            print("You are under check")
            return False

      for i in possibleCaptures:
        if " ".join(p1[2:]) == f"{i[0]} {i[2]}":
          if len(i.split())==3: 
            enpassant_square = i[0]
            ENPASSANT = True
            white_captures.append((j[int(p1[3]) - 2])[(4 * (dictionary[p1[2]])) - 1])
            (j[int(p1[3]) - 2])[(4 * (dictionary[p1[2]])) - 1] == " "
            break
          else:
            white_captures.append((j[int(p1[3]) - 1])[(4 * (dictionary[p1[2]])) - 1])
            break
      if pieceNameDictionary[piece]=="king":whitecastlingking = whitecastlingqueen = False
      elif "".join(p1[0:2])=="a1": whitecastlingqueen = False
      elif "".join(p1[0:2])=="h1": whitecastlingking = False
      if pieceNameDictionary[piece]=="white_pawn" and int(p1[3]) == 8: 
        while True:
          promotion = input("What piece would you like to promote to: ")
          if promotion in whitePromotionPieceNameDictionary: 
            piece = whitePromotionPieceNameDictionary[promotion]
            break
          else: print("That is not a valid piece")

      v = list(j[int(p1[3]) - 1])
      v[4 * dictionary[p1[2]] - 1] = piece
      j[int(p1[3]) - 1] = "".join(v)
      var = list(j[int(p1[1]) - 1])
      if ENPASSANT: var[4 * dictionary[p1[0]] - 1] = var[4 * dictionary[enpassant_square] - 1] = " "
      else:var[4 * dictionary[p1[0]] - 1] = " "
      j[int(p1[1]) - 1] = "".join(var)
      l = [
      row,"\n",j[7],"\n",row,"\n",j[6],"\n",row,"\n",j[5],"\n",row,"\n",j[4],"\n",row,"\n",j[3],"\n",row,"\n",j[2],"\n",row,"\n",j[1],"\n",row,"\n",j[0],"\n",row,"\n   a   b   c   d   e   f   g   h",
      ]

      
      return ("".join(l)),p1,whitecastlingking,whitecastlingqueen,white_captures

def black_move(whiteLastMove,blackcastlingking,blackcastlingqueen): # FUNCTION THAT EXECUTES WHEN IT IS THE BLACK SIDES TURN

    EL = []
    check = ENPASSANT = False
    test = []
    test2 = []
    for i in j:
      test.append(i)
      test2.append(i)

    ifCheck = checkamte(test2,EL,white_pieces,black_pieces,"♔",check,whiteLastMove,"white_pawn")
    if ifCheck[1]:
      if (len(ifCheck[0])) == 0:
        return "CHECKMATE"
      else: 
        for je in range(len(ifCheck[0])):print(ifCheck[0][je],end=" | ")
    try:
      if singlePlayer == False:
        p1 = list(input("Black Move: ").replace(" ","").lower())
      else:
        response = pip._vendor.requests.get(f"https://chess-api.herokuapp.com/next_best/{''.join(recordedMoves)}")
        p1 = response.json()["bestNext"].replace("e8g8","0-0").replace("e8c8","0-0-0")
        print(p1)
    
      if "".join(p1)=="0-0":
        if blackcastlingking:
          ifCastle = castle(test,27,23,19,31,"♔","♖",black_pieces,white_pieces,"white_pawn",'h','-i',7, ["e 8","f 8", "g 8"],4,3)
          if ifCastle == False: return False
          else: 
            blackcastlingking = blackcastlingqueen = False
            return ("".join(ifCastle)),["e","8","g","8"],blackcastlingking,blackcastlingqueen,black_captures
        else: return False

      if "".join(p1)=="0-0-0":
        if blackcastlingqueen:
          ifCastle = castle(test,11,15,19,3,"♔","♖",black_pieces,white_pieces,"white_pawn",'a','+i',7, ["e 8","d 8","c 8","b 8"],5,4)
          if ifCastle == False: return False
          else: 
            blackcastlingking = blackcastlingqueen = False
            return ("".join(ifCastle)),["e","8","c","8"],blackcastlingking,blackcastlingqueen,black_captures
        else: return False
      piece = (j[int(p1[1]) - 1])[4 * dictionary[p1[0]] - 1]
    except ValueError: return False
    except KeyError: return False
    except IndexError: return False
    if piece not in black_pieces: return False
    else:
      global possibleMovesListt, possibleCaptures
      possibleMovesList = []
      possibleMovesListt=  []
      possibleCaptures = []
    
      possibleMovesListt = sorted(list(set(eval(f"{pieceNameDictionary[piece]}(p1,possibleMovesList,possibleCaptures,black_pieces,white_pieces,[],j,whiteLastMove,'white_pawn')[0]"))))
      possibleCaptures = sorted(eval(f"{pieceNameDictionary[piece]}(p1,possibleMovesList,possibleCaptures,black_pieces,white_pieces,[],j,whiteLastMove,'white_pawn')[1]"))
      attackingSquares = sorted(list(set(eval(f"{pieceNameDictionary[piece]}(p1,possibleMovesList,possibleCaptures,black_pieces,white_pieces,[],j,whiteLastMove,'white_pawn')[2]"))))
      if " ".join(p1[2:]) not in possibleMovesListt:return False
      else:
        v = list(test[int(p1[3]) - 1])
        v[4 * dictionary[p1[2]] - 1] = piece
        test[int(p1[3]) - 1] = "".join(v)
        var = list(test[int(p1[1]) - 1])
        var[4 * dictionary[p1[0]] - 1] = " "
        test[int(p1[1]) - 1] = "".join(var)
        protectedSquares=sorted(list(set(checkProtectedSquares(p1,possibleMovesList,possibleCaptures,black_pieces,white_pieces,[],[],test,whiteLastMove,'white_pawn'))))
        for i in range(len(test)):
          for h in range(len(test[i])):
            if test[i][h] == "♔" and " ".join((f"{letterList[math.trunc((h+1)/4-1)]} {i+1}").split()) in protectedSquares :
              print("You are under check")
              return False

        
        for i in possibleCaptures:
          if " ".join(p1[2:]) == f"{i[0]} {i[2]}":
            if len(i.split())==3: 
              enpassant_square = i[0]
              ENPASSANT = True
              black_captures.append((j[int(p1[3])])[(4 * (dictionary[p1[2]])) - 1])
              break
            else:
              black_captures.append((j[int(p1[3]) - 1])[(4 * (dictionary[p1[2]])) - 1])
              break
        if pieceNameDictionary[piece]=="king":blackcastlingking = blackcastlingqueen = False
        elif "".join(p1[0:2])=="a1": blackcastlingqueen = False
        elif "".join(p1[0:2])=="h1": blackcastlingking = False
        if pieceNameDictionary[piece]=="black_pawn" and int(p1[3]) == 1: 
          while True:
            promotion = input("What piece would you like to promote to: ")
            if promotion in blackPromotionPieceNameDictionary: 
              piece = blackPromotionPieceNameDictionary[promotion]
              break
            else: print("That is not a valid piece")
        v = list(j[int(p1[3]) - 1])
        v[4 * dictionary[p1[2]] - 1] = piece
        j[int(p1[3]) - 1] = "".join(v)
        var = list(j[int(p1[1]) - 1])
        if ENPASSANT: var[4 * dictionary[p1[0]] - 1] = var[4 * dictionary[enpassant_square] - 1] = " "
        else:var[4 * dictionary[p1[0]] - 1] = " "
        j[int(p1[1]) - 1] = "".join(var)
        l = [
        row,"\n",j[7],"\n",row,"\n",j[6],"\n",row,"\n",j[5],"\n",row,"\n",j[4],"\n",row,"\n",j[3],"\n",row,"\n",j[2],"\n",row,"\n",j[1],"\n",row,"\n",j[0],"\n",row,"\n   a   b   c   d   e   f   g   h",
        ]
        return ("".join(l)),p1,blackcastlingking,blackcastlingqueen,black_captures
       
r="".join(l)
blackLastMove = ""
count = 0
while True: # LOOP THAT CONTROLS WHETHER IT IS WHITE SIDES TURN OR BLACK SIDES TURN, ALSO PRINTS NEW BOARD, RECORDS CAPTURES, PRINTS ILLEGAL MOVE (IF THE MOVE IS ILLEGAL)
    if count % 2 == 0:
        n = white_move(blackLastMove,whitecastlingking,whitecastlingqueen)
        if n == False:
          print("ILLEGAL MOVE")
          continue
        elif n == "CHECKMATE":
          print("CHECKMATE, BLACK WINS")
          break
        else:
          whiteLastMove = n[1]
          whitecastlingking,whitecastlingqueen = n[2],n[3]
          print("\n"+n[0])
          wc = list(filter((" ").__ne__, n[4]))
          if len(wc)>0:print(f"White Captures:{' '.join(wc)}")
          recordedMoves.append("".join(whiteLastMove))
          count += 1
    else:
        n = black_move(whiteLastMove,blackcastlingking,blackcastlingqueen)
        if n == False:
          print("ILLEGAL MOVE")
          continue
        elif n == "CHECKMATE":
          print("CHECKMATE, WHITE WINS")
          break
        else:
          blackcastlingking,blackcastlingqueen=n[2],n[3]
          blackLastMove = n[1]
          print("\n"+n[0])
          bc = list(filter((" ").__ne__, n[4]))
          if len(bc)>0:print(f"Black Captures:{' '.join(bc)}")
          recordedMoves.append("".join(blackLastMove))
          count += 1