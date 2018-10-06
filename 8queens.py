# in case we want to look at particular position. for testing etc.
def visualize(position):
    print('-------------------')
    for i in range(8):
        print('| ',end='')
        for k in range(8):
            if complex((-7 + 2 * k), (7 - 2 * i)) in position:
                print('F ', end='')
            else:
                print('- ', end='')
        print('|')
    print('-------------------')
    return


# set of positions isomorphic to given 'position'
def symmetry_group(position):
    s90 = frozenset(point * 1j for point in position)
    s180 = frozenset(- point for point in position)
    s270 = frozenset(- point * 1j for point in position)
    m = frozenset(point.conjugate() for point in position)
    m90 = frozenset(point.conjugate() * 1j for point in position)
    m180 = frozenset(- point.conjugate() for point in position)
    m270 = frozenset(- point.conjugate() * 1j for point in position)
    return {position, s90, s180, s270, m, m90, m180, m270}


# removes points hit by a 'queen' from the 'free_points' set and returns new free set
def remove_hit_set(free_points, queen):
    free = free_points.copy()
    for point in free_points:
        h = (queen - point).real
        v = (queen - point).imag
        if h == 0 or v == 0 or h == v or h == -v:
            free.discard(point)
    return free


# tries to find n's queen in 'free_points' (not hitting previous 'already_placed').
# if num = 8, checks if we have a new solution. if so - put all isomorphic copies in 'legal_positions'
def find_queens(free_points, already_placed, n):
    global legal_positions
    global counter
    free = free_points.copy()
    already = already_placed.copy()
    new_queen = free.pop()
# next 4 lines - searching solutions with some other new_queen
    ex_this_queen = free.copy()
    ex_this_queen.discard(new_queen)
    if ex_this_queen:
        find_queens(ex_this_queen, already, n)
# now searching with this new_queen
    already.add(new_queen)
    if n == 8:
        candidate = frozenset(already)
        if candidate not in legal_positions:
            legal_positions |= symmetry_group(candidate)
            counter += 1
    else:
        free = remove_hit_set(free, new_queen)
        if free:
            find_queens(free, already, n + 1)
    return


# encoding "chessboard" as a lattice around 0 in complex plane,
# besides general fun, it will trivialize creating isomorphic copies of positions (= subsets of the board)
# h, v = horizontal and vertical coordinates of a point on the board
chessboard = set()
for h in range(4):
    for v in range(4):
        z = complex(1 + 2 * h, 1 + 2 * v)
        chessboard |= {z, - z, z * 1j, - z * 1j}
# the main result, set of legal positions of 8 queens. starts empty
legal_positions = set()
counter = 0

import time
start = time.time()
find_queens(chessboard, set(), 1)
print(f'total = {len(legal_positions)}\nnon-isomorphic = {counter}')
print(time.time() - start)
