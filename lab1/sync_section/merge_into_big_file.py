from pathlib import Path

array_of_opened_file = []

def sync_merge():
    #FINAL_CONSTANT_IMPORTANT = 10

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

    for thousand_time in range(1000):

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


sync_merge()



