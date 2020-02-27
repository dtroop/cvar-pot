import numpy as np
from scipy.stats import genpareto
import warnings

def get_excesses(x, threshold):
    exceedances = x[x > threshold]
    if len(exceedances) == 0:
        print("No data above threshold")
        return np.nan
    return exceedances - threshold

def gpdFit(x, threshold):
    y = get_excesses(x, threshold)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        shape, _, scale = genpareto.fit(y, floc=0)
    return shape, scale

def rgpd(n, shape, scale):
    # Random number generation for the GPD
    return genpareto.rvs(shape, 0, scale, n)

def pgpd(x, shape, scale):
    # CDF for the GPD
    return genpareto.cdf(x, shape, 0, scale)

def qgpd(p, shape, scale):
    # Quantile function for the GPD
    return genpareto.ppf(p, shape, 0, scale)

def cvar_gpd(alph, shape, scale):
    q = qgpd(alph, shape, scale)
    return (q+scale)*(1+shape*q/scale)**(-1/shape)/((1-alph)*(1-shape))

def var_evt(x, alph, Fu):
    u = np.quantile(x, Fu)
    xi, sig = gpdFit(x, u)
    return u + sig/xi * (((1-alph)/(1-Fu))**(-xi) - 1)

def cvar_evt(x, alph, Fu):
    u = np.quantile(x, Fu)
    xi, sig = gpdFit(x, u)
    if xi >= 1:
        print("No valid shape parameter found")
        return np.nan
    q = u + sig/xi * (((1-alph)/(1-Fu))**(-xi) - 1)
    return (q + sig - xi*u)/(1-xi)

def cvar_sa(x, alph):
	q = np.quantile(x, alph)
	y = x[x >= q]
	return np.mean(y)
