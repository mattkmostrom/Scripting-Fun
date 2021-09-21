#!/usr/bin/python

from numpy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from scipy.interpolate import splrep, splev

mue_phahst = [0.480921298250999, 0.647735521368268, 0.732278589888828, 0.797445174607282, 0.831002051224987, 0.802300650050844, 0.737784448517327, 0.952952619876513, 0.835778021482067, 0.675755852733675]
mue_lj_pol = [0.489897035966024, 0.831458207304431, 1.29578232955585, 1.42406274800196, 1.22409057599764, 1.56191012049862, 1.23170968404042, 1.73543870403081, 1.77971599682716, 1.54530633246127]
mue_lj = [0.463316005999636, 0.790300969032204, 1.2456060482908, 1.3958441933393, 1.16817552922599, 1.50469630024674, 1.19750596529137, 1.70705941445849, 1.71254795538702, 1.49846285393422]
mse_phahst = [-0.189435857491501, 0.116781641981304, 0.113553048134039, -0.042257584598894, 0.29955488665937, 0.267198738053375, -0.201966604302165, -0.20312369050518, 0.080708539504405, -0.322970699217541]
mse_lj_pol = [0.011269726387855, 0.324489113450006, 0.186363137687121, 0.351602065992494, 0.334891026281484, 0.245988773186753, 0.117673233649971, 0.178490060485629, 0.574811015552278, 0.130904796374836]
mse_lj = [-0.126875865660527, 0.262111631629933, 0.146543005244547, 0.363630882827102, 0.330002512631785, 0.216254093676975, 0.153472029972026, 0.218724669590594, 0.566100731569556, 0.064830036823922]

fig, ax = plt.subplots()
width = 0.25
N = 10
ind = arange(N)
plt.bar(ind, mse_phahst, width, label='PHAHST')
plt.bar(ind+width, mse_lj_pol, width, label='LJ+POL')
plt.bar(ind+2.*width, mse_lj, width, label='LJ')

plt.ylabel('Mean Signed Error (kJ/mol)')
plt.xticks(ind+width,(r'C$_2$H$_6$-C$_2$H$_6$-C$_2$H$_6$',r'C$_2$H$_6$-C$_2$H$_6$-C$_2$H$_4$',r'C$_2$H$_6$-C$_2$H$_6$-C$_2$H$_2$',r'C$_2$H$_6$-C$_2$H$_4$-C$_2$H$_4$',r'C$_2$H$_6$-C$_2$H$_4$-C$_2$H$_2$',r'C$_2$H$_6$-C$_2$H$_2$-C$_2$H$_2$',r'C$_2$H$_4$-C$_2$H$_4$-C$_2$H$_4$',r'C$_2$H$_4$-C$_2$H$_4$-C$_2$H$_2$',r'C$_2$H$_4$-C$_2$H$_2$-C$_2$H$_2$',r'C$_2$H$_2$-C$_2$H$_2$-C$_2$H$_2$'))
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axhline(c='k',lw=0.6)

ax.set_ylim(-0.4,0.6)

plt.legend()
plt.tight_layout()
plt.show()