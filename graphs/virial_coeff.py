#!/usr/bin/python

import os
import scipy.integrate as integrate
from numpy import *
import copy
import itertools
import math
from scipy.interpolate import splrep, splev

class Atom:
    def __init__(self,x,y,z,name,element,q,pol,eps,sig,c6,c8,c10):
        self.name = name
        self.element = element
        self.x = array([x,y,z])
        self.q = q*408.7816 # e to sqrt(K*A)
        self.pol = pol
        self.eps = eps
        self.sig = sig
        self.c6 = c6
        self.c8 = c8
        self.c10 = c10
        self.mu = array([0.,0.,0.])
        self.e_static = array([0.,0.,0.])
        self.e_induced = array([0.,0.,0.])

class Quaternion:
    def normalize(self):
        magnitude = sqrt(dot(self.x,self.x))
        self.x = self.x/magnitude

    def get_conjugate(self):
        result = Quaternion(-self.x[0],-self.x[1],-self.x[2],self.x[3])
        return result

    def axis_angle(self,x,y,z,degrees):
        angle = degrees/57.2957795
        magnitude = sqrt(dot(array([x,y,z]),array([x,y,z])))
        self.x[0] = x*sin(angle/2.0)/magnitude
        self.x[1] = y*sin(angle/2.0)/magnitude
        self.x[2] = z*sin(angle/2.0)/magnitude
        self.x[3] = cos(angle/2.0)

    def random_rotation(self):
        self.x[0] = random.random()*2.0-1.0
        sum = self.x[0]*self.x[0]
        self.x[1] = sqrt(1.0-sum)*(random.random()*2.0-1.0)
        sum += self.x[1]*self.x[1]
        self.x[2] = sqrt(1.0-sum)*(random.random()*2.0-1.0)
        sum += self.x[2]*self.x[2]
        self.x[3] = sqrt(1.0-sum)*(-1.0 if random.random()>0.5 else 1.0)

    def __init__(self,x,y,z,w):
        self.x = array([float(x),float(y),float(z),float(w)])

    def __mul__(self, other):
        x = self.x[3]*other.x[0] + other.x[3]*self.x[0] + self.x[1]*other.x[2] - self.x[2]*other.x[1]
        y = self.x[3]*other.x[1] + other.x[3]*self.x[1] + self.x[2]*other.x[0] - self.x[0]*other.x[2]
        z = self.x[3]*other.x[2] + other.x[3]*self.x[2] + self.x[0]*other.x[1] - self.x[1]*other.x[0]
        w = self.x[3]*other.x[3] - self.x[0]*other.x[0] - self.x[1]*other.x[1] - self.x[2]*other.x[2]
        result = Quaternion(x,y,z,w)
        return result

def rotate_3vector(x,q):
    vec = Quaternion(x[0],x[1],x[2],0.)
    result = vec * q.get_conjugate()
    result = q * result
    return array([result.x[0],result.x[1],result.x[2]])

def tt_damping(n,br):
    total = 1.0
    running_br = br
    for i in range(1,n+1):
        total += running_br / math.factorial(i)
        running_br *= br

    result = 1.0 - math.exp(-br) * total

    if (result > 0.000000001):
        return result
    else:
        return 0.0

def close_contact_check(molecules,e_cut):
    close_contact = False
    for i in range(len(molecules)):
        for j in range(i+1,len(molecules)):
            a = molecules[i]
            b = molecules[j]
            for atom_i in a:
                for atom_j in b:
                    if (atom_i.eps!=0.0 and atom_j.eps!=0.0):
                        r = math.sqrt(dot((atom_i.x-atom_j.x)*(atom_i.x-atom_j.x),[1.,1.,1.]))
                        eps = 2.0 * atom_i.eps * atom_j.eps / (atom_i.eps + atom_j.eps)
                        sig = 0.5 * ( atom_i.sig + atom_j.sig )
                        repulsion = 596.725194095 * 1.0 / eps * math.exp(-eps*(r-sig))
                        if (repulsion>e_cut):
                            close_contact = True
    return close_contact

