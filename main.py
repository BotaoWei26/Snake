from snake_game import SnakeGame, DIRECTIONS

sg = SnakeGame(10)

sg.pretty_print()

while True:
    i = input()

    if i in DIRECTIONS.keys():
        sg.change_direction(i)
    else:
        sg.move_snake()

    sg.pretty_print()