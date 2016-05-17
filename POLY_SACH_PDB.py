#!/usr/bin/python

import sys, os, re

"""
In order for GROMACS to read a polysaccharide.pdb file, an `rtp` entry must first be added to the merged.rtp
This first step renumbers the atoms of the polysaccharide and lists them as one residue, this allows for downstream usage in CHARMM_GUI and PSF_PARSE.py
"""
def args_parse(path):
    # This function ensures that the first argument is a valid filepath
    path = path.strip()
    if os.path.isfile(path):
        return path
    else:
        args_parse(raw_input("Invalid filepath in first arg. Please re-enter the path to file.\n"))

def max_c(fin):
    # Returns a dictionary of lists containing appropriate values for the carbons in a particular chain
    res_dict, chain, cs = {}, 1, set()
    with open(fin, 'r') as f:
        for i in f:
            line = i.split()
            try:
                del line[4]
            except:
                pass
            if "ATOM" not in line[0]:
                continue
            if chain != int(line[4]):
                res_dict[chain] = cs
                chain = int(line[4])
            pattern = re.match(r"C(\d+)", line[2])
            if pattern:
                cs.add(int(pattern.group(1)))
    res_dict[chain] = cs
    n = [i * max(res_dict[i+1]) for i in [j for j in range(0, len(res_dict))]]
    real = {}
    for k, o in zip(res_dict, n):
        real[k] = []
        for l in res_dict[k]:
            real[k] += [l + o]
    return real

def atom_fixer(fin, cd, name):
    atoms = []
    with open(fin, 'rU') as f:
        for i in f:
            line = i.split()
            try:
                del line[4]
            except:
                pass
            if line[0] != 'ATOM':
                continue
            try:
                iterator = max(cd[int(line[4])-1])
            except:
                iterator = 0
            newline = []
            for j in re.split(r"(\D+)(\d+)", line[2]):
                if j.isdigit():
                    if len(j) > 1:
                        newline.append(str(int(j[0])+iterator))
                        newline.append(j[1:])
                        continue
                    else:
                        j = int(j)
                        j += iterator
                newline.append(str(j))
            atno = ''.join(newline)
            line[0], line[2], line[3] = 'HETATM',atno, name
            atoms.append(line)
    return atoms

def writeout(fin, fout, atoms):
    count = 0
    fo = open(fout, 'w')
    with open(fin) as fi:
        for i in fi:
            if 'ATOM' not in i:

                fo.write(i)
                # Write this line as is
            else:
                if count == 0:
                    for atom in atoms:
                        print atom
                        fo.write("{}{}".format(atom[0], atom[1]))
                        fo.write("{}{}".format(" " * (6-len(atom[1])), atom[2]))
                        fo.write("{}{}".format(" " * (5-len(atom[2])), atom[3]))
                        fo.write("{}{}".format(" " * (8-len(atom[3])), 1))
                        fo.write("{}{}".format(" " * (12-len(atom[5])), atom[5]))
                        fo.write("{}{}".format(" " * (8-len(atom[6])), atom[6]))
                        fo.write("{}{}".format(" " * (8-len(atom[7])), atom[7]))
                        fo.write("\n")
                    count += 1

def main():
    if not len(sys.argv) > 2:
        print "Usage | poly_pdb `path/to/file` `New 4-letter name`"
        sys.exit()
    else:
        filein = args_parse(sys.argv[1])
        carbon_dict = max_c(filein)
        atom = atom_fixer(filein, carbon_dict, sys.argv[2])
        fileout = os.path.basename(filein).split('.')
        fileout.insert(1, "_fixedatoms")
        fileout = os.path.dirname(os.path.realpath(filein)) + "/" + ''.join(fileout[:-1]) + ".pdb"
        print fileout
        writeout(filein, fileout, atom)

if __name__ == '__main__':
    main()