def vdw(molecules):
    u = 0.0
    for i in range(len(molecules)):
        for j in range(i+1,len(molecules)):
            a = molecules[i]
            b = molecules[j]
            for atom_i in a:
                for atom_j in b:
                    if (atom_i.eps!=0.0 and atom_j.eps!=0.0):
                        r = math.sqrt(dot((atom_i.x-atom_j.x)*(atom_i.x-atom_j.x),[1.,1.,1.]))
                        r2 = r*r
                        r4 = r2*r2
                        r6 = r4*r2
                        r8 = r4*r4
                        r10 = r6*r4
                        r12 = r6*r6
                        eps = 2.0 * atom_i.eps * atom_j.eps / (atom_i.eps + atom_j.eps)
                        sig = 0.5 * ( atom_i.sig + atom_j.sig )
                        c6 = math.sqrt( atom_i.c6 * atom_j.c6 ) * 0.021958709 / (3.166811429 * 0.000001)
                        c8 = math.sqrt( atom_i.c8 * atom_j.c8 ) * 0.0061490647 / (3.166811429 * 0.000001)
                        c10 = math.sqrt( atom_i.c10 * atom_j.c10 ) * 0.0017219135 / (3.166811429 * 0.000001)
                        repulsion = 596.725194095 * 1.0 / eps * math.exp(-eps*(r-sig))
                        dispersion = -tt_damping(6,eps*r)*c6/r6 - tt_damping(8,eps*r)*c8/r8 - tt_damping(10,eps*r)*c10/r10
                        u += repulsion + dispersion
    return u

def elst(molecules):
    u = 0.0
    for mol in molecules:
        for atom in mol:
            atom.e_static = array([0.,0.,0.])
    for i in range(len(molecules)):
        for j in range(i+1,len(molecules)):
            a = molecules[i]
            b = molecules[j]
            for atom_i in a:
                for atom_j in b:
                    r = math.sqrt(dot((atom_i.x-atom_j.x)*(atom_i.x-atom_j.x),[1,1,1]))
                    q1 = atom_i.q
                    q2 = atom_j.q
                    u += q1*q2/r
                    atom_i.e_static += q2 * (atom_i.x-atom_j.x) / (r*r*r)
                    atom_j.e_static += q1 * (atom_j.x-atom_i.x) / (r*r*r)
    return u

def pol(molecules):
    iterations = 3
    u = 0.0
    N = 0
    atoms = []
    damp = 2.1304
    damp2 = damp*damp
    damp3 = damp2*damp
    for mol in molecules:
        for atom in mol:
            atom.mu = atom.pol * atom.e_static
            N += 1
            atoms.append(atom)
    A = zeros((3*N,3*N))
    for i in range(len(atoms)):
        for j in range(len(atoms)):
            if (i==j):
                if (atoms[i].pol!=0.):
                    A[3*i][3*i] = 1./atoms[i].pol
                    A[3*i+1][3*i+1] = 1./atoms[i].pol
                    A[3*i+2][3*i+2] = 1./atoms[i].pol
                else:
                    A[3*i][3*i] = 10000000000000000000000.
                    A[3*i+1][3*i+1] = 10000000000000000000000.
                    A[3*i+2][3*i+2] = 10000000000000000000000.
            else:
                r = math.sqrt(dot((atoms[i].x-atoms[j].x)*(atoms[i].x-atoms[j].x),[1,1,1]))
                r2 = r*r
                r3 = r2*r
                r5 = r3*r2
                x = atoms[j].x[0] - atoms[i].x[0]
                y = atoms[j].x[1] - atoms[i].x[1]
                z = atoms[j].x[2] - atoms[i].x[2]
                expr = math.exp(-damp*r)
                damping_term1 = 1. - expr*(0.5*damp2*r2 + damp*r + 1.)
                damping_term1 *= 1.0/r3
                damping_term2 = 1. - expr*(damp3*r3/6. + 0.5*damp2*r2 + damp*r + 1.)
                damping_term2 *= -3./r5
                A[3*i+0][3*j+0] = x*x*damping_term2 + damping_term1
                A[3*i+0][3*j+1] = x*y*damping_term2
                A[3*i+0][3*j+2] = x*z*damping_term2
                A[3*i+1][3*j+0] = y*x*damping_term2
                A[3*i+1][3*j+1] = y*y*damping_term2 + damping_term1
                A[3*i+1][3*j+2] = y*z*damping_term2
                A[3*i+2][3*j+0] = z*x*damping_term2
                A[3*i+2][3*j+1] = z*y*damping_term2
                A[3*i+2][3*j+2] = z*z*damping_term2 + damping_term1
    for iteration in range(iterations):
        for i in range(len(atoms)):
            atoms[i].e_induced = array([0.,0.,0.])
            for j in range(len(atoms)):
                if (i!=j):
                    atoms[i].e_induced[0] -= A[3*i+0][3*j]*atoms[j].mu[0] + A[3*i+0][3*j+1]*atoms[j].mu[1] + A[3*i+0][3*j+2]*atoms[j].mu[2]
                    atoms[i].e_induced[1] -= A[3*i+1][3*j]*atoms[j].mu[0] + A[3*i+1][3*j+1]*atoms[j].mu[1] + A[3*i+1][3*j+2]*atoms[j].mu[2]
                    atoms[i].e_induced[2] -= A[3*i+2][3*j]*atoms[j].mu[0] + A[3*i+2][3*j+1]*atoms[j].mu[1] + A[3*i+2][3*j+2]*atoms[j].mu[2]
            atoms[i].mu = atoms[i].pol * (atoms[i].e_static + atoms[i].e_induced)
    for i in range(len(atoms)):
        u += -0.5 * dot(atoms[i].mu,atoms[i].e_static)
    return u
    

