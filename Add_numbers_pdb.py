import os, sys

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

newfile = os.path.dirname(fin) + "/" + os.path.basename(fin).split(".")[0] + "_new.pdb"

with open(newfile, "w") as fout:
    for line in new:
        print line
        j = line.split()
        fout.write("HETATM {}{}{}".format(j[1], " "*(5-len(j[1])), j[2]))
        fout.write("{}{}".format(" "*(5-len(j[2])), resname))
        fout.write("{}{}{}{}{}{}\n".format(" "*(13-len(resname)), j[5], " "*(8-len(j[5])), j[6], " "*(8-len(j[6])), j[7]))