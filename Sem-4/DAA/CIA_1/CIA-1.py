import random

random.seed(69)
match = 5
mismatch = -4
string_length = 16

def generate_string(length, count):
    if length == 0:
        return ""
    else:
        letters = ['A'] * count['A'] + ['C'] * count['C'] + ['G'] * count['G'] + ['T'] * count['T']
        return random.choice(letters) + generate_string(length - 1, count)

count = {'A' : 4, 'C' : 4, 'G' : 4, 'T' : 4}

genome_1 = generate_string(string_length, count)
genome_2 = generate_string(string_length, count)

alignment_matrix = [[0 for x in range(string_length + 1)] for y in range(string_length + 1)]


def print_matrix(matrix, i, j, c, sl, flag=0):
    if flag == 0:
        print('      ', end = '')
        for x in genome_1:
            print(x, end = '  ')
        print()
        print('  ', end=' ')
        flag = 1
    if i == sl:
        return
    if j == sl:
        print()
        if c != sl:
            print(genome_2[c], end = '  ')
        print_matrix(matrix, i+1, 0, c+1, 1, sl)
    else:
        print(matrix[i][j], end = '  ')
        print_matrix(matrix, i, j+1, c, 1, sl)
        
def dp(s1, s2, alignment_matrix, i, j):
    if j > len(s2):
        print(alignment_matrix)
        return alignment_matrix
    else:
        if i > len(s1):
            dp(s1, s2, alignment_matrix, 1, j+1)
            return alignment_matrix
        else:
            # MATCH
            if s1[j-1] == s2[i-1]:
                alignment_matrix[i][j] = alignment_matrix[i-1][j-1] + match;
            # MISMATCH
            else:
                alignment_matrix[i][j] = max(alignment_matrix[i-1][j], alignment_matrix[i][j-1]) + mismatch;
            dp(s1, s2, alignment_matrix, i+1, j)

'''def traceback(alignment_matrix, i, j, s1, s2):
    if i==j==0:
        return
    else:'''


print(genome_1)
print(genome_2)
print()
# print_matrix(alignment_matrix, 0, 0, 0)
dp(genome_1, genome_2, alignment_matrix, 0, 0)
#print_matrix(alignment_matrix, 0, 0, 0, string_length)