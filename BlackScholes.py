from math import sqrt, pow, log, exp
import scipy.integrate as integrate
from scipy.misc import derivative

from numpy import pi, inf

class BlackScholes( object ):

    def __init__( self, S_0, K, T, r, volatility ):
        self.S_0 = S_0
        self.K = K
        self.T = T
        self.r = r
        self.volatility = volatility

        self.d1 = 1 / (self.volatility * sqrt(self.T)) * log( self.S_0 * exp( self.r * self.T ) / self.K ) + .5 * self.volatility * sqrt( self.T )
        self.d2 = 1 / (self.volatility * sqrt(self.T)) * log( self.S_0 * exp( self.r * self.T ) / self.K ) - .5 * self.volatility * sqrt( self.T )

    def _N( self, d ):
            return 1 / sqrt(2*pi) * integrate.quad( lambda x: exp(-1*(x**2)/2), -inf, d )[0]

    def getPrice( self ):
        return self.S_0 * self._N( self.d1 ) - self.K * exp( -1 * self.r * self.T ) * self._N( self.d2 )

    def delta( self ):
        return self._N( self.d1 )

    def gamma( self ):
        return derivative( self._N, self.d1, dx=1e-6 ) / ( self.S_0 * self.volatility * sqrt( self.T ) )

    def vega( self ):
        return self.S_0 * sqrt( self.T ) * derivative( self._N, self.d1, dx=1e-6 )

    def theta( self ):
        return self.volatility * self.S_0 * derivative( self._N, self.d1, dx=1e-6 ) / ( 2 * sqrt( self.T ) ) + self.r * self.K * exp( -1 * self.r * self.T ) * self._N( self.d2 )

    def rho( self ):
        return self.T * self.K * exp( -1 * self.r * self.T ) * self._N( self.d2 )
if __name__ == '__main__':
    print(BlackScholes(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13).getPrice())