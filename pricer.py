from math import sqrt, pow, exp
from functools import lru_cache


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



def binomial_tree(S_0, K, T, r, volatility, N):

    delta_t = T / N
    u = 1 + volatility * sqrt(delta_t)
    d = 1 - volatility * sqrt(delta_t)
    p = ( exp( r * delta_t ) - d ) / ( u - d )

    c = {}

    @lru_cache(9999)
    def S( j, m ):
        return S_0 * pow( u, j ) * pow( d, m - j )

    def C( j, n ):

        if n == N - 1:
            c_1 = max( S(j+1, n+1) - K, 0 )
            c_2 = max( S(j, n+1) - K, 0)
        else:
            c_1 = c[ (j+1, n+1) ]
            c_2 = c[ (j, n+1) ]

        return exp(-1 * r * delta_t) * (p * c_1 + (1 - p) * c_2)


    for n in reversed( range( N ) ):
        for j in reversed( range( n+1 ) ):
            c[ (j, n) ] = C(j, n)

    return C(0, 0)

def main():
    print(binomial_tree(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300))
    print(recursive_binomial_tree(S_0=60, K=62, T=0.5, r=0.06, volatility=0.13, N=300))

