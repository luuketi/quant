from math import sqrt, pow, log, exp
import scipy.integrate as integrate
from numpy import pi, inf

def BlackScholes( S_0, K, T, r, volatility ):

        d1 = 1 / (volatility * sqrt( T)) * log( S_0 * exp( r * T ) / K ) + .5 * volatility * sqrt( T )
        d2 = 1 / (volatility * sqrt(T)) * log( S_0 * exp(r * T) / K) - .5 * volatility * sqrt(T)

        def N(d):
            return 1 / sqrt(2*pi) * integrate.quad( lambda x: exp(-1*(x**2)/2), -inf, d)[0]

        return S_0 * N(d1) - K * exp(-1*r*T) * N(d2)

if __name__ == '__main__':
    print(BlackScholes(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13))