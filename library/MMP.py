
def find_redundancy(data,delete_limit):
    redundancy_data=data.corr()
    repetition=len(redundancy_data)
    delete_list=[]
    for i in range(length-1):
        repetition=length.remove(i)
        for j in repetition:
            if redundancy_data.ix[i][j]>=delete_limit and i<j:
                delete_list.append(j)

    for d in delete_list:
        self.data=data.drop(data.columns[d],axis=1)
