from dataclasses import dataclass
import copy


@dataclass
class GameState:
    board: list
    current_player: int
    error_message: str


def make_move(row: int, col: int, game_state: GameState):
    game_state_cp = copy.deepcopy(game_state)
    game_state_cp.board[row][col] = game_state_cp.current_player
    for d_row in range(-1, 2):
        for d_col in range(-1, 2):
            if d_row == 0 and d_col == 0:
                continue
            if is_valid_direction(row, col, d_row, d_col, game_state_cp):
                flip_direction(row, col, d_row, d_col, game_state_cp)
    game_state_cp.current_player = 3 - game_state_cp.current_player
    return game_state_cp


# -1: no winner
# 0 - tie
# 1 - player1
# 2 - player2

def check_win(game_state: GameState):
    game_state_cp = copy.deepcopy(game_state)
    if not get_valid_moves(game_state_cp):
        game_state_cp.current_player = 3 - game_state_cp.current_player
        if not get_valid_moves(game_state_cp):
            counts = [0, 0, 0]
            for row in range(8):
                for col in range(8):
                    counts[game_state_cp.board[row][col]] += 1
            if counts[1] > counts[2]:
                return 1
            elif counts[2] > counts[1]:
                return 2
            else:
                return 0
        return -1
    return -1


def is_valid_direction(row, col, d_row, d_col, game_state: GameState):
    opponent = 3 - game_state.current_player
    r, c = row + d_row, col + d_col
    if r < 0 or r >= 8 or c < 0 or c >= 8 or game_state.board[r][c] != opponent:
        return False
    while 0 <= r < 8 and 0 <= c < 8:
        if game_state.board[r][c] == 0:
            return False
        if game_state.board[r][c] == game_state.current_player:
            return True
        r, c = r + d_row, c + d_col
    return False


def flip_direction(row, col, d_row, d_col, game_state):
    r, c = row + d_row, col + d_col
    while game_state.board[r][c] != game_state.current_player:
        game_state.board[r][c] = game_state.current_player
        r, c = r + d_row, c + d_col


def get_valid_moves(game_state):
    moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(row, col, game_state):
                moves.append((row, col))
    return moves


def is_valid_move(row, col, game_state):
    if game_state.board[row][col] != 0:
        return False
    for d_row in range(-1, 2):
        for d_col in range(-1, 2):
            if d_row == 0 and d_col == 0:
                continue
            if is_valid_direction(row, col, d_row, d_col, game_state):
                return True
    return False


# def get_winner():
#     counts = [0, 0, 0]
#     for row in range(8):
#         for col in range(8):
#             counts[game_state.board[row][col]] += 1
#     if counts[1] > counts[2]:
#         return 1
#     elif counts[2] > counts[1]:
#         return 2
#     else:
#         return 0

def print_board(board):
    print("   0 1 2 3 4 5 6 7 ")
    print("  +-+-+-+-+-+-+-+-+")
    for row in range(8):
        print(row, end=" |")
        for col in range(8):
            if board[row][col] == 0:
                print(" ", end="|")
            elif board[row][col] == 1:
                print("X", end="|")
            else:
                print("O", end="|")
        print("\n  +-+-+-+-+-+-+-+-+")


def test():
    print_board(game_state.board)
    print(get_valid_moves())
    print(game_state.current_player)
    print(is_valid_move(2, 4))
    game_state = make_move(2, 4, game_state)

    print_board(game_state.board)
    print(get_valid_moves())
    print(game_state.current_player)
    print(is_valid_move(2, 4))
    game_state = make_move(2, 4, game_state)
    print_board(game_state.board)


if __name__ == "__main__":
    test()
