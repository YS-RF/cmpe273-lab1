from pathlib import Path
#merge sort section
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

#sort ten files section
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
            merge_sort(array)

            with open (data_folder / filename_sorted,"w+") as g:
                for s in array:
                    g.write(str(s)+"\n")


# merge into a big file section
array_of_opened_file = []

def sync_merge():

    tdarr = [[0]*10 for i in range(10)]
    folder_name = Path("input/")
    final_output =  open(folder_name/"big_file.txt","w+")

    for i in range (1,11):

        file_name = "sorted_" + str(i) + ".txt"
        file_to_open = folder_name / file_name

        array_of_opened_file.append(open(file_to_open))


        for index in range (10):
            nextint = array_of_opened_file[i-1].readline()
            tdarr[i-1][index] = int(nextint.strip())

    for _ in range(1000):

        temp_local_min = find_local_min(tdarr)
        if temp_local_min is None:
            continue

        final_output.write(str(tdarr[temp_local_min[1]][0])+"\n")

        del tdarr [temp_local_min[1]][0]

        nextnum = array_of_opened_file[temp_local_min[1]].readline().strip()
        if nextnum == '':
            continue
        tdarr[temp_local_min[1]].append(int(nextnum))

    final_output.close()

def find_local_min (tdarr):
    localmin = 10000
    location = 0
    for i in range (10):
        while not tdarr[i]:
            i +=1
            if i >=10:
                return [localmin,location]


        if tdarr[i][0]<localmin:
            localmin = tdarr[i][0]
            location = i

    return [localmin,location]


for anything in array_of_opened_file:
    anything.close()




sort_ten_files()
sync_merge()