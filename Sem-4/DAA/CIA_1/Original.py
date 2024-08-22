# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random

match = 5
mismatch = -4
char_set = "ACGT"
char_count_1 = [0, 0, 0, 0]
char_count_2 = [0, 0, 0, 0]

s1 = ""
s2 = ""

while len(s1) < 16:
  s = random.choice(char_set)
  if (s1.count(s) == 4):
    continue
  else:
    s1 += s


while len(s2) < 16:
  s = random.choice(char_set)
  if (s2.count(s) == 4):
    continue
  else:
    s2 += s


alignment = [[0 for i in range(len(s1))] for j in range(len(s2))]

def score(alignment, s1, s2, row):
  if (row == len(s1)):
  return alignment

for j in range(1, len(s2)+1):
  if s1[row-1] == s2[j-1]:
    alignment[row][j] = alignment[row-1][j-1] + match
  else:
    num = max(alignment[row-1][j], alignment[row-1][j-1], alignment[row][j-1])
    num += mismatch
   if (num < 0):
    num = 0
   alignment[row][j] = num

score(alignment, s1, s2, row+1)


alignment = score(alignment, s1, s2, 1)
print(alignment)
