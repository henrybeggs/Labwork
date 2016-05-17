#!/usr/bin/python

import os, sys

"""

For appropriate connectivity within the graphite sheet in GROMACS the Carbons and Hydrogens have to be numbered.
Only works if atoms of same type are grouped together.
"""

# Check if necessary info is provided, exit otherwise
if len(sys.argv) < 3:
    print "Usage | Add_numbers_pdb.py `path/to/file.pdb` `4-letterRESNAME`"
    sys.ext()


fin, resname = sys.argv[1], sys.argv[2]

count, atom, new = 0, None, []
with open(fin) as f:
    for i in f:
        j = i.split()
        try:
            if atom != j[2]:
                atom = j[2]
                count = 0
        except:
            continue
        lst = list(i)
        for k in lst:
            if k == atom:
                count += 1
                lst[lst.index(atom)] = atom + str(count)
                break
        new.append(''.join(lst))


# Altered file is saved in the same directory and "_new" added to name
newfile = os.path.dirname(fin) + "/" + os.path.basename(fin).split(".")[0] + "_new.pdb"

with open(newfile, "w") as fout:
    for line in new:
        print line
        j = line.split()
        fout.write("HETATM {}{}{}".format(j[1], " "*(5-len(j[1])), j[2]))
        fout.write("{}{}".format(" "*(5-len(j[2])), resname))
        fout.write("{}{}{}{}{}{}\n".format(" "*(13-len(resname)), j[5], " "*(8-len(j[5])), j[6], " "*(8-len(j[6])), j[7]))
