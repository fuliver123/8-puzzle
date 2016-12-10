from queue import PriorityQueue
import time


class State:
    def __init__(self, board, g, posmove, father):
        self.board = board
        self.g = g
        self.h = State.heuristicCalc(board)
        self.posmove = posmove
        self.father = father

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def isGoal(self):
        return self.board == [1, 2, 3, 4, 5, 6, 7, 8, 0]

    @staticmethod
    def heuristicCalc(board):
        x = (2, 0, 0, 0, 1, 1, 1, 2, 2)
        y = (2, 0, 1, 2, 0, 1, 2, 0, 1)
        temp_board = [[board[0], board[1], board[2]],
                      [board[3], board[4], board[5]],
                      [board[6], board[7], board[8]]]
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                sum += (abs(i - x[temp_board[i][j]]) + abs(j - y[temp_board[i][j]]))
        return sum

    @staticmethod
    def isLegal(board):
        before = set()
        if (len(board) != 9):
            return False
        for i in range(0, 9):
            if board[i] > 8 or board[i] < 0:
                return False
            if board[i] not in before:
                before.add(board[i])
            else:
                return False
        return True

    @staticmethod
    def move(board, direction):
        xdir = (0, 1, 0, -1)
        ydir = (1, 0, -1, 0)
        zeropos = board.index(0)
        xzero = int(zeropos / 3)
        yzero = int(zeropos % 3)
        temp_board = [[board[0], board[1], board[2]],
                      [board[3], board[4], board[5]],
                      [board[6], board[7], board[8]]]
        xtemp = xzero + xdir[direction]
        ytemp = yzero + ydir[direction]
        if xtemp > 2 or xtemp < 0 or ytemp > 2 or ytemp < 0:
            return False, -1, board
        temp = temp_board[xtemp][ytemp]
        temp_board[xtemp][ytemp] = temp_board[xzero][yzero]
        temp_board[xzero][yzero] = temp
        newboard = [temp_board[0][0],
                    temp_board[0][1],
                    temp_board[0][2],
                    temp_board[1][0],
                    temp_board[1][1],
                    temp_board[1][2],
                    temp_board[2][0],
                    temp_board[2][1],
                    temp_board[2][2]]
        return True, temp, newboard


def printBoard(board):
    temp_board = [[board[0], board[1], board[2]],
                  [board[3], board[4], board[5]],
                  [board[6], board[7], board[8]]]
    for i in range(0, 3):
        for j in range(0, 3):
            print(temp_board[i][j], end=" ")
        print()


def printResult(state):
    listmove = []
    while not state.father == None:
        listmove.append(state.posmove)
        state = state.father
    listmove.reverse()
    print("Đáp số gồm", len(listmove), "bước: ")
    print(listmove)


def aStar(state):
    queue = PriorityQueue()
    queue.put(state)
    visited = set()
    visited.add("".join(str(state.board)))
    while not queue.empty():
        state = queue.get()
        for i in range(0, 4):
            islegal, posmove, newboard = State.move(state.board, i)
            if islegal:
                if "".join(str(newboard)) not in visited:
                    visited.add("".join(str(newboard)))
                    newstate = State(newboard, state.g + 1, posmove, state)
                    queue.put(newstate)
                    if newstate.isGoal():
                        printResult(newstate)
                        return
    print("Bài toán không có lời giải.")


# Start here

while True:
    sboard = list(input("Nhập vào trạng thái xuất phát: "))
    board = []
    for i in sboard:
        board.append(int(i))
    if State.isLegal(board):
        break
    print("Bạn đã nhập không chính xác, nhập lại!")
print("Trạng thái xuất phát: ")
printBoard(board)
start_time = time.time()
aStar(State(board, 0, -1, None))
end_time = time.time()
print("Time:", end_time - start_time)
