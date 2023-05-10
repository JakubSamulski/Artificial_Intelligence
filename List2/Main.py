from List2.GameServer import Server
from List2.Players import PlayerAI

player1 = PlayerAI(4,1)
player2 = PlayerAI(2, 2)

server = Server(player1, player2)
server.play()
