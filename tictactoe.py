import keyboard
import time
import os
import copy
import sys
class Node():

    def __init__(self,state,moves=[],last_move=''):

        self.state=state
        self.moves=moves
        self.last_move=last_move

    def add_move(self,move):

        self.moves.append(move)

class Stack():

    def __init__(self):

        self.stack=[]

    def push(self,item):

        self.stack.append(item)

    def pop(self):

        if len(self.stack)==0:

            return "Empty"

        item=self.stack[-1]
        self.stack=self.stack[:-1]
        return item

class GameBoard():

    def __init__(self):

        self.Board=[[' ']*3 for i in range(3)]

    def Set(self,Value,Coords):

        if self.Board[Coords[0]][Coords[1]]!=' ':

            return False

        else:

            self.Board[Coords[0]][Coords[1]]=Value
            return True

    def GetFreePlaces(self):

        coords=[]

        for i in range(0,3):

            for c in range(0,3):

                if self.Board[i][c]==' ':

                    coords.append((i,c))

        return coords

    def PrintState(self):

        for i in range(0,3):

            for c in range(0,3):

                print(self.Board[i][c],end=' ')

            print()

    def GetState(self):

        for i in range(0,3):

            if (self.Board[i][0]==self.Board[i][1]) and (self.Board[i][1]==self.Board[i][2]):

                if self.Board[i][0]==' ':

                    return "Continue"

                return self.Board[i][0]+' Wins'

            elif (self.Board[0][i]==self.Board[1][i]) and (self.Board[1][i]==self.Board[2][i]):

                if self.Board[0][i]==' ':

                    return "Continue"

                return self.Board[0][i]+' Wins'

        if (self.Board[0][0]==self.Board[1][1]) and (self.Board[1][1]==self.Board[2][2]):

            if self.Board[0][0]!=' ':

                return self.Board[0][0]+' Wins'

        elif (self.Board[2][0]==self.Board[1][1]) and (self.Board[1][1]==self.Board[0][2]):

            if self.Board[2][0]!=' ':

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

def AI(Game):

    player_val='O'
    NodeStack=Stack()
    NodeStack.push(Node(state=Game,last_move='X'))
    win_states=[]
    draw_states=[]
    loss_states=[]

    while True:

        n=NodeStack.pop()

        if n=="Empty":

            break

        state=n.state.GetState()

        if state=='O'+" Wins":

            win_states.append(n)

        if state=='X'+' Wins':

            loss_states.append(n)

        if state=="Draw":

            draw_states.append(n)

        moves=n.state.GetFreePlaces()

        if n.last_move=='X':

            player_val='O'

        else:

            player_val='X'

        if len(moves)!=0:

            for m in moves:

                new_node=Node(copy.deepcopy(n.state),copy.deepcopy(n.moves),player_val)
                new_node.state.Set(player_val,m)
                new_node.add_move(m)
                NodeStack.push(copy.deepcopy(new_node))

    best_move=0
    cost=999999999999

    if len(win_states)>0:

        for i in range(0,len(win_states)):

            loss_risk=0

            if len(win_states)<100:

                for l in loss_states:

                    if l.moves[0]==win_states[i].moves[0]:

                        loss_risk=loss_risk+1

            current_cost=len(win_states[i].moves)+loss_risk

            if current_cost<cost:

                cost=current_cost
                best_move=i

        return win_states[best_move].moves[0]

    elif len(draw_states)>0:

        for i in range(0,len(draw_states)):

            loss_risk=0

            if len(win_states)<100:

                for l in loss_states:

                    if l.moves[0]==draw_states[i].moves[0]:

                        loss_risk=loss_risk+1

            current_cost=len(draw_states[i].moves)+loss_risk

            if current_cost<cost:

                cost=current_cost
                best_move=i

        return draw_states[best_move].moves[0]

    else:

        game_depth=0

        for i in range(0,len(loss_states)):

            if len(loss_states[i].moves) > game_depth:

                game_depth=len(loss_states[i].moves)
                best_move=i

        return loss_states[best_move].moves[0]


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

        except:

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
                    CPU_move=AI(Game)
                    os.system('cls')
                    Game.Set('O',CPU_move)
                    Game.PrintState()
                    print('You are '+player_val)

            time.sleep(0.5)

            State=Game.GetState()

            if State!='Continue':

                print(State)
                os.system('pause')
                return 0

        except KeyboardInterrupt:

            sys.exit()

        except KeyError:

            pass


if __name__=='__main__':

    mode=input('(1)Two Player\n(2)Vs CPU\n>')

    if mode=='1':

        two_player()

    if mode=='2':

        cpu()
