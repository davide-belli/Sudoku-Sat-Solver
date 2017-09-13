
# coding: utf-8

# In[73]:


s=""
count=0
var=9*9*9


# In[74]:


#almeno_un_numero_per_cella
for i in range(1,10):
    for j in range(1,10):
        for d in range(1,10):
            s+=str(i)+str(j)+str(d)+" "
        s+="0\n"
        count+=1


# In[75]:


#al_massimo_un_numero_per_cella
for i in range(1,10):
    for j in range(1,10):
        for d in range(1,10):
            for k in range(d+1,10):
                s+="-"+str(i)+str(j)+str(d)+" ""-"+str(i)+str(j)+str(k)+" "
                s+="0\n"    
                count+=1


# In[76]:


#numeri_diversi_sulla_colonna
for c in range(1,10):
    for i in range(1,10):
        for j in range(i+1,10):
            for d in range(1,10):
                s+="-"+str(i)+str(c)+str(d)+" ""-"+str(j)+str(c)+str(d)+" "
                s+="0\n" 
                count+=1   


# In[77]:


#numeri_diversi_sulla_riga
for r in range(1,10):
    for i in range(1,10):
        for j in range(i+1,10):
            for d in range(1,10):
                s+="-"+str(r)+str(i)+str(d)+" ""-"+str(r)+str(i)+str(d)+" "
                s+="0\n"
                count+=1    


# In[78]:


#numeri_diversi_sulla_riga
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
                    s+="-"+str(3*a+i)+str(3*b+j)+str(d)+" ""-"+str(3*a+k)+str(3*b+l)+str(d)+" "
                    s+="0\n"  
                    count+=1


# In[79]:


#ogni_numero_nella_colonna
for d in range(1,10):
    for c in range(1,10):
        for r in range(1,10):
            s+=str(r)+str(c)+str(d)+" "
        s+="0\n"
        count+=1


# In[80]:


#ogni_numero_nella_colonna
for d in range(1,10):
    for r in range(1,10):
        for c in range(1,10):
            s+=str(r)+str(c)+str(d)+" "
        s+="0\n"
        count+=1


# In[81]:


#x-wing_righe
for n in range(1,10):
    for r1 in range(1,10):
        for r2 in range(r1+1,10):
            for c1 in range(1,10):
                for c2 in range(c1+1,10):
                    for c in range(1,10):
                        if(c!=c1 and c!=c2):
                            for t in [r1,r2]:
                                s+="-"+str(t)+str(c)+str(n)+" "
                                for r in range(1,10):
                                    if(r!=r1 and r!=r2):
                                        s+=str(r)+str(c1)+str(n)+" "
                                        s+=str(r)+str(c2)+str(n)+" "
                                s+="0\n"
                                count+=1


# In[82]:


#x-wing_colonne
for n in range(1,10):
    for r1 in range(1,10):
        for r2 in range(r1+1,10):
            for c1 in range(1,10):
                for c2 in range(c1+1,10):
                    for r in range(1,10):
                        if(r!=r1 and r!=r2):
                            for t in [c1,c2]:
                                s+="-"+str(r)+str(t)+str(n)+" "
                                for c in range(1,10):
                                    if(c!=r1 and c!=r2):
                                        s+=str(r1)+str(c)+str(n)+" "
                                        s+=str(r2)+str(c)+str(n)+" "
                                s+="0\n"
                                count+=1


# In[83]:


print(count)
print(var)


# In[84]:


with open("test.txt", "a") as out:
    out.write("c Example CNF format file\n")
    out.write("c\n")
    out.write("p cnf "+str(var)+" "+str(count)+"\n")
    out.write(s)


# In[ ]:




