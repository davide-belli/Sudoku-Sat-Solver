
# coding: utf-8

import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import os
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

    infos['propagation_per_decision'] = infos['propagations'] / infos['decisions']
    
    strategies = set(list(''.join(infos.strategy.unique())))
    combinations = infos.strategy.unique()
    
    combinations = [set(list(c)) for c in combinations]
    
    print(strategies)
    print(combinations)
    
    
    infos.strategy.replace("", "none", inplace=True)
    
    fields = list(set(infos.columns.values) - set(['CPU time', 'restarts', 'Memory used', 'difficulty', 'id', 'strategy']))

    for s in strategies:
        print('Strategy ' + s)
        if not os.path.exists(os.path.join(outdir, s)):
            os.makedirs(os.path.join(outdir, s))
        
        strats=['none']
        for c in combinations:
            if s in c:
                strats.append(''.join(sorted(c)))
        
        print('\t' + str(strats))
        
        groups = infos[infos.strategy.isin(strats)].groupby(['difficulty', 'strategy'])[fields]
        
        analysis = {}
        analysis['mean'] = groups.mean().reset_index()
        analysis['median'] = groups.median().reset_index()
        analysis['var'] = groups.var().reset_index()
        
        for f in fields:
            print('\t\tfield ' + f)
            for an, data in analysis.items():
                #fig, ax = plt.subplots()
                #axs, labels = [], []
                
                lines = data.groupby('strategy')
                
                colors = [cm.jet(x) for x in np.linspace(0, 1, len(lines))]

                for i, (key, g) in enumerate(lines):
                    #axs.append(ax.scatter(g.difficulty, g[f]))
                    plt.plot(g.difficulty, g[f], label=key, linewidth=0.5, color=colors[i])
                    #labels.append(key)
                
                #print('\t\t' + str(len(labels)))
                
                #plt.legend(axs, labels)
                plt.legend()
                
                plt.title(str(f) + ' ' + an)
                plt.savefig(os.path.join(outdir, s + '/' + f + '_' + an + '.png'), dpi=200)
                plt.close()

            

if __name__ == "__main__":
   main(sys.argv[1:])

