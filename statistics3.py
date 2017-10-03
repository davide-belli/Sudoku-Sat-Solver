
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

    strategies_infos = infos.groupby(['difficulty', 'strategy'], as_index=False).mean()
    strategies_infos['len'] = strategies_infos['strategy'].apply(lambda x : len(x))

    strat_stats = pd.DataFrame(index=list(range(1, 10)), columns=pd.MultiIndex.from_product([['propagation_per_decision', 'propagations', 'decisions', 'conflicts', 'CPU time', 'Memory used'], ['strategy', 'best']]))
    
    for f in ['propagation_per_decision', 'propagations']:
        row = strategies_infos.sort_values(by=[f, 'len'], ascending=[False, True]).groupby('difficulty').first()
        row = row[['strategy', f]].rename(columns={f:'best'})
        strat_stats[f] = row
    for f in ['decisions', 'conflicts', 'CPU time', 'Memory used']:
        row = strategies_infos.sort_values(by=[f, 'len'], ascending=[True, True]).groupby('difficulty').first()
        row = row[['strategy', f]].rename(columns={f: 'best'})
        strat_stats[f] = row
    print(strat_stats)

    
    with open(os.path.join(outdir, 'bests.txt'), 'w') as outfile:
        strat_stats.to_string(outfile)
    

    strategies_infos = strategies_infos.set_index('strategy')
    strategies_infos = strategies_infos.groupby('difficulty')
    
    def best_n(dataset, target, n=4, min=False, second_order=None):
        order = [target]
        ascending = [min]
        if second_order != None:
            order.append(second_order)
            ascending.append(True)
        
        return dataset.sort_values(by=order, ascending=ascending)[:n].index.values

    strat_stats = pd.DataFrame(index=list(range(1, 10)))

    for f in ['propagation_per_decision', 'propagations']:
        strat_stats[f] = strategies_infos.apply(lambda x: best_n(x, f, second_order='len'))
    for f in ['decisions', 'conflicts', 'CPU time', 'Memory used']:
        strat_stats[f] = strategies_infos.apply(lambda x: best_n(x, f, min=True, second_order='len'))
    print(strat_stats)

    
    with open(os.path.join(outdir, 'stats.txt'), 'w') as outfile:
        strat_stats.to_string(outfile)
    
    fields = list(set(infos.columns.values) - set(['CPU time', 'restarts', 'Memory used', 'difficulty', 'id', 'strategy']))

    for s in strategies:
        print('Strategy ' + s)
        if not os.path.exists(os.path.join(outdir, s + '/improvements/' )):
            os.makedirs(os.path.join(outdir, s + '/improvements/'))
        
        strats_base=['none']
        strats_comp=[s]
        for c in combinations:
            if s in c and len(c) > 1:
                strats_base.append(''.join(sorted(c - {s})))
                strats_comp.append(''.join(sorted(c)))
        
        print('\t' + str(strats_base))

        groups_b = infos[infos.strategy.isin(strats_base)].groupby(['difficulty', 'strategy'])[fields]
        groups_c = infos[infos.strategy.isin(strats_comp)].groupby(['difficulty', 'strategy'])[fields]

        base = groups_b.mean()
        comp = groups_c.mean()
        
        rename = {c:b for b, c in zip(strats_base, strats_comp)}
        
        comp = comp.reset_index().replace({'strategy':rename})
        comp.set_index(['difficulty', 'strategy'], inplace=True)
        
        data = (base - comp) / base
        
        data.reset_index(inplace=True)

        for f in fields:
            print('\t\tfield ' + f)
            
            lines = data.groupby('strategy')

            colors = [cm.jet(x) for x in np.linspace(0, 1, len(lines))]

            for i, (key, g) in enumerate(lines):
                plt.plot(g.difficulty, g[f], label=key, linewidth=0.5, color=colors[i])

                plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., fontsize=12)

            #plt.title(str(f) + ' mean improvement')
            plt.savefig(os.path.join(outdir, s + '/improvements/' + f + '_improvement.png'), dpi=200, bbox_inches='tight')
            plt.close()

            

if __name__ == "__main__":
   main(sys.argv[1:])

