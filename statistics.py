
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
    
    for d in range(1, 10):
        dir = os.path.join(directory, str(d))
        if os.path.isdir(dir):
            print('Difficulty ' + str(d))
            for file in os.listdir(dir):
                id = filenameregex.match(file)
                if id != None:
                    
                    id = id[1]
                    
                    #print(id)
                    
                    logs = ""
                    with open(os.path.join(dir, file), 'r') as f:
                        logs = f.read()
                        f.close()
                        
                    cases = logs.split('Strategies: ')[1:]
                    
                    for c in cases:
                        strat = c.split('\n')[0].replace(" ", "")
                        #print('\ts: ' + strat)
                        
                        fields = fieldsregex.findall(c)
                        
                        for field, val in fields:
                            #print("\t\t" + str(field))
                            
                            infos.append([d, id, strat, field, float(val)])


    infos = pd.DataFrame(infos, columns=['difficulty', 'id', 'strategy', 'field', 'value'])
    
    infos.sort_values(by=["field", "strategy", "difficulty", "id"], inplace=True)

    infos.strategy.replace("", "none", inplace=True)

    sns.palplot(sns.color_palette("bright", 20))

    for f in infos['field'].unique():
        print('Plotting ' + f)
        fig, ax = plt.subplots(figsize=(20, 8))
    
        sns.swarmplot(ax=ax, x="strategy", y="value", hue="difficulty", data=infos[infos.field == f], dodge=True)
        # ax.legend_.remove()
        plt.title(f)
        plt.savefig(os.path.join(outdir, f + '.png'))
        plt.close()

    # for f in infos['field'].unique():
    #     print('Plotting ' + f)
    #     fig, ax = plt.subplots(figsize=(20, 8))
    #
    #     sns.swarmplot(ax=ax, x="strategy", y="value", hue="difficulty", data=infos[infos.field == f])
    #     # ax.legend_.remove()
    #     plt.title(f)
    #     plt.savefig(os.path.join(outdir, f + '_2.png'))
    #     plt.close()
            

if __name__ == "__main__":
   main(sys.argv[1:])

