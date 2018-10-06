from copy import deepcopy
import random
import time


def random_puzzle(n):
    per = list(range(n * n))
    random.shuffle(per)
    arr = []
    for i in range(n):
        line = []
        for j in range(n):
            line.append(per[i * n + j])
        arr.append(line)
    return arr


def ex_upper_row(arr):
    w = len(arr[0])
    sli = arr[1:]
    for i in range(len(sli)):
        for j in range(w):
            if sli[i][j]:
                sli[i][j] -= w
    return sli


def transpose(stripe):

    def change(n, w):
        if n <= w:
            return n * 2
        return (n - w) * 2 - 1

    w = len(stripe[0])
    col = []
    for i in range(w):
        col.append([change(stripe[1][i], w), change(stripe[0][i], w)])
    return col


def grid(arr, pos):
    if pos[0] == len(arr) - 1 and pos[1] == len(arr[0]) - 1:
        return 0
    else:
        return pos[0] * len(arr[0]) + pos[1] + 1

def check_parity(arr):
    residue = list(range(len(arr) * len(arr[0])))
    even_cycle = True
    while residue:
        i = residue[0]
        i_next = i
        cycle = 0
        while True:
            i_next = grid(arr, find_tile(arr, i_next))
            residue.remove(i_next)
            cycle += 1
            if i_next == i:
                break
        if cycle % 2 == 0:
            even_cycle = not even_cycle
    zp = find_tile(arr, 0)
    taxi = (zp[0] + zp[1]) % 2
    return (even_cycle + taxi) % 2


def print_board(arr):

    def stri(tile):
        if tile < 10:
            return str(tile) + ' '
        else:
            return str(tile)

    print('--------------------')
    for line in arr:
        print('| ', '  '.join(stri(tile) for tile in line), ' |')
    print('--------------------')
    return

def check_solution(arr):
    import itertools
    size = len(arr) * len(arr[0])
    our = list(itertools.chain(*arr))
    etal = list(range(size))[1:]
    etal.append(0)
    return our == etal

def represent(arr, seq):
    tile_moves = []
    h = len(arr)
    w = len(arr[0])
    for move in seq:
        zp = find_tile(arr, 0)
        np = (zp[0] + move[0], zp[1] + move[1])
        tile_moves.append(arr[np[0]][np[1]])
        arr[zp[0]][zp[1]], arr[np[0]][np[1]] = arr[np[0]][np[1]], arr[zp[0]][zp[1]]
    return tile_moves


def find_tile(arr, n):
    h = len(arr)
    w = len(arr[0])
    for i in range(h):
        for j in range(w):
            if arr[i][j] == n:
                return i, j


def get_zero(arr, cp):
    h = len(arr)
    w = len(arr[0])
    seq = []
    zp = find_tile(arr, 0)
    if cp[0] == 0:
        if zp[0] == 0:
            seq.extend([left] * (zp[1] - cp[1] - 1) if zp[1] > cp[1] else [right] * (cp[1] - zp[1]))
        else:
            if zp[1] == cp[1]:
                seq.append(left)
                seq.extend([up] * zp[0])
                seq.append(right)
            elif zp[1] > cp[1]:
                seq.extend([up] * zp[0])
                seq.extend([left] * (zp[1] - cp[1] - 1))
            else:
                seq.extend([right] * (cp[1] - zp[1] - 1))
                seq.extend([up] * zp[0])
                seq.append(right)
    else:
        if zp[0] != cp[0]:
            fix = (1 if zp[1] == cp[1] else 0)
            seq.extend([up] * (zp[0] - cp[0] - fix) if zp[0] > cp[0] else [down] * (cp[0] - zp[0] - fix))
        if zp[1] != cp[1]:
            seq.extend([left] * (zp[1] - cp[1] - 1) if zp[1] > cp[1] else [right] * (cp[1] - zp[1]))
        else:
            if zp[1] == w - 1:
                if zp[0] < cp[0]:
                    seq.extend([left, down, right])
                else:
                    seq.extend([left, up, right])
            else:
                if zp[0] < cp[0]:
                    seq.extend([right, down])
                else:
                    seq.extend([right, up])
        if cp[0] == h - 1:
            seq.extend([up, left, down, right, up])
    return seq


