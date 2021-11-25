def check_n_queens(checked,N):
    list = []
    for check in checked:
        row = int(int(check)/N)
        col = int(check)%N
        for r,c in list:
            if row == r or col == c or abs(row-r) == abs(col-c):
                return 0
        list.append(tuple([row,col]))

    return 1


      