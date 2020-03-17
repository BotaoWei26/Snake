import socket

with socket.socket() as s:
    s.bind(('localhost', 9999))

    s.listen(2)
    print("waiting for connections...")

    player1, addr1 = s.accept()
    print("player1 is connected on: ", addr1)

    player2, addr2 = s.accept()
    print("player2 is connected on: ", addr2)

    player1.send(bytes("set","utf-8"))
    player2.send(bytes("set","utf-8"))
    while True:
        board1 = player1.recv(1024)
        board2 = player2.recv(1024)
        if board1.decode() == "over" or board2.decode() == "over":
            player1.send(bytes("over","utf-8"))
            player2.send(bytes("over","utf-8"))
        else:
            player1.send(board2)
            player2.send(board1)