def fill_upper_row(arr):
    w = len(arr[0])
    seq_total = []
    curr = 1
    while curr < w:
        cp = find_tile(arr, curr)
        if grid(arr, cp) == curr:
            curr += 1
            continue
        seq = get_zero(arr, cp)
        represent(arr, seq)
        seq_total.extend(seq)
        seq = []
        cp = find_tile(arr, curr)
        if grid(arr, cp) == curr:
            curr += 1
            continue
        if cp[1] < curr - 1:
            seq.extend([left, down, right, right, up] * (curr - 1 - cp[1]))
        if cp[1] > curr - 1:
            seq.extend([down, left, left, up, right] * (cp[1] - curr + 1))
        seq.extend([up, left, down, right, up] * cp[0])
        represent(arr, seq)
        seq_total.extend(seq)
        curr += 1
    cp = find_tile(arr, curr)
    if grid(arr, cp) == curr:
        return seq_total
    zp = find_tile(arr, 0)
    if grid(arr, zp) == curr and grid(arr, cp) == curr + w:
        seq_total.append(down)
        return seq_total
    seq = get_zero(arr, cp)
    represent(arr, seq)
    seq_total.extend(seq)
    seq = []
    cp = find_tile(arr, curr)
    if cp[1] < curr - 2:
        seq.extend([left, down, right, right, up] * (curr - 2 - cp[1]))
    seq.extend([up, left, down, right, up] * (cp[0] - 1))
    seq.extend([down, left, up, right, up, left, down, down, right, up, left, up, right, down])
    represent(arr, seq)
    seq_total.extend(seq)
    return seq_total


def solve22(arr):
    zp = find_tile(arr, 0)
    if zp == (0, 1):
        if arr[0][0] == 1:
            return [right, down]
        if arr[0][0] == 4:
            return [right, down, left, up, right, down]
        if arr[0][0] == 2:
            return [down, right]
    if zp == (1, 1):
        seq = [left]
        corr = [up]
    if zp == (1, 0):
        seq = [up, left]
        corr = [up, right]
    if zp == (0, 0):
        seq = [up]
        corr = [right]
    represent(arr, corr)
    seq.extend(solve22(arr))
    return seq


def solver(start):
    arr = deepcopy(start)
    if not check_parity(arr):
        return None
    h = len(arr) - 3
    seq_total = fill_upper_row(arr)
    while h > 0:
        arr = ex_upper_row(arr)
        seq_total.extend(fill_upper_row(arr))
        h -= 1
    turn = {up: left, left: down, down: right, right: up}
    arr = transpose(ex_upper_row(arr))
    h = len(arr) - 2
    for _ in range(h):
        seq = fill_upper_row(arr)
        seq_real = [turn[move] for move in seq]
        seq_total.extend(seq_real)
        arr = ex_upper_row(arr)
    seq_total.extend(solve22(arr))
    return seq_total


def slide_puzzle(ar):
    seq = solver(ar)
    if seq:
        return represent(ar, seq)
    return None



up, left, down, right = (-1, 0), (0, -1), (1, 0), (0, 1)
moves_repr = {up: 'up', left: 'left', down: 'down', right: 'right'}

starting_array = [
    [15,    11,    8,    0],
    [3,     1,     2,    14],
    [6,     7,    5,     10],
    [9,     12,     13,    4],
]

'''
x = deepcopy(starting_array)

seq = solver(starting_array)
print_board(starting_array)
represent(x, seq)
print_board(x)
'''

n = 3
c = 0
fail = 0
start = time.time()
for i in range(10):
    x = random_puzzle(n)
    print_board(x)
    seq = slide_puzzle(x)
    print(seq)
    if seq:
        if not check_solution(x):
            fail += 1

        c += 1
print(c, fail)
print(time.time() - start)
