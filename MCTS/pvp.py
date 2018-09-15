from Env import *
print("Welcome to tic-tac-toe pvp")
Board = Env()
Board.reset()
legal_input = [1, 2, 3, 4, 5, 6, 7, 8, 9]
legal_input = set(legal_input)

def parse_input():
    print("\n" + str(Board.player_turn()))
    while True:
        try:
            action = int(input("Choose from available moves: " + str(sorted(Board.legal_moves()))))
            if (action not in legal_input):
                print ("Illegal input")
                continue
            break
        except:
            print("Illegal input")
    legal_input.remove(action)
    return action

while(not Board.done):
    action = parse_input()
    Board.step(action)
    Board.render()

