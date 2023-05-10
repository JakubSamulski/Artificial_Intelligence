import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

from reversi_engine import GameState, check_win, get_valid_moves, make_move


class Player(ABC):
    @abstractmethod
    def get_move(self, game_state: GameState) -> tuple[int, int]:
        pass

    @property
    @abstractmethod
    def player_id(self):
        pass


class PlayerHuman(Player):

    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def player_id(self):
        return self.player_id

    @player_id.setter
    def player_id(self, value):
        self._player_id = value

    def get_move(self, game_state: GameState) -> tuple[int, int]:
        col = int(input("Enter column: "))
        row = int(input("Enter row: "))
        return row, col



@dataclass
class Node:
    game_state: GameState
    children: list
    value: int = None
    move: (int, int) = None
    level: int = 0
    alfa: int = -math.inf
    beta = math.inf


class PlayerAI(Player):
    def __init__(self, max_level:int, player_id:int):
        self.max_level = max_level
        board = [[0] * 8 for _ in range(8)]
        board[3][3] = board[4][4] = 1
        board[3][4] = board[4][3] = 2
        self._player_id = player_id
        self.root = Node(GameState(board, 3 - self._player_id, ''), [], None, None, 0)

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, value):
        self._player_id = value

    def heuristic_amount_of_coins(self, board: list):
        count = 0
        for row in board:
            for field in row:
                if field == 2:
                    count += 1
        return count

    def generate_tree(self, root: Node, level):
        if root.level >= level:
            return
        if check_win(root.game_state) == -1:
            moves = get_valid_moves(root.game_state)
        else:
            return
        for move in moves:
            # print_board(root.game_state.board)
            gamestate_after = make_move(move[0], move[1], root.game_state)
            #print(root.level)
            root.children.append(Node(gamestate_after, [], None, move, root.level + 1))
            self.generate_tree(root.children[-1], self.max_level)

    def _mini_max(self, root: Node, heuristic_fn):
        if not root.children:
            root.value = heuristic_fn(root.game_state.board)
            return
        for child in root.children:
            self._mini_max(child, heuristic_fn)
        if root.game_state.current_player == self.player_id:
            root.value = max(child.value for child in root.children)
        elif root.game_state.current_player != self.player_id:
            root.value = min(child.value for child in root.children)

    def mini_max(self, root: Node, heuristic_fn):
        self._mini_max(root, heuristic_fn)
        for child in root.children:
            if child.value == root.value:
                root.move = child.move
                return

    def update_alfa_beta(self, node: Node):
        if node.game_state.current_player == self.player_id:
            if node.value > node.alfa:
                node.alfa = node.value
        elif node.game_state.current_player != self.player_id:
            if node.value < node.beta:
                node.beta = node.value

    def _alfa_beta(self, root: Node, heuristyc_fn):
        if not root.children:
            root.value = heuristyc_fn(root.game_state.board)
            self.update_alfa_beta(root)
            return

        for child in root.children:
            self._alfa_beta(child, heuristyc_fn)

        if root.game_state.current_player == self.player_id:
            root.value = max(child.value for child in root.children)
            root.alfa = max(root.value, root.alfa)
            root.beta = min(child.beta for child in root.children)


        elif root.game_state.current_player != self.player_id:
            root.value = min(child.value for child in root.children)
            root.beta = min(root.value, root.beta)
            root.alfa = max(child.alfa for child in root.children)
        if root.beta <= root.alfa:
           # print(f"skipping node at level {root.level}, alfa {root.alfa}, beta: {root.beta}")
            return

    def alfa_beta(self, root: Node, heuristic_fn):
        self._alfa_beta(root, heuristic_fn)
        root.move = None
        for child in root.children:
            if child.value == root.value and child.move in get_valid_moves(root.game_state):
                root.move = child.move
                return

    def get_move(self, game_state: GameState) -> tuple[int, int]:
        self.root = Node(game_state, [], None, None, 0)
        self.generate_tree(self.root, self.max_level)
        self.alfa_beta(self.root, self.heuristic_amount_of_coins)
        return self.root.move

