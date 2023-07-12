from random import randint


def fill_the_matrix(x, y):
    mat = []
    for i in range(x):
        row = [randint(-9, 10) for _ in range(y)]
        mat.append(row)
    return mat


def print_matrix(mat):
    print('Matrix:')
    for i in mat:
        print(i)


def count_columns_with_zeros(mat):
    columns_with_zero = 0
    for j in range(len(mat[0])):
        for i in range(len(mat)):
            if mat[i][j] == 0:
                columns_with_zero += 1
                break
    return columns_with_zero


def find_longest_series(mat):
    longest_series_row = -1
    max_series_length = 0
    for i in range(len(mat)):
        series_length = 1
        for j in range(1, len(mat[0])):
            if mat[i][j] == mat[i][j - 1]:
                series_length += 1
            else:
                if series_length > max_series_length:
                    max_series_length = series_length
                    longest_series_row = i + 1

                series_length = 1
        if series_length > max_series_length:
            max_series_length = series_length
            longest_series_row = i + 1

    if max_series_length > 1:
        return longest_series_row
    else:
        return 'Element series not found'


rows = int(input('Enter the number of rows - '))
columns = int(input('Enter the number of columns - '))
matrix = fill_the_matrix(rows, columns)
print_matrix(matrix)

count = count_columns_with_zeros(matrix)
print(f'Number of columns containing at least one zero element - {count}')

longest_series = find_longest_series(matrix)
print(f'Number of the row with the longest series of identical elements - {longest_series}')
