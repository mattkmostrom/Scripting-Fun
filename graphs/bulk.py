#!/usr/bin/python

from numpy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from scipy.interpolate import splrep, splev

noble_gas_x = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
small_mol_x = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]

he = [0.318361426499293, 0.286536616565405, 0.145192936559843, 0.263034759358292, 0.19010679850319, 0.295853862601106, 0.331768006342628, 0.475723927716085, 0.443596784005525, 0.44843184559711]
ne = [0.123616144566357, 0.089605734767027, 0.026028110359178, -0.299094058086867, -0.267248431960726, -0.346912202380964, -0.47904435746903, -0.503720455208645, -0.506031283138937, -0.519852515464558]
ar = [-0.451467805847427, -1.02363583309017, -1.25893029542382, -1.47380071651181, -1.46418406072107, -1.08851553135731, -0.811531531531543, -0.634429210280624, -0.278527458531717, -0.001564388821744]
kr = [-0.942142707679444, -1.78054652983943, -2.00390754069159, -0.884339294057694, 0.544199628351462, 1.37670315822635, 2.04066811909949, 2.42345544013122, 2.59790187007233, 2.66056770474342]
xe = [-1.29415957588989, -3.56248282360333, -4.83231959860839, -3.89864222087692, -2.40883262605193, -0.815280092295849, 0.114262033035344, 0.614989675763158, 1.07458710708578, 1.27923676651622]
h2 = [0.245109062289188, 0.315221317067299, 0.386195693718933, 0.395156851953772, 0.384443838739252, 0.403254373635921, 0.279998715602223, 0.243618196374104, 0.096702446571901, 0.047349364033035, -0.070744156890848, -0.091050988553597, -0.148235492293459, -0.233779017307856, -0.281024819855899, -0.281866583150641, -0.335941095260026, -0.312993755172673, -0.351045746803659, -0.329941860465123]
n2 = [0.549324129997101, 0.711061731824177, 0.720620509274547, 0.505180991122214, 0.332590234913577, 0.187427983034628, 0.013298811345158, -0.121219012963398, -0.28392281538395, -0.385761144270594, -0.5566353922609, -0.660158018188564, -0.782940416599402, -0.899058006941006, -1.01746171105257, -1.16833205226748, -1.23141043857158, -1.37502336885399, -1.44083441019013, -1.5442853233604]

# I fucked up the signs here, actually supposed to be (\rho-\rho_calc)/\rho
he = [-x for x in he]
ne = [-x for x in ne]
ar = [-x for x in ar]
kr = [-x for x in kr]
xe = [-x for x in xe]
h2 = [-x for x in h2]
n2 = [-x for x in n2]

fig, ax = plt.subplots(2,figsize=[6.4,6.4])

ax1, ax2 = ax

ax1.plot(small_mol_x, h2, color='m', zorder=1, marker="x", label="H$_2$")
ax1.plot(small_mol_x, n2, color='c', zorder=1, marker="x", label="N$_2$")

ax2.plot(noble_gas_x, he, color='k', zorder=1, marker="x", label="He")
ax2.plot(noble_gas_x, ne, color='g', zorder=1, marker="x", label="Ne")
ax2.plot(noble_gas_x, ar, color='r', zorder=1, marker="x", label="Ar")
ax2.plot(noble_gas_x, kr, color='y', zorder=1, marker="x", label="Kr")
ax2.plot(noble_gas_x, xe, color='b', zorder=1, marker="x", label="Xe")

ax1.set(xlabel=r'Pressure (atm)',ylabel=r'Relative Density Deviation (%)')
ax2.set(xlabel=r'Pressure (atm)',ylabel=r'Relative Density Deviation (%)')

ax1.set_ylim(-2.0,2.0)
ax1.set_xlim(0,10000)
ax1.xaxis.set_minor_locator(AutoMinorLocator())
ax1.yaxis.set_minor_locator(AutoMinorLocator())
ax1.tick_params(which='both', axis="x", direction="in")
ax1.tick_params(which='both', axis="y", direction="in")
ax1.tick_params(which='both', bottom=True, top=True, left=True, right=True)

ax2.set_ylim(-5.0,5.0)
ax2.set_xlim(50,500)
ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())
ax2.tick_params(which='both', axis="x", direction="in")
ax2.tick_params(which='both', axis="y", direction="in")
ax2.tick_params(which='both', bottom=True, top=True, left=True, right=True)

leg = ax1.legend(frameon=True,ncol=2,loc=1)
leg.get_frame().set_linewidth(0.0)
leg = ax2.legend(frameon=True,ncol=3)
leg.get_frame().set_linewidth(0.0)

plt.tight_layout()
plt.savefig('bulk.eps', format='eps')

#plt.show()


