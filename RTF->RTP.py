import sys, os

def file_fixer(filein):
    fin = filein[1].strip()
    if not os.path.exists(fin):
        return False
    if len(filein[2]) != 4:
        return False
    return fin, filein[2].upper()

def remove_crap(filein, resname):
    fileout = os.path.dirname(filein) + "/" + os.path.basename(filein).split(".")[0] + ".rtp"
    fout = open(fileout, 'w')
    fout.write("[ {} ]\n".format(resname))
    fout.write(" [ atoms ]\n")
    with open(filein) as f:
        count = 0
        for i in f:
            if "ATOM" in i:
                j = i.split()
                fout.write("\t{}{} {}{}{}  {}\n".format(" "*(5-len(j[1])), j[1], j[2], " "*(12-len(j[2])), j[3], count))
                count += 1
            if "BOND" in i:
                if count > 0:
                    fout.write(" [ bonds ]\n")
                    count = 0
                j = i.split()
                fout.write("{}{}{}{}\n".format(" "*(13-len(j[1])), j[1], " "*(6-len(j[2])), j[2]))

def main():
    if len(sys.argv) < 3:
        print "Usage  |  RTF->RTP 'path/to/file' '4 char Residue Name'"
        sys.exit()
    else:
        filein, resname = file_fixer(sys.argv)
        if filein is False:
            print "Invalid filepath or residue name"
            sys.exit()
    remove_crap(filein, resname)

if __name__ == '__main__':
    main()