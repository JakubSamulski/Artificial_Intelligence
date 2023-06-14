from List2.reversi_engine import GameState, get_valid_moves


def heuristic_amount_of_coins(game_state: GameState):
    count = 0
    for row in game_state.board:
        for field in row:
            if field == game_state.current_player:
                count += 1
    return count


def basic_heuristic( games_state: GameState):
    weights = [[100, -20, 10, 5, 5, 10, -20, 100],
               [-20, -50, -2, -2, -2, -2, -50, -20],
               [10, -2, -1, -1, -1, -1, -2, 10],
               [5, -2, -1, -1, -1, -1, -2, 5],
               [5, -2, -1, -1, -1, -1, -2, 5],
               [10, -2, -1, -1, -1, -1, -2, 10],
               [-20, -50, -2, -2, -2, -2, -50, -20],
               [100, -20, 10, 5, 5, 10, -20, 100]]

    score = 0
    for i in range(len(games_state.board)):
        for j in range(len(games_state.board[i])):
            if games_state.board[i][j] == games_state.current_player:
                score += weights[i][j]
    return score


def mobility_heuristic( game_state: GameState):
    player_moves = len(get_valid_moves(game_state))
    game_state.current_player = 3 - game_state.current_player
    opponent_moves = len(get_valid_moves(game_state))
    score = player_moves - opponent_moves
    game_state.current_player = 3 - game_state.current_player
    return score