def U(molecules):
    close_contact = close_contact_check(molecules,1e4)
    if (not close_contact):
        u = vdw(molecules)
        #print "vdw",u
        u += elst(molecules)
        #print "elst",u
        u += pol(molecules)
        #print "pol",u
        return u
    else:
        return 1e4

ethane = []
ethane.append(Atom(-0.762000,    0.000000,    0.000000, "C2H6", "C", -0.04722,0.69670,4.00769,  3.17248,   13.53161, 301.22670, 21554.47000))
ethane.append(Atom( 0.762000,    0.000000,    0.000000, "C2H6", "C", -0.04722,0.69670,4.00769,  3.17248,   13.53161, 301.22670, 21554.47000))
ethane.append(Atom(-1.155809,    1.015301,    0.000000, "H6C2", "H", 0.01574,0.47580,3.20240,  1.97467,    3.89683,  0.00000,  0.00000))
ethane.append(Atom(-1.155809,   -0.507650,    0.879276, "H6C2", "H", 0.01574,0.47580,3.20240,  1.97467,    3.89683,  0.00000,  0.00000))
ethane.append(Atom(-1.155809,   -0.507650,   -0.879276, "H6C2", "H", 0.01574,0.47580,3.20240,  1.97467,    3.89683,  0.00000,  0.00000))
ethane.append(Atom( 1.155809,    0.507650,    0.879276, "H6C2", "H", 0.01574,0.47580,3.20240,  1.97467,    3.89683,  0.00000,  0.00000))
ethane.append(Atom( 1.155809,    0.507650,   -0.879276, "H6C2", "H", 0.01574,0.47580,3.20240,  1.97467,    3.89683,  0.00000,  0.00000))
ethane.append(Atom( 1.155809,   -1.015301,    0.000000, "H6C2", "H", 0.01574,0.47580,3.20240,  1.97467,    3.89683,  0.00000,  0.00000))

ethylene = []
ethylene.append(Atom( 0.666,   0.000,   0.000, "C2H4", "C",-0.34772,1.63040,3.03860,  3.47290,   40.50952, 1325.41700, 56051.68000))
ethylene.append(Atom(-0.666,   0.000,   0.000, "C2H4", "C",-0.34772,1.63040,3.03860,  3.47290,   40.50952, 1325.41700, 56051.68000))
ethylene.append(Atom( 1.230,   0.921,   0.000, "H4C2", "H", 0.17386,0.19000,4.77867,  1.74237,    1.17702,  0.00000,  0.00000))
ethylene.append(Atom( 1.230,  -0.921,   0.000, "H4C2", "H", 0.17386,0.19000,4.77867,  1.74237,    1.17702,  0.00000,  0.00000))
ethylene.append(Atom(-1.230,   0.921,   0.000, "H4C2", "H", 0.17386,0.19000,4.77867,  1.74237,    1.17702,  0.00000,  0.00000))
ethylene.append(Atom(-1.230,  -0.921,   0.000, "H4C2", "H", 0.17386,0.19000,4.77867,  1.74237,    1.17702,  0.00000,  0.00000))

acetylene = []
acetylene.append(Atom( 0.605,   0.000,   0.000, "C2H2", "C",-0.29121,1.5514,3.06161,  3.40728,   39.44099, 1123.91000, 43535.55000))
acetylene.append(Atom(-0.605,   0.000,   0.000, "C2H2", "C",-0.29121,1.5514,3.06161,  3.40728,   39.44099, 1123.91000, 43535.55000))
acetylene.append(Atom( 1.665,   0.000,   0.000, "H2C2", "H", 0.29121,0.1448,4.71283,  1.71998,    0.76016,  0.00000,  0.00000))
acetylene.append(Atom(-1.665,   0.000,   0.000, "H2C2", "H", 0.29121,0.1448,4.71283,  1.71998,    0.76016,  0.00000,  0.00000))


