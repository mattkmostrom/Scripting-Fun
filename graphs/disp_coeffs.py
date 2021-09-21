#!/usr/bin/python

from numpy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from scipy.interpolate import splrep, splev

c6_x = [5.688, 19.857, 29.148, 44.139, 3.0712, 9.5667, 13.652, 19.916, 19.753, 28.009, 40.518, 93.161, 137.97, 201.27]
c6_y = [6.52580781744299, 20.4808846273299, 29.6291821027851, 44.3237021190694, 3.09391583822185, 9.71008265979235, 14.047333042254, 21.0140733271777, 20.5652842455435, 29.751280913601, 44.5063555349121, 93.3727392765148, 139.680719750437, 202.072593886455]

c8_x = [97.818, 442.13, 732.2, 1357.2, 36.175, 167.47, 279.99, 524.99, 390.12, 638.14, 1162.3, 2616.7, 4669.4, 7389.1]
c8_y = [106.01279305065, 449.360233131505, 721.731495384537, 1262.21205575767, 35.7059723183671, 151.348187171172, 243.085047133714, 425.123302819312, 382.944357315785, 615.058884335476, 1075.65589665097, 2607.07218158608, 4559.42127906602, 7323.02882009896]

c10_x = [2220.5, 12617., 23441., 51088., 545.08, 3701.1, 7256.6, 16674., 9335.2, 17658., 38978., 88260., 184250., 316030.]
c10_y = [2246.267454423, 12696.9515697273, 22600.4858930068, 45129.6756859608, 530.976609654324, 3001.32750628784, 5342.34218297555, 10667.8312697568, 8679.92758034305, 15450.2110017954, 30851.6823528313, 87331.8003364181, 174388.101428968, 310409.613253198]


fig, ax = plt.subplots(1,3)
ax1, ax2, ax3 = ax

ax1.plot([-2000,2000],[-2000,2000], color='0.0', zorder=0, lw=0.5)
ax2.plot([-20000,20000],[-20000,20000], color='0.0', zorder=0, lw=0.5)
ax3.plot([-2000000,2000000],[-2000000,2000000], color='0.0', zorder=0, lw=0.5)

ax1.scatter(c6_x,c6_y, color='b', zorder=1, alpha=0.5, lw=2.0, label='C6')
ax2.scatter(c8_x,c8_y, color='g', zorder=1, alpha=0.5, lw=2.0, label='C8')
ax3.scatter(c10_x,c10_y, color='r', zorder=1, alpha=0.5, lw=2.0, label='C10')

ax1.set_ylim(1,1000)
ax1.set_xlim(1,1000)

ax2.set_ylim(1,10000)
ax2.set_xlim(1,10000)

ax3.set_ylim(1,1000000)
ax3.set_xlim(1,1000000)

ax1.set_xscale('log')
ax1.set_yscale('log')

ax2.set_xscale('log')
ax2.set_yscale('log')

ax3.set_xscale('log')
ax3.set_yscale('log')

ax1.set(ylabel=r'Mixed Dispersion Coefficient')
ax2.set(xlabel=r'ab initio Dispersion Coefficient')

ax1.xaxis.set_minor_locator(AutoMinorLocator())
ax1.yaxis.set_minor_locator(AutoMinorLocator())
ax1.tick_params(which='both', axis="x", direction="in")
ax1.tick_params(which='both', axis="y", direction="in")
ax1.tick_params(which='both', bottom=True, top=True, left=True, right=True)

ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())
ax2.tick_params(which='both', axis="x", direction="in")
ax2.tick_params(which='both', axis="y", direction="in")
ax2.tick_params(which='both', bottom=True, top=True, left=True, right=True)

ax3.xaxis.set_minor_locator(AutoMinorLocator())
ax3.yaxis.set_minor_locator(AutoMinorLocator())
ax3.tick_params(which='both', axis="x", direction="in")
ax3.tick_params(which='both', axis="y", direction="in")
ax3.tick_params(which='both', bottom=True, top=True, left=True, right=True)

ax1.legend()
ax2.legend()
ax3.legend()

plt.show()



