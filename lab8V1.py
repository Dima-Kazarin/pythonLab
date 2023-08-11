from random import randint


def fill_the_matrix(x, y):
    return [[randint(-9, 10) for _ in range(y)] for _ in range(x)]


def print_matrix(mat):
    print('Matrix:')
    for i in mat:
        print(i)


def count_rows_without_zeros(mat):
    return sum(1 for i in mat if 0 not in i)


def find_max_duplicate(mat):
    flat_matrix = [j for i in mat for j in i]
    counts = {i: flat_matrix.count(i) for i in flat_matrix}

    return max([i for i, j in counts.items() if j > 1])


rows = int(input('Enter the number of rows - '))
columns = int(input('Enter the number of columns - '))
matrix = fill_the_matrix(rows, columns)
print_matrix(matrix)

count = count_rows_without_zeros(matrix)
print(f'The number of rows containing no null elements - {count}')

max_duplicate = find_max_duplicate(matrix)
print(f'Maximum of the numbers occurring more than once in the matrix - {max_duplicate}')
