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


def count_rows_without_zeros(mat):
    rows_without_zeros = 0
    for i in mat:
        if 0 not in i:
            rows_without_zeros += 1
    return rows_without_zeros


def find_max_duplicate(mat):
    flat_matrix = []
    for i in mat:
        for j in i:
            flat_matrix.append(j)

    counts = {}

    for i in flat_matrix:
        counts[i] = counts.get(i, 0) + 1

    duplicate = max([i for i, j in counts.items() if j > 1])
    return duplicate


rows = int(input('Enter the number of rows - '))
columns = int(input('Enter the number of columns - '))
matrix = fill_the_matrix(rows, columns)
print_matrix(matrix)

count = count_rows_without_zeros(matrix)
print(f'The number of rows containing no null elements - {count}')

max_duplicate = find_max_duplicate(matrix)
print(f'Maximum of the numbers occurring more than once in the matrix - {max_duplicate}')
