from List2.reversi_engine import GameState, check_win, make_move, print_board, get_valid_moves

from Players import PlayerHuman, PlayerAI, Player


class Server:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        board = [[0 for _ in range(8)] for _ in range(8)]
        board[3][3] = board[4][4] = 1
        board[3][4] = board[4][3] = 2

        self.game_state = GameState(board, 1, '')

    def play(self):
        while (winner:= check_win(self.game_state)) == -1:

            print_board(self.game_state.board)
            print("Player {}'s turn".format(self.game_state.current_player))
            print(f"Valid moves: {get_valid_moves(self.game_state)}")

            if self.game_state.current_player == 1:
                self.make_move(self.player1)

            else:
                self.make_move(self.player1)



        print("Game over!")
        print("Player {} won!".format(winner) if winner != 0 else "Tie!")

    def make_move(self,player:Player):
        move = player.get_move(self.game_state)
        if move is None:
            print("Player {} passed".format(self.game_state.current_player))
            self.game_state = GameState(self.game_state.board, 3 - self.game_state.current_player, '')
            return
        self.game_state = make_move(move[0], move[1], self.game_state)
        print(f"Moved {move}, message {self.game_state.error_message}")


