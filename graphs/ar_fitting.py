#!/usr/bin/python

from numpy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from scipy.interpolate import splrep, splev

x = [1.8,2.,2.2,2.4,2.6,2.8,3.,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.,4.1,4.2,4.3,4.4,4.5,4.6,4.8,5.,5.2,5.4,5.6,5.9,6.2,6.5,7.,7.5,8.,9.,10.,12.,15.]
ccsdtq = [98948.472,51406.2,25736.338,12404.62,5701.427,2439.023,912.136,502.756,235.724,66.058,-37.753,-97.643,-128.726,-141.366,-142.546,-136.953,-127.658,-116.63,-105.114,-93.849,-83.251,-73.536,-64.786,-50.128,-38.825,-30.207,-23.66,-18.674,-13.298,-9.643,-7.113,-4.432,-2.865,-1.911,-0.918,-0.479,-0.156,-0.04]
model = [213959.110330198,95452.3409834472,42068.3650764732,18188.0140331754,7615.59691140255,3008.68142095904,1051.86633559041,562.764054809361,256.488422306479,69.441070194201,-40.542706832456,-101.30081761044,-131.116495946217,-141.918350403241,-141.422793075782,-134.565661711727,-124.456682800453,-113.014062576613,-101.384994583764,-90.223162314433,-79.870936683825,-70.478233923134,-62.079419852725,-48.100390118113,-37.36290303615,-29.184542406062,-22.959679915162,-18.204364355637,-13.04589842824,-9.512465301863,-7.048787597335,-4.416909695019,-2.866740221974,-1.917636448819,-0.925040448175,-0.48394656896,-0.158848400786,-0.040975284464]


fig, ax = plt.subplots()

plt.plot(x,ccsdtq, color='r', zorder=1, lw=2.0, label='CCSDT(Q)')
plt.plot(x, model, "-.", color='b', zorder=2, alpha=1.0, lw=2.0, label='Model')

ax.set_ylim(-200,400)
ax.set_xlim(0,14)

ax.set(xlabel=r'Ar-Ar Distance ($\mathrm{\AA}$)',ylabel=r'Energy ($\mathrm{K}/k_\mathrm{B}$)')

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='both', axis="x", direction="in")
ax.tick_params(which='both', axis="y", direction="in")
ax.tick_params(which='both', bottom=True, top=True, left=True, right=True)

plt.legend()

plt.show()
