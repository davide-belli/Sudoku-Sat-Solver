from bs4 import BeautifulSoup
import numpy as np
import re
import requests

import os.path
import sys, getopt


regex = re.compile(r'(?:<a.*?>\s*(.*?)\s*</a>)|(\w+)', re.IGNORECASE)




def main(argv):
    
    XWING = False
    CROSSHATCHING = False
    ALTERN_PAIRS = False
    
    try:
        opts, args = getopt.getopt(argv,"hd:o:n:",["difficulty=", "outdir=", "number="])

    except getopt.GetoptError:
        print ('script.py -d <difficulty> -o <outdir> -n <number>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('script.py -d <difficulty> -o <outdir> -n <number>')
            sys.exit()
        elif opt in ("-d", "--difficulty"):
            difficulty = arg
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-n", "--number"):
            N = int(arg)
            
    
    assert (int(difficulty) >=0 and int(difficulty) <= 9), "difficulty ranges between 0 and 9!"
    assert (N >= 0), "the number of sudokus must be non negative"
    


    s_list = []
    
    i=0

    while i <N:    
        page = requests.get('http://www.menneske.no/sudoku/eng/random.html?diff='+difficulty)
        soup = BeautifulSoup(page.text, "lxml")
        s_id=str(soup.body).split("number: ")[1]
        s_id = s_id[0:7]
        table = soup.find('div', class_='grid')
        
        
        if s_id in s_list:
            print(s_id," is a copy\n")
        else:
            i+=1
            print("Importing Sudoku # ",i," on ",N," ----- ID: ",s_id)
            s_list.append(s_id)
            
            
            sudoku = np.zeros((9, 9))
            encoding=""
            
            r=0
            
            for row in table.find_all('tr'):
                c=0
                for col in row.find_all('td'):
                    x=(str(col).split('">',1)[1][0]).replace(" ","0")
                    #print(i,r,c)
                    
                    sudoku[r][c]=int(x)
                    
                    if x!="0":
                        encoding+= str(r+1)+str(c+1)+x+" 0\n"
                        
                        for d in range(1,10):
                            if str(d) != x:
                                encoding += '-'+str(r+1)+str(c+1)+str(d)+" 0\n"
                        
                    c+=1
                r+=1
            
            
            tmp = str(soup.body).split("Solution methods:  ")        
            tech = []
            if len(tmp) > 1:
                tmp =regex.findall(tmp[1].split("<br/>")[0])
                for t in tmp:
                    if t[0] == '':
                        tech.append(t[1])
                    else:
                        tech.append(t[0])
            
            #print("Printing Sudoku # ",i," on ",N," ----- ID: ",s_id)
            #print(sudoku)
            #print(encoding)
            #print(tech)        
            
            with open(os.path.join(outdir, s_id+"_sudoku.txt"), "w") as myfile:
                for r in range(9):
                    for c in range(9):
                        myfile.write(str(int(sudoku[r][c]))+" ")
                    myfile.write("\n")
                myfile.close()
                    
            with open(os.path.join(outdir, s_id+"_encoded.txt"), "w") as myfile:
                myfile.write(encoding)
                myfile.close()

            with open(os.path.join(outdir, s_id + '_info.txt'), 'w') as f:
                for t in tech:
                    f.write(t + '\n')
                f.close()
            
            
            print("     Done")

    print('Finished!')





if __name__ == "__main__":
   main(sys.argv[1:])
