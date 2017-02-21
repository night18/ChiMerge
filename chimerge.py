from __future__ import division


def read(file):  
    '''read raw date from a file '''  
    Instances=[]  
    fp=open(file,'r')  
    for line in fp:  
        line=line.strip('\n') #discard '\n'  
        if line!='':  
            Instances.append(line.split(','))  
    fp.close()  
    return(Instances)  
  


''' Split the 4 attibutes, collect the data of the ith attributs, i=0,1,2,3 
    Return a list like [['4.3', 'Iris-setosa'], ['4.4', 'Iris-setosa'],...]'''  
def split(content,i):  
    iris_data=[]  
    for r in content:  
        iris_data.append([r[i],r[4]])  
    return(iris_data)  
  

''' Count the number of the same record
    Return a list like [['4.3', 'Iris-setosa', 1], ['4.4', 'Iris-setosa', 3],...]'''
def count(iris_data):  
    counted_data=[]  
    iris_data.sort(key=lambda iris_data:iris_data[0])  
    i=0  
    while(i<len(iris_data)):  
        times=iris_data.count(iris_data[i])#count the number of the same record  
        record=iris_data[i][:]  
        record.append(times) # append the number of the same record to the record  
        counted_data.append(record)  
        i+=times #count the next different item   
    return(counted_data)  
  
''' Build a structure that ChiMerge algorithm works properly on it 
    Return a dictionary {'4.3': [1,0,2], ... }'''     
def build(counted_data):  
    length_dic={}  
    for record in counted_data:
        if record[0] not in length_dic.keys():  
            length_dic[record[0]]=[0,0,0]  
        if record[1]=='Iris-setosa':  
            length_dic[record[0]][0]=record[2] 
        elif record[1]=='Iris-versicolor':  
            length_dic[record[0]][1]=record[2]  
        elif record[1]=='Iris-virginica':  
            length_dic[record[0]][2]=record[2]  
        else:  
            raise TypeError("Data Exception")  
    length_dic=sorted(length_dic.items())  
    return(length_dic)  
  
''' Order data and make every value is in a separate interval '''
def Initialize(content,i):  
    iris_data=split(content,i)  
    counted_data=count(iris_data)  
    length_dic=build(counted_data)  
    return(length_dic)  
  
''' Compute the Chi-Square value '''     
def chi2(intervals):    
    m=len(intervals)  
    num_class=len(intervals[0])  
    #sum of each row
    Rows=[]  
    for i in range(m):  
        sum=0  
        for j in range(num_class):  
            sum+=intervals[i][j]  
        Rows.append(sum) 
    #sum of each column
    Cols=[]  
    for j in range(num_class):  
        sum=0  
        for i in range(m):  
            sum+=intervals[i][j]  
        Cols.append(sum)  
    #total number in the intervals
    N=0  
    for i in Cols:  
        N += i  
    
    chi_value=0  
    for i in range(m):  
        for j in range(num_class):  
            Estimate=Rows[i]*Cols[j]/N  
            if Estimate!=0:  
                chi_value=chi_value+(intervals[i][j]-Estimate)**2/Estimate  
    return chi_value  
  
''' ChiMerge algorithm 
    Return split points '''    
def ChiMerge(length_dic,max_interval):  

    num_interval=len(length_dic)
    ceil = max(record[0] for record in length_dic) 
    print(ceil) 
    while(num_interval>max_interval):                 
        num_pair=num_interval-1  
        chi_values=[]
        #calculate the chi value of each neighbor interval  
        for i in range(num_pair):  
            intervals=[length_dic[i][1],length_dic[i+1][1]]  
            chi_values.append(chi2(intervals))  
        # get the minimum chi value 
        min_chi=min(chi_values)
        for i in range(num_pair-1,-1,-1): # treat from the last one, because I change the bigger interval as 'Merged' 
            if chi_values[i]==min_chi:
                # combine the two adjacent intervals
                temp = length_dic[i][:]
                for j in range(len(length_dic[i+1])):
                     temp[1][j] += length_dic[i+1][1][j]
                
                length_dic[i]=temp  
                length_dic[i+1]='Merged'  
        while('Merged' in length_dic): # remove the merged record  
            length_dic.remove('Merged')  
        num_interval=len(length_dic)
        
    split_points = []
    for record in length_dic:
        split_points.append(record[0])
    
    print('split_point = {lst} \nfinal intervals'.format(lst = split_points))
    split_points.append(ceil)
    for i in range(len(split_points)-1):
        print split_points[i] + '~' + split_points[i+1]

    return(split_points)  
  
  
def discrete(path):  
    ''' ChiMerege discretization of the Iris plants database '''  
    content=read(path)  

    max_interval=6  
    num_attr=4  
    attrlist = ['sepal length', 'sepal width', 'petal length', 'petal width']
    for i in range(num_attr):  
        print('\n'+attrlist[i])
        length_dic=Initialize(content,i) # Order and Initialize  
        split_points=ChiMerge(length_dic,max_interval) # discretize data using ChiMerge algorithm   
      
  
if __name__=='__main__':
    print ('Author: Chun-Wei Chiang') 
    discrete('/home/chunwei/IRIS/iris.data')  

'''Attribute Information:
   1. sepal length in cm
   2. sepal width in cm
   3. petal length in cm
   4. petal width in cm
   5. class: 
      -- Iris Setosa
      -- Iris Versicolour
      -- Iris Virginica
'''