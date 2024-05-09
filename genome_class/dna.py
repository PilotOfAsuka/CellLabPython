import numpy as np
import time

PAUSE = 0.15


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
    #123456789


dna = np.random.randint(0, 64, size=10000)
def dna_print(dna):
    time.sleep(2)
    rowIndex = 0
    len_dna = 0

    while len_dna != 100:
        len_dna = len_dna +1

        rowIndex = rowIndex +1
        if rowIndex == len(ROWS):
            rowIndex = 0


        if rowIndex == 0 or rowIndex ==9:
            print(ROWS[rowIndex])
            continue



        print(ROWS[rowIndex].format(dna[len_dna], len_dna))
        time.sleep(PAUSE)


dna_print(dna)