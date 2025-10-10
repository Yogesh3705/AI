import heapq

class PuzzleState:
    def __init__(self, board, g, parent=None):
        self.board = board
        self.g = g  # cost so far
        self.h = self.misplaced()  # heuristic
        self.f = self.g + self.h
        self.parent = parent

    def misplaced(self):
        goal = [1,2,3,4,5,6,7,8,0]
        return sum(1 for i in range(9) if self.board[i] != 0 and self.board[i] != goal[i])

    def get_moves(self):
        neighbors = []
        idx = self.board.index(0)  # blank position
        row, col = divmod(idx, 3)
        directions = [(-1,0),(1,0),(0,-1),(0,1)]  # up,down,left,right
        for dr, dc in directions:
            r, c = row+dr, col+dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_idx = r*3+c
                new_board = self.board[:]
                new_board[idx], new_board[new_idx] = new_board[new_idx], new_board[idx]
                neighbors.append(PuzzleState(new_board, self.g+1, self))
        return neighbors

    def __lt__(self, other):
        return self.f < other.f  # for heapq ordering

def astar(start):
    goal = [1,2,3,4,5,6,7,8,0]
    open_list = []
    heapq.heappush(open_list, PuzzleState(start, 0))
    visited = set()

    while open_list:
        current = heapq.heappop(open_list)
        if current.board == goal:
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            return path[::-1]  # reversed path
        visited.add(tuple(current.board))
        for neighbor in current.get_moves():
            if tuple(neighbor.board) not in visited:
                heapq.heappush(open_list, neighbor)
    return None

# Example
start_state = [1,2,3,4,0,6,7,5,8]  # _ represents 0
solution = astar(start_state)
print("Moves to goal:", len(solution)-1)
for s in solution:
    for i in range(0,9,3):
        print(s[i:i+3])
    print()
