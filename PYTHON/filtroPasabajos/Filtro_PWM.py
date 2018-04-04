import numpy as np
import matplotlib.pyplot as  plt


duty = 2000 

signal = np.zeros( (20000,1) )
signal[:duty] = np.ones( (duty,1) )*3.3

for i in range(4):
	signal = np.append(signal,signal)

sigSize = signal.shape[0]
 
#fourier

T = 1e-6
f1 = np.fft.fft(signal) * T
D = 2*np.pi/(sigSize*T)
m = np.array([D*i for i in range(sigSize)])

fig,axes = plt.subplots(2)

axes[0].plot(np.arange(20000*5),signal[:20000*5])
axes[1].plot(m[:200],abs(f1[:200]) )

[ax.grid() for ax in axes]

plt.show()
