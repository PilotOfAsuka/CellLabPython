import numpy as np
import time

PAUSE = 0.15  # Change it 0.0 and see what happen

# below are the rows of DNA animation

ROWS = [
    '         ##',
    '        #{}-{}#',
    '       #{}---{}#',
    '      #{}-----{}#',
    '     #{}------{}#',
    '    #{}------{}#',
    '    #{}-----{}#',
    '     #{}---{}#',
    '      #{}-{}#',
    '       ##',
    '      #{}-{}#',
    '      #{}---{}#',
    '     #{}-----{}#',
    '     #{}------{}#',
    '      #{}------{}#',
    '       #{}-----{}#',
    '        #{}---{}#',
    '         #{}-{}#',]
    #123456789 use this to measure the number of spaces


dna = np.random.randint(0, 64, size=10000)
def dna_print(dna):
    time.sleep(2)
    rowIndex = 0
    len_dna = 0
    #Main loop of the program || Started
    while len_dna != 100:
        len_dna = len_dna +1
        #incrementing for to draw a next row:
        rowIndex = rowIndex +1
        if rowIndex == len(ROWS):
            rowIndex = 0

        # Row indexes 0 and 9 don't have nucleotides:
        if rowIndex == 0 or rowIndex ==9:
            print(ROWS[rowIndex])
            continue



        # priting the row
        print(ROWS[rowIndex].format(dna[len_dna], len_dna))
        time.sleep(PAUSE)


dna_print(dna)