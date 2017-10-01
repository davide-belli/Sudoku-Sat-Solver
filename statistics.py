
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
                        strat = c.split('\n')[0]
                        strat = strat.replace(" ", "")
                        strat = strat.replace("-", "")
                        strat = strat.replace("s", "")
                        
                        strat=''.join(sorted(strat))
                        
                        
                        fields = fieldsregex.findall(c)
                        
                        if len(fields) > 1:
                            row = {'difficulty': d, 'id' : id, 'strategy' : strat}
                            
                            for field, val in fields:
                                row[field] = float(val)
                                
                            infos.append(row)

    
    
    infos = pd.DataFrame(infos)

    l1 = len(infos)
    infos = infos.groupby(['strategy', 'difficulty', 'id']).first().reset_index()
    l2 = len(infos)
    if l2 < l1:
        print("ATTENTION! DUPLICATE ENTRIES! " + str((l1, l2, l1 - l2)))

    infos.strategy.replace("", "none", inplace=True)
    infos.sort_values(by=['strategy', 'difficulty', 'id'], inplace=True)
    
    infos['propagation_per_decision'] = infos['propagations'] / infos['decisions']
    infos['conflicts_per_decision'] = infos['conflicts'] / infos['decisions']

    print(infos[(np.isfinite(infos['propagation_per_decision'])) & infos['propagation_per_decision'].notnull()]['propagation_per_decision'].describe())
    print(infos[(np.isfinite(infos['conflicts_per_decision'])) & infos['conflicts_per_decision'].notnull()]['conflicts_per_decision'].describe())
    
    sns.palplot(sns.color_palette("bright", 20))
    
    print(infos.columns.values)

    for f in (set(infos.columns.values) - set(['difficulty', 'id', 'strategy'])):
        print('Plotting ' + f)
        fig, ax = plt.subplots(figsize=(40, 8))

        sns.swarmplot(ax=ax, x="strategy", y=f, hue="difficulty", size=1.4, data=infos, dodge=True)
        plt.title(f)
        plt.savefig(os.path.join(outdir, f + '.png'), dpi=200)
        plt.close()

            

if __name__ == "__main__":
   main(sys.argv[1:])