h2 = []
h2.append(Atom( 0.000000, 0.000000, 0.000000, "H2DA", "DA", -0.846166,     0.0, 3.627796, 2.664506,      0.0,      0.0,       0.0))
h2.append(Atom( 0.371000, 0.000000, 0.000000,  "H2H",  "H",  0.423083, 0.34325, 3.100603, 1.859425, 2.884735, 38.97178, 644.95683))
h2.append(Atom(-0.371000, 0.000000, 0.000000,  "H2H",  "H",  0.423083, 0.34325, 3.100603, 1.859425, 2.884735, 38.97178, 644.95683))

n2 = []
n2.append(Atom( 0.0000, 0.000, 0.000, "N2DA", "DA",  0.94194,  0.00000,  0.000000,  0.000000, 0.0, 0.0, 0.0))
n2.append(Atom( 0.5507, 0.000, 0.000,  "N2N",  "N", -0.47103,  0.85092,  3.853680,  3.31513, 17.80503, 416.3235, 11924.913))
n2.append(Atom(-0.5507, 0.000, 0.000,  "N2N",  "N", -0.47103,  0.85092,  3.853680,  3.31513, 17.80503, 416.3235, 11924.913))
#n2.append(Atom( 0.600, 0.000, 0.000, "N2DA", "DA", -9.407736,  0.00000,  3.502523,  2.718495, 0.0, 0.0, 0.0))
#n2.append(Atom(-0.600, 0.000, 0.000, "N2DA", "DA", -9.407736,  0.00000,  3.502523,  2.718495, 0.0, 0.0, 0.0))

co2 = []
co2.append(Atom( 0.0000,   0.000,   0.000, "CO2", "C",  0.734213,  0.92373,  2.888020,  3.077050, 17.04946, 205.2651, 3027.3016))
co2.append(Atom( 1.1625,   0.000,   0.000, "O2C", "O", -0.367159,  0.73493,  4.507360,  3.133450, 15.37517, 328.2494, 8584.6787))
co2.append(Atom(-1.1625,   0.000,   0.000, "O2C", "O", -0.367159,  0.73493,  4.507360,  3.133450, 15.37517, 328.2494, 8584.6787))

he = []
he.append(Atom(0.,0.,0.,"He","He",0.,0.2002,4.68451,2.38376,1.407164,11.13635,107.964))

ne = []
ne.append(Atom(0.,0.,0.,"Ne","Ne",0.,0.3823,4.99432,2.80240,6.212746,67.98647,911.376))

ar = []
ar.append(Atom(0.,0.,0.,"Ar","Ar",0.,1.655,3.88525,3.68623,65.46,1438.9,38745.))

kr = []
kr.append(Atom(0.,0.,0.,"Kr","Kr",0.,2.4970,3.528942,4.034770,130.1,3981.,149225.))

xe = []
xe.append(Atom(0.,0.,0.,"Xe","Xe",0.,4.026,3.24691,4.47518,288.4,11390.,551047.))

def integrand(r,molecule,temperature,N,qm="no",mass=0.):
    averages = zeros(3) # 0 = pair potential 1 = first deriv 2 = second deriv
    points = 0
    for i in range(N):
        q1 = Quaternion(0,0,0,1)
        q1.random_rotation()
        q2 = Quaternion(0,0,0,1)
        q2.random_rotation()
        a = copy.deepcopy(molecule)
        b = copy.deepcopy(molecule)
        for atom in a:
            atom.x = rotate_3vector(atom.x,q1)
        for atom in b:
            atom.x = rotate_3vector(atom.x,q2)
            atom.x += array([r,0.,0.])
        u = zeros(5)
        derivs = zeros(2)
        u[2] = U([a,b])
        if qm=="yes":
            dx = 1e-3
            for atom in b:
                atom.x -= array([dx,0.,0.])
            u[1] = U([a,b])
            for atom in b:
                atom.x -= array([dx,0.,0.])
            u[0] = U([a,b])
            for atom in b:
                atom.x += array([3.*dx,0.,0.])
            u[3] = U([a,b])
            for atom in b:
                atom.x += array([dx,0.,0.])
            u[4] = U([a,b])
            derivs[0] = 1./12.*u[0]-2./3.*u[1]+2./3.*u[3]-1./12.*u[4]
            derivs[1] = -1./12.*u[0]+4./3.*u[1]-5./2.*u[2]+4./3.*u[3]-1./12.*u[4]
            derivs /= dx
            #print r, u[0], u[1], u[2], u[3], u[4], derivs[0], derivs[1]
        averages[0] += exp(-u[2]/temperature)
        averages[1] += derivs[0]
        averages[2] += derivs[1]
        points += 1
    averages /= points
    return_val = 0.
    if qm=="yes":
        return_val = -0.5*(averages[0]-1.-1.054571817e-34*1.054571817e-34/(12.*mass*1.66054e-27*temperature*temperature*1.380649e-23*1.380649e-23)*averages[0]*1.380649e-23*1e20*(averages[2]+2.*averages[1]/r))*4.*math.pi*r*r
    else:
        return_val = -0.5*(averages[0]-1.)*4.*math.pi*r*r
    return return_val

