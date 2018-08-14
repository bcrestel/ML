# -*- coding: utf-8 -*-
"""
Numerical experience to look at how to calculate statistics of periodic returns
given draws of the compounded returns
We assume the periodic returns are normal

Created on Fri Aug  3 12:58:31 2018

@author: bcrestel
"""

import numpy as np
import pandas as pd


# inputs
months = 20*12
mean = 0.0025
std = 0.02
samples = int(1e4)

distr_cumrtns = []
for ii in range(samples):
    rtns = pd.DataFrame(np.random.normal(mean, std, months))
    cumrtns = (1+rtns).cumprod()
    distr_cumrtns.append(cumrtns.iloc[-1].values[0])
    #rtns.plot()
    #cumrtns.plot()
distr_cumrtns = pd.DataFrame(distr_cumrtns)
distr_cumrtns.hist(bins=25)




print ('Compounded returns:')
mu_c = months*mean
var_c = months*std**2
E_c = np.exp(mu_c+0.5*var_c)
V_c = (np.exp(var_c)-1.0)*np.exp(2*mu_c+var_c)
print('Compounded returns: E={:.4f}, std={:.4f}'.format(E_c, np.sqrt(V_c)))
E_c_h = distr_cumrtns.mean().values[0]
V_c_h = distr_cumrtns.std().values[0]**2
print('Compounded returns (sampling estimate): E={:.4f}, std={:.4f}\n'.format(E_c_h, np.sqrt(V_c_h)))

# MLE of lognormal parameters (CORRECT)
mu_c_h = np.log(distr_cumrtns).sum().values[0]/float(samples)
var_c_h = ((np.log(distr_cumrtns)-mu_c_h)**2).sum().values[0]/float(samples-1)
print('Parameters of lognormal compounded returns: mu_c={:.4f}, std_c={:.4f}'.format(mu_c, np.sqrt(var_c)))
print('Parameters of lognormal compounded returns (sampling): mu_c={:.4f}, std_c={:.4f}\n'.format(mu_c_h, np.sqrt(var_c_h)))


print('Periodic returns:')
print('Periodic returns: mu={}, std={}'.format(mean, std))
mu_h1 = (E_c_h-1.0)/float(months)
var_h1 = V_c_h/float(months)
print('Periodic returns (sampling; using lognormal moments directly): mu={:.4f} ({:.2f}%), std={:.4f} ({:.2f}%)'\
      .format(mu_h1, 100*np.abs(mu_h1-mean)/mean, np.sqrt(var_h1), 100*np.abs(np.sqrt(var_h1)-std)/std))
mu_h2 = mu_c_h/float(months)
var_h2 = var_c_h/float(months)
print('Periodic returns (sampling; using parameters of lognormal): mu={:.4f} ({:.2f}%), std={:.4f} ({:.2f}%)'\
      .format(mu_h2, 100*np.abs(mu_h2-mean)/mean, np.sqrt(var_h2), 100*np.abs(np.sqrt(var_h2)-std)/std))
E_h = np.exp(mu_h2 + 0.5*var_h2)-1.0
V_h = (np.exp(var_h2)-1.0)*np.exp(2*mu_h2+var_h2)
print('Periodic returns (sampling; best): mu={:.4f} ({:.2f}%), std={:.4f} ({:.2f}%)'\
      .format(E_h, 100*np.abs(E_h-mean)/mean, np.sqrt(V_h), 100*np.abs(np.sqrt(V_h)-std)/std))



