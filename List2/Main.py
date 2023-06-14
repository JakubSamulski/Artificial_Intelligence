from List2.GameServer import Server
from List2.Players import PlayerAI, PlayerHuman
from Heuristics import basic_heuristic, mobility_heuristic, heuristic_amount_of_coins

player1 = PlayerAI(4,1,heuristic_amount_of_coins)

player2 = PlayerAI(4,2,heuristic_amount_of_coins)



server = Server(player1, player2)
server.play()
player1.print_times()
player2.print_times()
