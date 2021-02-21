import keyboard
import time
import os
import copy
import sys

recursions=0

class GameBoard():

    def __init__(self):

        self.Board=[['_']*3 for i in range(3)]

    def Set(self,Value,Coords):

        if self.Board[Coords[0]][Coords[1]]!='_':

            return False

        else:

            self.Board[Coords[0]][Coords[1]]=Value
            return True

    def GetFreePlaces(self):

        coords=[]

        for i in range(0,3):

            for c in range(0,3):

                if self.Board[i][c]=='_':

                    coords.append((i,c))

        return coords

    def PrintState(self):

        for i in range(0,3):

            for c in range(0,3):

                print(self.Board[i][c],end=' ')

            print()

    def GetState(self):

        for i in range(0,3):

            if self.Board[0][2]==self.Board[1][2]==self.Board[2][2]=='X':

                return 'X Wins'

            if self.Board[2][0]==self.Board[2][1]==self.Board[2][2]=='X':

                return 'X Wins'

            if self.Board[0][2]==self.Board[1][2]==self.Board[2][2]=='O':

                return 'O Wins'

            if self.Board[2][0]==self.Board[2][1]==self.Board[2][2]=='O':

                return 'O Wins'

            if (self.Board[i][0]==self.Board[i][1]) and (self.Board[i][1]==self.Board[i][2]):

                if self.Board[i][0]=='_':

                    return "Continue"

                return self.Board[i][0]+' Wins'

            elif (self.Board[0][i]==self.Board[1][i]) and (self.Board[1][i]==self.Board[2][i]):

                if self.Board[0][i]=='_':

                    return "Continue"

                return self.Board[0][i]+' Wins'

        if (self.Board[0][0]==self.Board[1][1]) and (self.Board[1][1]==self.Board[2][2]):

            if self.Board[0][0]!='_':

                return self.Board[0][0]+' Wins'

        elif (self.Board[2][0]==self.Board[1][1]) and (self.Board[1][1]==self.Board[0][2]):

            if self.Board[2][0]!='_':

                return self.Board[2][0]+' Wins'

        elif len(self.GetFreePlaces())==0:

            return "Draw"

        return "Continue"

KeyCoordinateMap={
    'q':(0,0),
    'w':(0,1),
    'e':(0,2),
    'a':(1,0),
    's':(1,1),
    'd':(1,2),
    'z':(2,0),
    'x':(2,1),
    'c':(2,2)
}

player_bool={'X':True,'O':False}

def minimax(Game,player):

    global recursions

    recursions=recursions+1

    state=Game.GetState()

    if state[0]=='X':

        return 10

    if state[0]=='O':

        return -10

    if state=='Draw':

        return 0

    moves=Game.GetFreePlaces()

    scores=[]

    for m in moves:

        New=copy.deepcopy(Game)
        if player=='X':
            New.Set('X',m)
            scores.append(minimax(copy.deepcopy(New),'O'))
        else:
            New.Set('O',m)
            scores.append(minimax(copy.deepcopy(New),'X'))

    if player=='X':

        return max(scores)

    else:

        return min(scores)


def AI(Game,cpu_player):

    global recursions

    recursions=0

    if cpu_player=='O':

        best_score=999999999999999999

    else:

        best_score=-9999999999999999

    moves=Game.GetFreePlaces()

    for m in moves:

        New=copy.deepcopy(Game)

        New.Set(cpu_player,m)

        score=minimax(copy.deepcopy(New),'X')

        if cpu_player=='O':

            if score<best_score:

                best_score=score
                best_move=m

        else:

            if score>best_score:

                best_score=score
                best_move=m

    return best_move

def two_player():

    Game=GameBoard()
    player_val='X'
    Game.PrintState()
    print(player_val+' turn')

    while True:

        KeyPressed=keyboard.read_key()

        try:

            IsSet=Game.Set(player_val,KeyCoordinateMap[KeyPressed])
            if IsSet:
                os.system('cls')
                Game.PrintState()
                if player_val=='O':

                    player_val='X'

                elif player_val=='X':

                    player_val='O'

                print(player_val+' turn')
            time.sleep(0.5)

            State=Game.GetState()

            if State!='Continue':

                print(State)
                os.system('pause')
                return 0

        except KeyError:

            pass

def cpu():

    Game=GameBoard()
    player_val='X'
    Game.PrintState()
    print('You are '+player_val)

    while True:

        KeyPressed=keyboard.read_key()

        try:

            IsSet=Game.Set(player_val,KeyCoordinateMap[KeyPressed])
            if IsSet:
                os.system('cls')
                Game.PrintState()
                print('You are '+player_val)
                State=Game.GetState()
                if State=='Continue':
                    CPU_move=AI(Game,'O')
                    os.system('cls')
                    f.write(str(recursions)+'\n')
                    Game.Set('O',CPU_move)
                    Game.PrintState()
                    print('You are '+player_val)

            time.sleep(0.5)

            State=Game.GetState()

            if State!='Continue':

                print(State)
                return 0

        except KeyboardInterrupt:

            sys.exit()

        except KeyError:

            pass


if __name__=='__main__':

    f=open('recursions.txt','a')

    mode=input('(1)Two Player\n(2)Vs CPU\n>')

    os.system('cls')

    if mode=='1':

        two_player()

    if mode=='2':

        cpu()

    f.write('\n')

    f.close()
