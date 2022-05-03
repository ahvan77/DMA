##### This is a simple code to rename the text files to desired ones
##### By running this code the text files in the "Materials Studio outputs" directory  ####
#####  renamed and the new files are created in the "data" directory                   ####
########## Change the path00, and path11 according to the path of your PC  

import os
import fnmatch
# Function to rename multiple files
path00="Materials studio text files path (e.g. C:/../tests/Materials Studio outputs/)"
path11="New renamed files path ( e.g. C:/.../test/data)"
finalname="_Frame2"
fname="*Frame2_*.txt"
def last_4chars(x):
    return(x[:3])

#sx.sort(key = last_4chars) 
#print(sx)

numOfIterations =  [i for i in range(1,2)]

for x in numOfIterations:
 #   path0 =path00 + "FRAME2_compression"+ " Data"+ " (" + str("{:d}".format(x))+")" + ".txt"
 #   path = path11+ "FRAME2_" + str("{:d}".format(x))+")" + ".txt"

    sx=fnmatch.filter(os.listdir(path00), "FRAME2_*.txt")
    for j in range(int((len(fnmatch.filter(os.listdir(path00), "FRAME2_*.txt"))))):
        print((sx[j].split(("_"),3)[1]).split(("."),1)[0])
        f_number=((sx[j].split(),3)[0])[2]
        #print(f_number) #.split()[0][1])
        f_number1=int((f_number.split("(")[1]).split(")"[0])[0])
        print(int((f_number.split("(")[1]).split(")"[0])[0]))
        my_dest =str(f_number1+1000) + finalname + ".txt"
        my_dest=path11+my_dest
        print(sx[j])
        my_source=path00+sx[j]
        size = os.path.getsize(my_source)/1024
        #print(size)
        if size>0:
            os.rename(my_source, my_dest)
    
    sx=fnmatch.filter(os.listdir(path11), fname)
    sx.sort(key = last_4chars) 

