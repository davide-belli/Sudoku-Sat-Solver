
# coding: utf-8

import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os.path
import sys, getopt
import pandas as pd

sns.set(style="whitegrid", color_codes=True)

def main(argv):
    
    try:
        opts, args = getopt.getopt(argv,"hd:o:",["directory=", "outdir="])

    except getopt.GetoptError:
        print ('script.py -d <directory> -o <outdir>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('script.py -d <directory> -o <outdir>')
            sys.exit()
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-d", "--directory"):
            directory = arg
            

    filenameregex = re.compile(r'(.*)_log.txt')
    
    #use this to match also the basic info in the first lines about the number of variables, number of clauses etc.
    #fieldsregex = re.compile(r'(\w+(?: \w+)*)\s*:\s*(\d+ | \d+\.\d+)')
    
    #use this one istead in order to match only the info about the sat solving
    fieldsregex = re.compile(r'(?<=\n)(\w+(?: \w+)*)\s*:\s*(\d+|\d+\.\d+)')
    
    
    infos = []
    
    for file in os.listdir(directory):
        id = filenameregex.match(file)
        if id != None:
            
            id = id[1]
            
            print(id)
            
            logs = ""
            with open(os.path.join(directory, file), 'r') as f:
                logs = f.read()
                f.close()
                
            cases = logs.split('Strategies: ')[1:]
            
            for c in cases:
                strat = c.split('\n')[0].replace(" ", "")
                #print('\ts: ' + strat)
                
                fields = fieldsregex.findall(c)
                
                for field, val in fields:
                    #print("\t\t" + str(field))
                    
                    infos.append([id, strat, field, float(val)])

    infos = pd.DataFrame(infos, columns=['id', 'strategy', 'field', 'value'])
    
    infos.sort_values(by=["field", "strategy", "id"], inplace=True)

    infos.strategy.replace("", "none", inplace=True)
    
    
    
    for f in infos['field'].unique():
        ax = sns.stripplot(x="strategy", y="value", hue="id", data=infos[infos.field == f], jitter=1.5, palette="Paired")
        ax.legend_.remove()
        plt.title(f)
        plt.savefig(os.path.join(outdir, f+'.png'))
            

if __name__ == "__main__":
   main(sys.argv[1:])

