import re

DIMENSION = 6
TOTAL_SIZE = DIMENSION * DIMENSION


def find_lines_with_regex(filename: str, regex: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f if re.match(regex, line)]


def rotate(board: list[str], n: int) -> list[str]:
    if n == 0:
        return board
    elif n == 1:
        new = ""
        for i in reversed(range(DIMENSION)):
            for j in range(DIMENSION):
                new += board[j * DIMENSION + i]
        return new
    elif n == 2:
        new = ""
        for j in reversed(range(DIMENSION)):
            for i in reversed(range(DIMENSION)):
                new += board[j * DIMENSION + i]
        return new
    elif n == 3:
        new = ""
        for i in range(DIMENSION):
            for j in reversed(range(DIMENSION)):
                new += board[j * DIMENSION + i]
        return new
    else:
        raise Exception(f"bad rotate: {n}")


def rotate_opposite(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 3
    elif n == 2:
        return 2
    elif n == 3:
        return 1


def rotations(board: list[str]) -> tuple[int, list[str]]:
    for n in range(4):
        yield n, rotate(board, n)


def get_board_from_stdin() -> str:
    board = input(
        "enter board (lines all together, Fox, Gift, Sword, _empty, #blocked, .unknown): "
    )
    if len(board) != TOTAL_SIZE:
        raise Exception(f"bad size board, should be {TOTAL_SIZE} but is {len(board)}")
    if any(
        c != "F" and c != "G" and c != "S" and c != "_" and c != "#" and c != "."
        for c in board
    ):
        raise Exception("invalid characters in board")
    return board


def find_best_symbol_positions(
    boards: list[list[str]], user_board: list[str]
) -> list[str]:
    best = ["_"] * TOTAL_SIZE
    best_appearences = {}
    for symbol in ("F", "G", "S"):
        if symbol in user_board:
            continue
        appearences = [0] * TOTAL_SIZE
        for i in range(TOTAL_SIZE):
            for board in boards:
                if board[i] == symbol:
                    appearences[i] += 1
                    # +1 if F can also be there (and we are not F)
                    if symbol != "F" and board[i] == "F":
                        appearences[i] += 1
        indices = [
            i for i in range(len(appearences)) if appearences[i] == max(appearences)
        ]
        best_appearences[symbol] = max(appearences)
        for i in indices:
            if best[i] == "F" and symbol == "G":
                best[i] = "g"
            elif best[i] == "F" and symbol == "S":
                best[i] = "s"
            elif best[i] == "G" and symbol == "S":
                best[i] = "b"
            else:
                best[i] = symbol
    return best, best_appearences


def print_board(board, best_appearences):
    board2d = [board[i:i + DIMENSION] for i in range(0, TOTAL_SIZE, DIMENSION)]
    print("\n".join("".join(row) for row in board2d))
    for symbol, appearences in best_appearences.items():
        print(f"{symbol}={appearences}")


def main() -> int:
    try:
        user_board = get_board_from_stdin()
    except Exception as e:
        print(e)
        return 1

    boards = None
    for r, b in rotations(user_board):
        boards = find_lines_with_regex("boards.txt", b)
        if boards:
            # Make matching boards be rotated like the user's board
            boards = [rotate(bb, rotate_opposite(r)) for bb in boards]
            print(f"rotation={r}")
            break

    if not boards:
        print("no matching board found")
        return 1

    print("possible boards:")
    for b in boards:
        print(b)

    best, best_appearences = find_best_symbol_positions(boards, user_board)

    # add blocked tiles to output
    for i, s in enumerate(user_board):
        if s == "#":
            assert best[i] not in ("F", "G", "S"), "bug! best is in a wall!"
            best[i] = "#"

    print()
    print("Best squares for each symbol:")
    print_board(best, best_appearences)

    return 0


if __name__ == "__main__":
    exit(main())
