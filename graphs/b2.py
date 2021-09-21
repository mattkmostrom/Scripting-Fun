#!/usr/bin/python

from numpy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from scipy.interpolate import splrep, splev


he_x = []
he_y = []

he_x = []
he_y = []

ne_x = []
ne_y = []

ar_x = []
ar_y = []

kr_x = []
kr_y = []

xe_x = []
xe_y = []

h2_x = []
h2_y = []

n2_x = []
n2_y = []

fig, ax = plt.subplots(2, 1, sharex=False, sharey=False,figsize=[6.4,6.4])
#gridspec_kw={'wspace': 0}

ax1 = ax

ax1.plot(h2_exp_x1, h2_exp_y1, color='m', zorder=11, label="H$_2$ exp.")
ax1.plot(n2_exp_x1, n2_exp_y1, color='c', zorder=13, label="N$_2$ exp.")

ax1.scatter(h2_x, h2_y, s=20, facecolors='none', edgecolors='m', zorder=12, label="H$_2$ sim.")
ax1.scatter(n2_x, n2_y, s=20, facecolors='none', edgecolors='c', zorder=14, label="N$_2$ sim.")

ax1.set(xlabel=r'Temperature (K)',ylabel=r'B$_2$ (cm$^3$/mol)')

ax1.set_ylim(-200,25)
ax1.set_xlim(0,600)
#ax1.xaxis.set_major_locator(MaxNLocator(nbins=6,prune=None))
ax1.xaxis.set_minor_locator(AutoMinorLocator())
ax1.yaxis.set_minor_locator(AutoMinorLocator())
ax1.tick_params(which='both', axis="x", direction="in")
ax1.tick_params(which='both', axis="y", direction="in")
ax1.tick_params(which='both', bottom=True, top=True, left=True, right=True)

leg = ax1.legend(frameon=True,ncol=2,loc=4)
leg.get_frame().set_linewidth(0.0)

plt.tight_layout()
plt.savefig('b2.eps', format='eps')

#plt.show()


