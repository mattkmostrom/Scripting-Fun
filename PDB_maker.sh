###This is a script with some automated commands and instructions to make a PDB compatible with MPMC

# First, make the first two columns
for var in `seq 1 [number of atoms]`; do echo "ATOM"; done | tee col1
for var in `seq 1 [number of atoms]`; do echo $var; done | tee col2
paste col1 col2 > 2col.pdb

# Then XYZ parameters (make sure not to include the forst two lines of a standard .xyz file)
cat LxWxH.xyz | awk '{printf(%3s %3s %s %i %10lf %10lf %10lf %3s\n",$1,"MOF","F","1",$2,$3,$4,$1"XX")}' > next.pdb
paste 2col.pdb next.pdb > temp.pdb

# Element-Specific L-J Parameters
cat temp.pdb | sed s/"[Element Label (e.g. H1,etc)]"XX/[mass,charge,st. pol.,eps,sig]/g > temp2.pdb

# Insert your sorbate gas at the bottom of the file with the following columns:
# "ATOM" atom_number atom_ID molecule_name "M" molecule_number x y z mass(amu) charge(e) st._pol.(A^3 (a.u.^3 -> A^3 (0.529))) eps(a.u. (503.2195737)) sig(a.u. (1/(2)^(1/6)) omega gwp_alpha C6 C8 C10 C9

# I put some conversion factors from the units used the Rappe's forcefield to a.u. units used in MPMC, as well as from a.u. to A^3 for static polarizability

