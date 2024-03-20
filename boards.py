import re

def find_lines_with_regex(filename, regex):
    return [line.strip() for line in open(filename) if re.match(regex, line)]


def rotate(board, n):
    if n == 0:
        return board
    elif n == 1:
        new = ""
        for i in reversed(range(6)):
            for j in range(6):
                new += board[j*6+i]
        return new
    elif n == 2:
        new = ""
        for j in reversed(range(6)):
            for i in reversed(range(6)):
                new += board[j*6+i]
        return new
    elif n == 3:
        new = ""
        for i in range(6):
            for j in reversed(range(6)):
                new += board[j*6+i]
        return new


def rotations(board):
    for n in range(4):
        yield n, rotate(board, n)


def main() -> int:
    user_board = input("enter board (lines all together, Fox, Gift, Sword, _empty, #blocked, .unknown): ")
    boards = None
    for r, b in rotations(user_board):
        boards = find_lines_with_regex("boards.txt", b)
        if boards:
            boards = [rotate(bb, r) for bb in boards]
            break

    if not boards:
        print("no matching board found")
        return 1

    print("possible boards:")
    for b in boards:
        print(b)

    best = [' ']*36
    for symbol in ('F', 'G', 'S'):
        if symbol in user_board:
            continue
        appearences = [0]*36
        for i in range(36):
            for board in boards:
                if board[i] == symbol or board[i] == 'F':  # Should probably also count F 
                    appearences[i] += 1
        indices = [i for i in range(len(appearences)) if appearences[i] == max(appearences)]
        for i in indices:
            if best[i] != ' ':
                best[i] += symbol
            else:
                best[i] = symbol

    print()
    print("Best squares for each symbol:")
    l = [best[i:i+6] for i in range(0, 36, 6)]
    print('\n'.join(''.join(ll) for ll in l))

    return 0


if __name__ == '__main__':
    exit(main())
