from math import sqrt, pow, log, exp
import numpy as np

def MonteCarloPricer( S_0, K, T, r, volatility, N = 100 ):

    sum_ = sum(
        [max(S_0 * exp(np.random.normal(0, 1) * volatility * sqrt(T) + T * (r - volatility ** 2 / 2)) - K, 0) for n in
         range(N)])
    return 1 / N * exp( -1 * r * T ) * sum_

if __name__ == '__main__':
    print(MonteCarloPricer(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=9999))

