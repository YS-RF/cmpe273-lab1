import asyncio
from pathlib import Path

array_of_opened_file = []
tdarr = [[0]*10 for i in range(10)]
folder_name = Path("input/")
final_output =  open(folder_name/"big_file.txt","w+")
# define tdarr
for i in range (1,11):

    file_name = "sorted_" + str(i) + ".txt"
    file_to_open = folder_name / file_name

    array_of_opened_file.append(open(file_to_open))

    for index in range (10):
        nextint = array_of_opened_file[i-1].readline()
        tdarr[i-1][index] = int(nextint.strip())
# find local min and location

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


async def find_minimum(myQueue):
    for index in range (1000):
        temp_local_min = find_local_min(tdarr)
        if temp_local_min is None:
            continue
        await myQueue.put(temp_local_min)
        del tdarr [temp_local_min[1]][0]




async def bring_data_in(myQueue):
    while not myQueue.empty():  
        item = await myQueue.get()
        if item is None:
            break
        final_output.write(str(item[0])+"\n")

        nextnum = array_of_opened_file[item[1]].readline().strip()
        if nextnum == '':
            continue
        tdarr[item[1]].append(int(nextnum))

loop = asyncio.get_event_loop()
myQueue = asyncio.Queue(loop=loop, maxsize=5)

try:
    loop.run_until_complete(asyncio.gather(find_minimum(myQueue), bring_data_in (myQueue)))
finally:
    loop.close()

for anything in array_of_opened_file:
    anything.close()