from math import sqrt, pow, exp
from functools import lru_cache

class EuropeanCall(object):

    def __init__(self, S_0, K, T, r, volatility, N):

        self.S_0 = S_0
        self.K = K
        self.T = T
        self.r = r
        self.volatility = volatility
        self.N = N

        self.c = {}

        self.delta_t = self.T / self.N
        self.u = 1 + self.volatility * sqrt(self.delta_t)
        self.d = 1 - self.volatility * sqrt(self.delta_t)
        self.p = (exp(self.r * self.delta_t) - self.d) / (self.u - self.d)

    @lru_cache(999)
    def _S(self, j, m):
        return self.S_0 * pow(self.u, j) * pow(self.d, m - j)

    @lru_cache(999)
    def _C(self, j, n ):

        if n == self.N - 1:
            c_1 = max( self._S(j+1, n+1) - self.K, 0 )
            c_2 = max( self._S(j, n+1) - self.K, 0)
        else:
            c_1 = self.c[ (j+1, n+1) ]
            c_2 = self.c[ (j, n+1) ]

        return exp( -1 * self.r * self.delta_t ) * ( self.p * c_1 + ( 1-self.p ) * c_2 )

    def getPrice(self):
        for n in reversed(range(self.N)):
            for j in reversed(range(n + 1)):
                self.c[(j, n)] = self._C(j, n)

        return self._C(0,0)


class CoxRossRubinstein(EuropeanCall):

    def __init__(self, S_0, K, T, r, volatility, N):
        super().__init__(S_0, K, T, r, volatility, N)

        self.u = exp(self.volatility * sqrt(self.delta_t))
        self.d = 1 / self.u
        self.p = (exp(self.r * self.delta_t) - self.d) / (self.u - self.d)

class JarrowRudd(EuropeanCall):

    def __init__(self, S_0, K, T, r, volatility, N):
        super().__init__(S_0, K, T, r, volatility, N)

        m = (self.r - 1 / 2 * self.volatility ** 2) * self.delta_t
        self.u = exp( m + self.volatility * sqrt(self.delta_t))
        self.d = exp( m - self.volatility * sqrt(self.delta_t))
        self.p = .5


class AmericanCall(EuropeanCall):

    @lru_cache(999)
    def _C(self, j, n ):

        c_n = super()._C(j, n)
        return max( self._S(j, n) - self.K, c_n )


def recursive_binomial_tree(S_0, K, T, r, volatility, N):
    delta_t = T / N
    u = 1 + volatility * sqrt(delta_t)
    d = 1 - volatility * sqrt(delta_t)
    p = (exp(r * delta_t) - d) / (u - d)

    @lru_cache(999)
    def S(j, m):
        return S_0 * pow(u, j) * pow(d, m - j)

    @lru_cache(999)
    def Cn( j, n ):

        if n == N - 1 :
            c_1 = Cm( j+1, n+1 )
            c_2 = Cm( j, n+1 )
        else:
            c_1 = Cn( j+1, n+1 )
            c_2 = Cn( j, n+1 )

        return exp( -1 * r * delta_t ) * ( p * c_1 + ( 1-p ) * c_2 )

    @lru_cache(999)
    def Cm( j, m ):
        return max( S( j, m ) - K, 0 )

    return Cn(0, 0)



if __name__ == '__main__':
    print(EuropeanCall(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300).getPrice())
    print(CoxRossRubinstein(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300).getPrice())
    print(JarrowRudd(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300).getPrice())
    print(AmericanCall(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300).getPrice())
    print(recursive_binomial_tree(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300))
