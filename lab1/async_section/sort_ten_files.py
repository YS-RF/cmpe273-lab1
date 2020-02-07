from pathlib import Path

def merge_sort (A):
    merge_sort2(A,0,len(A)-1)

def merge_sort2(A,first,last):
    if first < last:
        middle = (first + last )//2
        merge_sort2(A,first,middle)
        merge_sort2(A,middle+1,last)
        merge (A,first,middle,last)

def merge (A,first,middle,last):
    L = A [first:middle+1]
    R = A [middle+1:last+1]

    L.append(9999)
    R.append(9999)

    i=j=0
    for k in range (first,last+1):
        if L[i]<=R[j]:
            A[k] = L[i]
            i+=1
        else:
            A[k] = R[j]
            j+=1


def sort_ten_files():
    for i in range (1,11):
        filename_unsort = "unsorted_" + str(i) + ".txt"
        filename_sorted = "sorted_" + str(i) + ".txt"

        data_folder = Path("input/")
        file_to_open = data_folder / filename_unsort

        with open(file_to_open,'r') as f:
            array = []

            while True:  
                line = f.readline() 
                if not line: 
                    break
                array.append(int(line.strip()))
            #await here
            merge_sort(array)

            with open (data_folder / filename_sorted,"w+") as g:
                #await here
                for s in array:
                    g.write(str(s)+"\n")

    print("finish sorting 10 files")




sort_ten_files()