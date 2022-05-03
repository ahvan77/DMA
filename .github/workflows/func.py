import numpy as np
import math
def ReadFile(File):
    f = open(File)
    s = []
    data = False
    for i, line in enumerate(f):
        if line.startswith('FUNCTION: XY'):
            data = True

            line = next(f)
            line = next(f)
            line = next(f)

            s.append(float(line.split()[6])*1e9) # GP to Pascal
                
    return s

def stress_strain(df,w,Strain0,dt,NDT):
    G11_i = 0
    G1_i = 0
    for k in range (df.shape[0]):
        G11_i += (df.Stress.values[k]*df.RStrain.values[k]*dt)
        G1_i += (df.Stress.values[k]*df.Strain.values[k]*dt)
    G11_i = abs(G11_i/(Strain0*Strain0*math.pi*df.shape[0]/NDT)) 
    G1_i = abs(G1_i*w/(Strain0*Strain0*math.pi*df.shape[0]/NDT))
                        
    return G1_i, G11_i

def Green_Kubo(df, w):
	Coef = w*df.Time
	Gtf = df.G*(np.exp(-1j*Coef))
	GFFT2 = 1j*w*np.fft.fft(df.G)
	return np.mean(abs(GFFT2.real)), np.mean(abs(GFFT2.imag))
