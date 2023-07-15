from random import randint


def calculate_shift(x, y):
    s = int(input('Enter matrix shift - '))
    direct = int(input('Enter shift direction(0 - to right, 1 - to down) - '))

    return s % y if not direct else s % x, direct


def fill_the_matrix(x, y):
    return [[randint(-9, 10) for _ in range(y)] for _ in range(x)]


def print_matrix(mat):
    for i in mat:
        print(i)


def validate_direction(direct):
    return direct in (0, 1)


def shift_the_matrix(x, y, s, direct, mat, mat_shift):
    if validate_direction(direct):
        for i in range(x):
            for j in range(y):
                mat_shift[i][j] = mat[i][(j + y - s) % y] if direct == 0 else mat[(i + x - s) % x][j]

        print('Initial matrix: ')
        print_matrix(mat)

        print('Changed matrix:')
        print_matrix(mat_shift)
    else:
        print('Input error')


rows = int(input('Enter the number of rows - '))
columns = int(input('Enter the number of columns - '))
shift, direction = calculate_shift(rows, columns)

matrix = fill_the_matrix(rows, columns)
matrix_shift = fill_the_matrix(rows, columns)

shift_the_matrix(rows, columns, shift, direction, matrix, matrix_shift)
