from random import randint


def fill_the_matrix(x, y):
    mat = []
    for i in range(x):
        row = [randint(-9, 10) for _ in range(y)]
        mat.append(row)
    return mat


def print_matrix(mat):
    for i in mat:
        print(i)


def shift_the_matrix(x, y, s, direct, mat, mat_shift):
    if direct == 0 or direct == 1:
        if direct == 0:
            for i in range(x):
                for j in range(y):
                    mat_shift[i][j] = mat[i][(j + y - s) % y]

        if direct == 1:
            for i in range(x):
                for j in range(y):
                    mat_shift[i][j] = mat[(i + x - s) % x][j]

        print('Initial matrix: ')
        print_matrix(mat)

        print('Changed matrix:')
        print_matrix(mat_shift)
    else:
        print('Input error')


rows = int(input('Enter the number of rows - '))
columns = int(input('Enter the number of columns - '))
shift = int(input('Enter matrix shift - '))
direction = int(input('Enter shift direction(0 - to right, 1 - to down) - '))

shift = shift % columns if direction == 0 else shift % rows

matrix = fill_the_matrix(rows, columns)
matrix_shift = fill_the_matrix(rows, columns)

shift_the_matrix(rows, columns, shift, direction, matrix, matrix_shift)
