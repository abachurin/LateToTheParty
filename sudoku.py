def solve(board):
    from copy import deepcopy
    # convention in the program is: j - row, i - column

    def print_cands(cands):
        for j in range(9):
            for i in range(9):
                if len(cands[j][i]) == 1:
                    print(sum(cands[j][i]), end=' ')
                else:
                    print('0', end=' ')
            print()
        print('-----------------')
        return

    def cand_list(board, j, i):
        if board[j][i] != 0:
            return {board[j][i]}
        set_row = set(board[j])
        set_col = {board[row][i] for row in range(9)}
        j_sec = j // 3 * 3
        i_sec = i // 3 * 3
        set_sect = {board[r][c] for c in range(i_sec, i_sec + 3) for r in range(j_sec, j_sec + 3)}
        return set(range(1, 10)) - (set_row | set_col | set_sect) | {0}

    def suggest_cand(cands, j, i, x):
        trial = deepcopy(cands)
        for c in range(9):
            if c != i:
                trial[j][c].discard(x)
                if trial[j][c] == {0}:
                    return False
        for r in range(9):
            if r != j:
                trial[r][i].discard(x)
                if trial[r][i] == {0}:
                    return False
        j_sec = j // 3 * 3
        i_sec = i // 3 * 3
        for c in range(i_sec, i_sec + 3):
            for r in range(j_sec, j_sec + 3):
                if r != j and c != i:
                    trial[r][c].discard(x)
                    if trial[r][c] == {0}:
                        return False
        trial[j][i] = {x}
        return trial

    def solve_cands(cands):
        pivot_row = pivot_col = 0
        var = 10
        for j in range(9):
            for i in range(9):
                if not cands[j][i]:
                    return False
                if 1 < len(cands[j][i]) < var:
                    pivot_row, pivot_col = j, i
                    var = len(cands[j][i])
        if var == 10:
            return cands
        for x in (cands[pivot_row][pivot_col] - {0}):
            trial = suggest_cand(cands, pivot_row, pivot_col, x)
            if not trial:
                return False
            solution = solve_cands(trial)
            if solution:
                return solution
        return False

    cands = [[cand_list(board, j, i) for i in range(9)] for j in range(9)]
    result = solve_cands(cands)
    if not result:
        return 'no solution'
    answer = [[sum(result[j][i]) for i in range(9)] for j in range(9)]
    return answer
