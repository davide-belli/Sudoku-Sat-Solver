
# coding: utf-8

import os.path
import sys, getopt


def main(argv):
    
    XWING = False
    CROSSHATCHING = False
    ALTERN_PAIRS = False
    CANDIDATE_LINES = False
    NAKED_PAIRS = False
    SINGLE_BOX = False
    
    try:
        opts, args = getopt.getopt(argv,"ho:laxcpb",["output=","candidatelines", "alternatepairs", "xwing", "crosshatching", "nakedpairs", "singlebox"])

    except getopt.GetoptError:
        print ('script.py -o <output> [-l] [-a] [-x] [-c] [-p] [-b]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('script.py -o <output> [-l] [-a] [-x] [-c] [-p] [-b]')
            sys.exit()
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-l", "--candidatelines"):
            CANDIDATE_LINES = True
        elif opt in ("-a", "--alternatepairs"):
            ALTERN_PAIRS = True
        elif opt in ("-x", "--xwing"):            
            XWING = True
        elif opt in ("-c", "--crosshatching"):            
            CROSSHATCHING = True
        elif opt in ("-p", "--nakedpairs"): 
            NAKED_PAIRS = True
        elif opt in ("-b", "--singlebox"): 
            SINGLE_BOX = True
            
    
    s=""
    count=0
    var=9*9*9


    #almeno_un_numero_per_cella
    for i in range(1,10):
        for j in range(1,10):
            for d in range(1,10):
                s+=str(i)+str(j)+str(d)+" "
            s+="0\n"
            count+=1


    print('almeno_un_numero_per_cella')

    #al_massimo_un_numero_per_cella
    for i in range(1,10):
        for j in range(1,10):
            for d in range(1,9):
                for k in range(d+1,10):
                    s+="-"+str(i)+str(j)+str(d)+" -"+str(i)+str(j)+str(k)+" 0\n"    
                    count+=1
                    
    print('al_massimo_un_numero_per_cella')

    #numeri_diversi_sulla_colonna
    for c in range(1,10):
        for i in range(1,9):
            for j in range(i+1,10):
                for d in range(1,10):
                    s+="-"+str(i)+str(c)+str(d)+" -"+str(j)+str(c)+str(d)+" 0\n"
                    count+=1

    print('numeri_diversi_sulla_colonna')

    #numeri_diversi_sulla_riga
    for r in range(1,10):
        for i in range(1,9):
            for j in range(i+1,10):
                for d in range(1,10):
                    s+="-"+str(r)+str(i)+str(d)+" -"+str(r)+str(j)+str(d)+" 0\n"
                    count+=1

    print('numeri_diversi_sulla_riga')


    #ogni_numero_nella_colonna
    for d in range(1,10):
        for c in range(1,10):
            for r in range(1,10):
                s+=str(r)+str(c)+str(d)+" "
            s+="0\n"
            count+=1

    print('ogni_numero_nella_colonna')

    #ogni_numero_nella_riga
    for d in range(1,10):
        for r in range(1,10):
            for c in range(1,10):
                s+=str(r)+str(c)+str(d)+" "
            s+="0\n"
            count+=1

    print('ogni_numero_nella_riga')

    #ogni_numero_nel_blocco
    for d in range(1, 10):
        for a in range(3):
            for b in range(3):
                for x in range(3):
                    for y in range(3):
                        s += str(3*a +x+1) + str(3*b+y+1) + str(d) + " "
                        
                s += "0\n"
                count += 1
    print('ogni_numero_nel_blocco')

    if XWING:
        #per colonne
        for n in range(1, 9):
            for r1 in range(1, 9):
                for r2 in range(r1+1, 10):
                    for c1 in range(1, 9):
                        for c2 in range(c1+1, 10):
                            
                            ip=""

                            for c in range(1, 10):
                                if c != c1 and c != c2:
                                    for r in [r1, r2]:
                                        ip += "-" + str(r) + str(c) + str(n) + " "

                            for r in range(1, 10):
                                if r != r1 and r != r2:
                                    for c in [c1, c2]:
                                        s += ip + "-" + str(r) + str(c) + str(n) + " 0\n"
                                        count += 1

        #per righe
        for n in range(1, 9):
            for r1 in range(1, 9):
                for r2 in range(r1 + 1, 10):
                    for c1 in range(1, 9):
                        for c2 in range(c1 + 1, 10):

                            ip = ""
                            for r in range(1, 10):
                                if r != r1 and r != r2:
                                    for c in [c1, c2]:
                                        ip += "-" + str(r) + str(c) + str(n) + " "

                            for c in range(1, 10):
                                if c != c1 and c != c2:
                                    for r in [r1, r2]:
                                        s += ip + "-" + str(r) + str(c) + str(n) + " 0\n"
                                        count += 1

        print('x-wing')

    #Single Box
    if SINGLE_BOX:
        for d in range(1,10):
            for a in range(0,3):
                for b in range(0,3):
                    for r in range (3*a+1,3*a+4):
                        for r2 in range (3*a+1,3*a+4):
                            if r2!=r:
                                for c2 in range(3*b+1,3*b+4):
                                    for c in range(1,10):
                                        if c!= 3*b+1 and c!= 3*b+2 and c!= 3*b+3:
                                            s+=str(r)+str(c)+str(d)+" "
                                    s+="-"+str(r2)+str(c2)+str(d)+" "
                                    s+="0\n"
                                    count+=1  
        for d in range(1,10):
            for a in range(0,3):
                for b in range(0,3):
                    for c in range (3*a+1,3*a+4):
                        for c2 in range (3*a+1,3*a+4):
                            if c2!=c:
                                for r2 in range(3*b+1,3*b+4):
                                    for r in range(1,10):
                                        if r!= 3*b+1 and r!= 3*b+2 and r!= 3*b+3:
                                            s+=str(r)+str(c)+str(d)+" "
                                    s+="-"+str(r2)+str(c2)+str(d)+" "
                                    s+="0\n"
                                    count+=1   
        print('single-box')

    #cross-hatching (numeri diversi nel blocco)
    if CROSSHATCHING:
        for d in range(1, 10):
            for a in range(3):
                for b in range(3):
                    for x in range(8):
                        for y in range(x+1, 9):
                            i, j = x//3, x % 3
                            k, l = y//3, y % 3
                            
                            s += '-' + str(3*a +i+1) + str(3*b+j+1) + str(d) + ' -' + str(3*a +k+1) + str(3*b+l+1) + str(d) + ' 0\n'
                            count += 1
        print('cross-hatching')

                 
    #candidate lines
    if CANDIDATE_LINES:
        for v in range(1, 10):
            for a in range(3):
                for b in range(3):
                    for c in range(3):
                        for l in range(1, 10):
                            if l not in range(3*a+1, 3*a+4):
                                for d in range(3):
                                    if d != c:
                                        for r in range(3):
                                            s += str(3*a +r+1) + str(3*b+d+1) + str(v) + " -" + str(l) + str(3*b+c+1) + str(v) + " "
                                s += "0\n"
                                count += 1
                                
        for v in range(1, 10):
            for a in range(3):
                for b in range(3):
                    for r in range(3):
                        for l in range(1, 10):
                            if l not in range(3*b+1, 3*b+4):
                                for d in range(3):
                                    if d != r:
                                        for c in range(3):
                                            s += str(3*a +d+1) + str(3*b+c+1) + str(v) + " -" + str(3*a+r+1) + str(l) + str(v) + " "
                                s += "0\n"
                                count += 1
        print("candidate lines")

    #naked pairs/disjoint subset
    if NAKED_PAIRS:
        for r in range(1,10):
            for c1 in range(1,9):
                for c2 in range (c1+1,10):
                    for d1 in range(1,9):
                        for d2 in range(d1+1,10):
                            for c3 in range (1,10):
                                if (c3!=c1 and c3!=c2):
                                    for dk in [d1,d2]:
                                        for d3 in range (1,10):
                                            if (d3!=d1 and d3!=d2):
                                                s+=str(r)+str(c1)+str(d3)+" "
                                                s+=str(r)+str(c2)+str(d3)+" "
                                        
                                        s+="-"+str(r)+str(c3)+str(dk)+" "
                                        s+="0\n"
                                        count+=1
        for c in range(1,10):
            for r1 in range(1,9):
                for r2 in range (r1+1,10):
                    for d1 in range(1,9):
                        for d2 in range(d1+1,10):
                            for r3 in range (1,10):
                                if (r3!=r1 and r3!=r2):
                                    for dk in [d1,d2]:
                                        for d3 in range (1,10):
                                            if (d3!=d1 and d3!=d2):
                                                s+=str(r1)+str(c)+str(d3)+" "
                                                s+=str(r2)+str(c)+str(d3)+" "
                                        
                                        s+="-"+str(r3)+str(c)+str(dk)+" "
                                        s+="0\n"
                                        count+=1
        print("naked_pairs")
        
    if ALTERN_PAIRS:
    
        # per colonne
        for n in range(1, 10):
            for a in range(3):
                for b in range(3):
                    if a != b:
                        for c in range(3):
                            for d in range(3):
                                if c != d:
                                    for r1 in range(3):
                                        for c1 in range(3):
                                            for c2 in range(3):
                                                for r2 in range(3):
                                                    for r3 in range(3):
                                                        ip = ""
                                                    
                                                        for x in range(1, 10):
                                                            if x != 3 * c + c1 + 1 and x != 3 * d + c2 + 1:
                                                                ip += "-" + str(3 * b + r1 + 1) + str(x) + str(n) + " "
                                                    
                                                        for x in range(1, 10):
                                                            if x != 3 * b + r1 + 1 and x != 3 * a + r3 + 1:
                                                                ip += "-" + str(x) + str(3 * d + c2 + 1) + str(n) + " "
                                                    
                                                        for x in range(1, 10):
                                                            if x != 3 * b + r1 + 1 and x != 3 * a + r2 + 1:
                                                                ip += "-" + str(x) + str(3 * c + c1 + 1) + str(n) + " "
                                                    
                                                        for x in range(3):
                                                            s += ip + "-" + str(3 * a + r3 + 1) + str(3 * c + x + 1) + str(n) + " 0\n"
                                                            count += 1
                                                        
                                                            s += ip + "-" + str(3 * a + r2 + 1) + str(3 * d + x + 1) + str(n) + " 0\n"
                                                            count += 1
                
                # per righe
                for n in range(1, 10):
                    for a in range(3):
                        for b in range(3):
                            if a != b:
                                for c in range(3):
                                    for d in range(3):
                                        if c != d:
                                            for r1 in range(3):
                                                for c1 in range(3):
                                                    for c2 in range(3):
                                                        for r2 in range(3):
                                                            for r3 in range(3):
                                                                ip = ""
                                                
                                                                for x in range(1, 10):
                                                                    if x != 3 * c + c1 + 1 and x != 3 * d + c2 + 1:
                                                                        ip += "-" + str(3 * b + r1 + 1) + str(x) + str(n) + " "
                                                
                                                                for x in range(1, 10):
                                                                    if x != 3 * b + r1 + 1 and x != 3 * a + r3 + 1:
                                                                        ip += "-" + str(x) + str(3 * d + c2 + 1) + str(n) + " "
                                                
                                                                for x in range(1, 10):
                                                                    if x != 3 * b + r1 + 1 and x != 3 * a + r2 + 1:
                                                                        ip += "-" + str(x) + str(3 * c + c1 + 1) + str(n) + " "
                                                
                                                                for x in range(3):
                                                                    s += ip + "-" + str(3 * a + r3 + 1) + str(3 * c + x + 1) + str(n) + " 0\n"
                                                                    count += 1
                                                    
                                                                    s += ip + "-" + str(3 * a + r2 + 1) + str(3 * d + x + 1) + str(n) + " 0\n"
                                                                    count += 1

        print("alternative pairs")



    print(count)
    print(var)



    with open(output, "w") as out:
        #out.write("c Example CNF format file\n")
        #out.write("c\n")
        #out.write("p cnf "+str(var)+" "+str(count)+"\n")
        out.write(s)



if __name__ == "__main__":
   main(sys.argv[1:])