'''
x = linspace(2,10,81)
y = []
for r in x:
        a = copy.deepcopy(he)
        b = copy.deepcopy(he)
        for atom in b:
            atom.x += array([r,0.,0.])
        y.append(U([a,b]))
spline = splrep(x,y)
spline_y = splev(x,spline)
spline_y1 = splev(x,spline,1)
spline_y2 = splev(x,spline,2)

for i in range(len(x)):
    print x[i], y[i], spline_y[i], spline_y1[i], spline_y2[i]


x = []
y = []
for temp in (5,6,7,8,9,10,12.5,15,17.5,20,25,30,40,57.5,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(he,temp,1,"yes",4.002602), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "he_x =",x
print "he_y =",y

x = []
y = []
for temp in (20,21,22,23,24,25,27.5,30,35,40,50,60,70,80,90,107.5,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(ne,temp,1), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "ne_x =",x
print "ne_y =",y
x = []
y = []
for temp in (25,50,75,100,110,120,130,140,150,160,170,180,190,200,210,220,230,245,260,280,300,320,340,360,380,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(ar,temp,1), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "ar_x =",x
print "ar_y =",y
x = []
y = []
for temp in (25,50,75,100,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,307.5,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(kr,temp,1), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "kr_x =",x
print "kr_y =",y
x = []
y = []
for temp in (25,50,75,100,125,150,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,407.5,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(xe,temp,1), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "xe_x =",x
print "xe_y =",y
'''
'''
x = []
y = []
for temp in (20,21,22,23,24,25,27.5,30,35,40,50,60,70,80,90,107.5,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(h2,temp,3000), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "h2_x =",x
print "h2_y =",y
x = []
y = []
for temp in (25,50,75,100,110,120,130,140,150,160,170,180,190,200,210,220,230,245,260,280,300,320,340,360,380,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,900,1000,1100,1200,1300,1400):
    x.append(temp)
    y.append((integrate.quad(integrand, 1.5, inf, args=(n2,temp,3000), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23)
print "n2_x =",x
print "n2_y =",y
'''
'''
print "CO2"
#250,255,260,265,270,273.15,275,
for temp in (280,285,290,295,300,310,320,330,340,350,360,370,373.15,380,390,400,410,420,430,440,450,460,480,500,520,540,560,580,600,620,640,680,700,714.81,750,800,850,900,950,1000):
    print temp,(integrate.quad(integrand, 1.5, inf, args=(co2,temp,10000), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23

'''

print "ethane"
#250,255,260,265,270,273.15,275,
for temp in (280,285,290,295,300,310,320,330,340,350,360,370,373.15,380,390,400,410,420,430,440,450,460,480,500,520,540,560,580,600,620,640,680,700,714.81,750,800,850,900,950,1000):
    print temp,(integrate.quad(integrand, 1.5, inf, args=(ethane,temp,500), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23

print "ethylene"
#250,255,260,265,270,273.15,275,
for temp in (280,285,290,295,300,310,320,330,340,350,360,370,373.15,380,390,400,410,420,430,440,450,460,480,500,520,540,560,580,600,620,640,680,700,714.81,750,800,850,900,950,1000):
    print temp,(integrate.quad(integrand, 1.5, inf, args=(ethylene,temp,500), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23

print "acetylene"
#250,255,260,265,270,273.15,275,
for temp in (280,285,290,295,300,310,320,330,340,350,360,370,373.15,380,390,400,410,420,430,440,450,460,480,500,520,540,560,580,600,620,640,680,700,714.81,750,800,850,900,950,1000):
    print temp,(integrate.quad(integrand, 1.5, inf, args=(acetylene,temp,500), epsabs=1e0, epsrel=1e0)[0]+2./3.*math.pi*1.5**3)*1e-8*1e-8*1e-8*6.022140857e23



