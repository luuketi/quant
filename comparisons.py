from pricer import binomial_tree
import matplotlib.pyplot as plt
import numpy as np


S_range = range(100)
r_range = np.arange( 0, 0.5, 0.05 )
T_range = np.arange( 0.1, 3, 0.1 )
volatility_range = np.arange( 0.1, .5, 0.05 )

C_0_S = [binomial_tree(S_0=S_0, K=62, T=0.5, r=0.06, volatility=0.13, N=300) for S_0 in S_range]
C_0_r = [binomial_tree(S_0=60, K=62, T=0.5, r=R, volatility=0.13, N=300) for R in r_range]
C_0_T = [binomial_tree(S_0=60, K=62, T=t, r=0.06, volatility=0.13, N=300) for t in T_range]
C_0_volatility = [binomial_tree(S_0=60, K=62, T=0.5, r=0.06, volatility=volatility, N=300) for volatility in volatility_range]

fig, axs = plt.subplots(2, 2, gridspec_kw={'hspace': 0.25, 'wspace': 0.25})
fig.suptitle('C_0')

axs[0, 0].plot(S_range, C_0_S)
axs[0, 0].set(xlabel='S_0')

axs[0, 1].plot(r_range, C_0_r, 'tab:orange')
axs[0, 1].set(xlabel='r')

axs[1, 0].plot(T_range, C_0_T, 'tab:green')
axs[1, 0].set(xlabel='T')

axs[1, 1].plot(volatility_range, C_0_volatility, 'tab:red')
axs[1, 1].set(xlabel='volatility')

plt.show()