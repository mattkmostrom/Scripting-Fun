#!/usr/bin/env python3
import itertools
import numpy as np
import os

#This script will print out the many-body interactions tuple-wise for n interacting atoms
#should be run in a directory with the output of "exporter.sh" and with directories of the distances considered
#results of exporter.sh look like lists with a header of the distance followed by a list of lists with structure: (tuple,corr_qz,corr_tz,HF_qz)

#For example:
#5.75
#1 -0.041011618 -0.039414559 -2.861521998
#2 -0.082029889 -0.078838793 -5.723045158


f = np.array(open("configuration_energies.dat").readlines())

# distances present are assumed to be subdirectories in the directory the script is called from
available_distances = []
for name in os.listdir("."):
    if os.path.isdir(name):
        try:
            #if there is a non-float directory, ignore it (and hope to god all the directories parsable as floats are relevant simulation data)
            float(name)
            available_distances.append(name)
        except ValueError:
            pass

available_distances.sort() #fucking bash directory sorting bullshit

# split file into sublist for each available distance; exclude first item (it is the distance)
lists = [list(i[1:]) for i in np.split(f, len(available_distances))]

# ************************************************************
N_ATOMS = 7  # update me senpai
# ************************************************************

# list of labels, doesn't really matter what they are
# FIXME: breaks if there are more than 26 atoms
chr_list = [chr(i) for i in range(97, 97 + N_ATOMS)]
chr_str = "".join(chr_list)

# maps distance to label to list of energies at that label
master_data = {d: {} for d in available_distances}

for idx, dist in enumerate(lists):
    labels = (
        j for i in range(1, (N_ATOMS + 1)) for j in itertools.combinations(chr_str, i)
    )
    for line in dist:
        # label every line with an a,b, ab, acde, etc
        master_data[available_distances[idx]][next(labels)] = [
            float(i) for i in line.split()[1:]
        ]


for dist, data in master_data.items():
    # do extrapolation shit etc
    for k, v in data.items():
        try:
            qz_corr = v[0]
            tz_corr = v[1]
            first = (3 ** 3.05) * tz_corr
            first -= (4 ** 3.05) * qz_corr
            second = 3 ** 3.05 - 4 ** 3.05
            corr = first / second
            corr_SCF = v[2] + corr
            data[k] = [corr, corr_SCF]
        except IndexError:
            print(
                "fucked up data somewhere, exiting before completion of extrapolation loop"
            )
            import sys

            sys.exit()


for dist, data in master_data.items():
    for k, v in data.items():
        l = len(k)
        summed = 0
        for i in range(1, l):
            for j in itertools.combinations("".join(k), i):
                # energy at label abc is raw energy from abc - (a + b + c + ab + ac)
                summed += data[j][1]
        data[k][1] -= summed


answer = {d: [0] * (N_ATOMS + 1) for d in available_distances}
for dist, data in master_data.items():
    for k, v in data.items():
        # energy for 1-body is sum of all a,b,c etc
        answer[dist][len(k)] += data[k][1]

# dump data to console
for dist, row in sorted(answer.items()):
    print(f"{dist} ", end="")
    for i in row[1:]:
        print(f"{i} ", end="")
    print("")
