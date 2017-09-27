
# coding: utf-8

import re
import numpy as np

import os.path
import sys, getopt


def main(argv):
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["input=", "output="])

    except getopt.GetoptError:
        print ('script.py -i <input> -o <output>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('script.py -i <input> -o <output>')
            sys.exit()
        elif opt in ("-o", "--output"):
            outfile = arg
        elif opt in ("-i", "--input"):
            infile = arg            


    fls = re.compile(r'(?<=-)(\d)(\d)(\d)')
    tr = re.compile(r'(?<!-)(\d)(\d)(\d)')

    #print(fls.findall('9 -8 123 -345 -456 789'))
    #print(tr.findall('9 -8 123 -345 -456 789'))

    sol = ""
    with open(infile, 'r') as f:
        sol = f.read()
        f.close()
        
    
    print(sol.split('\n')[0])    

    trues = tr.findall(sol)
    falses = fls.findall(sol)

    #print(len(trues))

    sudoku = np.zeros((9, 9), dtype='int')

    for r, c, d in trues:
        if int(r) > 0 and int(c) > 0:
            sudoku[int(r)-1, int(c)-1] = int(d)
        
    for r, c, d in falses:
        if sudoku[int(r)-1, int(c)-1] == str(d):
            print("ERROR! At " + r+ ", " + c+ " value " + d+ " conflict!")

    #print(sudoku)

    np.savetxt(outfile, sudoku.astype(int), fmt='%i', delimiter=',')




if __name__ == "__main__":
   main(sys.argv[1:])

