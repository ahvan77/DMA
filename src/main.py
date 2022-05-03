# Input: The txt files of stress generated by Materials studio (See perl script).
# The text files first re-named. eg:
#    FRAME2_compression Data (2).txt => 2_Frame2.txt or 2.txt . 
# Output: G' and G'' by using time series and Green-Kubo methods
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft, ifft
from statsmodels.tsa.stattools import acf, pacf
import fnmatch
import os
from scipy import integrate
import csv
import func

#path = "New renamed files path ( e.g. C:/.../test/data)"
#path = "C:/Users/Prodesk_400_i5/Documents/Sadollah_lammps/MS/sin/TEST_NEW/test/DMA-MD/tests/data/"

####################################### Parameters and inputs##################
def splitstrip(s):
    return s.split(':')[1].strip()

with open('params.dat','r') as f:
    logw, T, Strain0, V, M, N, ts, n = tuple([float(splitstrip(x)) for x in f.read().rstrip().split('\n')])

######## These data come from MD simulation (perl script)##
# logw : Log of frequency (1.ps)
# T : Temperature (K)
# Strain0 :Strain Amplitude
# V : System Volume
# M : No. of stress text files (data)
# N : No of cycles
# ts : Time step
###########################################################
# n : average of data (default = 1)

kb=1.380649*1e-23                                    # Boltzmann constant
Sim = int(N*1000/(ts*10**(logw)))                    # Simulation time (fs)
Data_output = int(Sim/M)           
ti = np.array([i for i in range(0,Sim,Data_output)]) # time array 
w = 10**(logw)                                       # frequency
NDT = M / N                                     #  The No of data of one cycle 

#########################Print parameters######################################
print ()
print ("=====Parameters according the Materials Studio output==========")
print ()
print ("Log(f) = ", logw, " (1/ps)")
print ("Temperature = ", T, "(K)")
print ("No. periods = ", N)
print ("Simulation time = ", Sim, " (ps)")
print ()
print ()

###################Input File#############################################
#Input_Files = "*_Frame2.txt"                         # Stress text files 
Input_Files = input('Input the name files (use * for numbers, e.g. *_Frame2.txt):  ') 
print ()


columns_name = ['Time', 'Stress']

def last_4chars(x):
    return(x[:2])
##Read and sort the txt files =================================================
sx=fnmatch.filter(os.listdir(path), Input_Files )
sx.sort(key = last_4chars) 

#==================================Main program================================


s11=[]
t11=[]

#==== Read and save the XY shear stress (pa) data in athe s11 list =================================    
for j in range(int((len(fnmatch.filter(os.listdir(path), Input_Files ))))):
        f_number=int((sx[j].split(("_"),3)[0]))
        s = func.ReadFile(sx[j])
        s = np.array(s)[4:]
        s11.append(np.average(s))
#=======================================================================        
s11 = np.array(s11)  - np.array(s11)[0]
t11=ti[:len(s11)]      
      
def moving_average(a, n) :
     n = int(n)
     ret = np.cumsum(a, dtype=float)
     ret[n:] = ret[n:] - ret[:-n]
     return ret[n - 1:] / n
f1 = list(zip(t11,moving_average(s11,n)))
            
df = pd.DataFrame(f1, columns=columns_name)

df = df.apply(pd.to_numeric)  
df=df.astype(float) 

dt=df.Time[1]-df.Time[0]
df['Strain']=Strain0*np.sin(w*np.array(df.Time)*dt) #/(2*math.pi)
df['RStrain']=Strain0*w*np.cos(w*np.array(df.Time)*dt) #/(2*math.pi)**2



df['SACF']=np.correlate(df.Stress, df.Stress, mode="full")[df.shape[0]-1:]/df.shape[0]
df['G']=(V/(kb*T))*(df.SACF)

#=================================================

#============================= show_menu()

def show_menu() : 

    print("~ DMA Menu: ~")
    print("      G - Green_Kubo   #Claculate shear moduli using Green_Kubo expression")
    print("      T - time-series  #Claculate shear moduli using stress time-series")
    print("      P - Plot G(t)-Time")
    print("      S - Plot Stress-Time")
    print("      A - Plot Strain-Time")
    print("      Q - Quit")
    return 

def get_menu_option() :
    return input("Enter menu selection: ")




show_menu()
option = get_menu_option()

while option.lower() != 'q' :
   
    if option.lower() == 'g'  :
        G1, G11 = func.Green_Kubo(df, w)
        print ("log(G') = ", np.log(G1), "(Pa)")
        print ("log(G'') = ", np.log(G11), "(Pa)")
    
    elif option.lower() == 't'  :
        G1, G11 = func.stress_strain(df,w,Strain0,dt,NDT)
        print ("log(G') = ", np.log(G1), "(Pa)")
        print ("log(G'') = ", np.log(G11), "(Pa)")
    
    elif option.lower() == 'p'  :
        plt.plot(df.Time, df.G)  
        plt.show()
        
    elif option.lower() == 's'  :
        plt.plot(t11, s11)
        plt.show()
        
    elif option.lower() == 'a'  :
        plt.scatter(df.Time, df.Strain)
        plt.show()
           
    show_menu()
    option = get_menu_option()    
          

