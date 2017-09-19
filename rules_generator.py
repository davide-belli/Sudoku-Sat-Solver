
# coding: utf-8

import os.path
import sys, getopt


def main(argv):
    
    XWING = False
    CROSSHATCHING = False
    ALTERN_PAIRS = False
    
    try:
        opts, args = getopt.getopt(argv,"ho:axc",["output=","alternativepairs", "xwing", "crosshatching"])

    except getopt.GetoptError:
        print ('script.py -o <output> [-a] [-x] [-c]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('script.py -o <output> [-a] [-x] [-c]')
            sys.exit()
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-a", "--alternativepairs"):
            ALTERN_PAIRS = True
        elif opt in ("-x", "--xwing"):            
            XWING = True
        elif opt in ("-c", "--crosshatching"):            
            CROSSHATCHING = True
            
    
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


    #numeri_diversi_nel_blocco
    for a in range(0,3):
        for b in range(0,3):
            for d in range(1,10):
                for x in range(0,8):
                    for y in range(x+1,9):
                        i=x//3+1
                        j=x%3+1
                        k=y//3+1
                        l=y%3+1
                        #print(i," ",j," ",k," ",l)
                        s+="-"+str(3*a+i)+str(3*b+j)+str(d)+" -"+str(3*a+k)+str(3*b+l)+str(d)+" 0\n"  
                        count+=1
    print('numeri_diversi_nel_blocco')

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
        for n1 in range(1, 9):
            for n2 in range(n1+1, 10):
                for r1 in range(1, 9):
                    for r2 in range(r1+1, 10):
                        for c1 in range(1, 9):
                            for c2 in range(c1+1, 10):
                                for i in range(1, 10):
                                    if i != r1 and i != r2:
                                        for j in (c1, c2):
                                            for n in [n1, n2]: 
                                                for r in [r1, r2]:
                                                    for c in [c1, c2]:
                                                        for m in range(1, 10):
                                                            if m!=n1 and m!=n2:                
                                                                s+= str(r) + str(c)+str(m) + " "
                                                
                                                
                                                s+="-" + str(i)+str(j)+str(n)+" 0\n"
                                                count +=1
        #per righe
        for n1 in range(1, 9):
            for n2 in range(n1+1, 10):
                for r1 in range(1, 9):
                    for r2 in range(r1+1, 10):
                        for c1 in range(1, 9):
                            for c2 in range(c1+1, 10):
                                for j in range(1, 10):
                                    if j != c1 and j != c2:
                                        for i in (r1, r2):
                                            for n in [n1, n2]: 
                                                for r in [r1, r2]:
                                                    for c in [c1, c2]:
                                                        for m in range(1, 10):
                                                            if m!=n1 and m!=n2:                
                                                                s+= str(r) + str(c)+str(m) + " "
                                                
                                                
                                                s+="-" + str(i)+str(j)+str(n)+" 0\n"
                                                count +=1                                                            
                                                            
        print('x-wing')

    #cross-hatching
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

                 
    #alternative_pair
    if ALTERN_PAIRS:
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



    print(count)
    print(var)



    with open(output, "w") as out:
        #out.write("c Example CNF format file\n")
        #out.write("c\n")
        #out.write("p cnf "+str(var)+" "+str(count)+"\n")
        out.write(s)



if __name__ == "__main__":
   main(sys.argv[1:])
