
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
    
    strategies = set(''.join(infos.strategy.unique())) # | {'none'}

    strategies_split = [
        ['none'] + ['b', 'c', 'l'],
        ['none'] + ['p', 'x', 'a']
    ]

    print(strategies)
    
    
    
    infos.strategy.replace("", "none", inplace=True)
    infos.sort_values(by=['strategy', 'difficulty', 'id'], inplace=True)
    
    infos['propagation_per_decision'] = infos['propagations'] / infos['decisions']
    infos['conflicts_per_decision'] = infos['conflicts'] / infos['decisions']

    infos_singles = infos[infos.strategy.isin(strategies | {'none'})]

    print(infos[(np.isfinite(infos['propagation_per_decision'])) & infos['propagation_per_decision'].notnull()]['propagation_per_decision'].describe())
    print(infos[(np.isfinite(infos['conflicts_per_decision'])) & infos['conflicts_per_decision'].notnull()]['conflicts_per_decision'].describe())
    
    sns.palplot(sns.color_palette("bright", 20))

    print(infos.columns.values)
    print(infos.index.values)

    print(infos.groupby('difficulty')['decisions'].nlargest(2).shape)
    print(infos.groupby('difficulty')['decisions'].nlargest(2).values)
    
    
    
    for f in (set(infos.columns.values) - set(['difficulty', 'id', 'strategy'])):
        print('Plotting ' + f)
    
        fig, axes = plt.subplots(2, 1, sharey=True, figsize=(20, 10))
    
        for j, ax in enumerate(axes):
            sns.swarmplot(ax=ax, x="strategy", y=f,
                          data=infos_singles[infos_singles.strategy.isin(strategies_split[j])], hue="difficulty",
                          dodge=True, order=strategies_split[j], hue_order=list(range(1, 10)))  # , size=2)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[:0], labels[:0])
            ax.set_xlabel('')
            ax.set_ylabel('')
    
        for ax in axes:
            ax.vlines([0.5], *ax.get_ylim())
            ax.tick_params(labelsize=20)

        # plt.title(f)
    
        handles, labels = axes[-1].get_legend_handles_labels()
        plt.legend(handles[0:9], labels[0:9], bbox_to_anchor=(1.01, 1.5), loc=2, borderaxespad=0., fontsize=20)
    
        plt.savefig(os.path.join(outdir, f + '_single_split.png'), dpi=200, bbox_inches='tight')
        plt.close()

    for f in (set(infos.columns.values) - set(['difficulty', 'id', 'strategy'])):
        print('Plotting ' + f)

        fig, ax = plt.subplots(figsize=(40, 8))

        sns.swarmplot(ax=ax, x="strategy", y=f, hue="difficulty", data=infos_singles, dodge=True)  # , size=2)
        #plt.title(f)
        plt.legend(bbox_to_anchor=(1.01, 0.75), loc=2, borderaxespad=0., fontsize=20)
        plt.savefig(os.path.join(outdir, f + '_single.png'), dpi=200, bbox_inches='tight')
        plt.close()

        fig, ax = plt.subplots(figsize=(40, 8))

        sns.swarmplot(ax=ax, x="strategy", y=f, hue="difficulty", size=1.4, data=infos, dodge=True)
        #plt.title(f)
        plt.legend(bbox_to_anchor=(1.01, 0.75), loc=2, borderaxespad=0., fontsize=20)
        plt.savefig(os.path.join(outdir, f + '.png'), dpi=200, bbox_inches='tight')
        plt.close()

        

            

if __name__ == "__main__":
   main(sys.argv[1:])

