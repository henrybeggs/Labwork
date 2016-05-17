#!/usr/bin/python
import re, os, sys
"""
In order to make a polysaccharide for use in GROMACS, a PDB must be generated using a tool like "Carb-Builder"
Next, using PyMOL, create CONECT records using the command `set pdb_conect_all, on`
The file is now ready passed through the charmm-gui which will generate a new PDB and PSF file
The numbering must be altered so that the molecule is treated as a single residue...
    This is done by first running the POLY_SACH_PDB script to correctly number the pdb
Finally, using the PSF and the newly renumbered PDB, an RTP file can be generated for usage in GROMACS
"""

def generate_psf_dict(fin):
    title, psf_dict, items = None, {}, []
    with open(fin) as f:
        for i in f:
            pattern = re.match(r".*!N(\w+)", i)
            if pattern:
                psf_dict[title] = items
                title, items = pattern.group(1), []
                continue
            if title is not None:
                items.append(i.strip().split())
    return psf_dict

def atom_number_fixer(fin, fix):
    new = []
    with open(fix) as f:
        pdb, fd = [], []
        for i in f:
            pattern = re.match(r"(HETATM|ATOM)(.*)", i)
            if pattern:
                line = pattern.group(2).split()
                pdb.append(line)
        for j in fin['ATOM']:
            fd.append(j)
    for o, n in zip(fd, pdb):
        new_line = []
        new_line.append(o[0])
        new_line.append(o[1])
        new_line.append("1")
        new_line.append(n[2])
        new_line.append(n[1])
        for x in o[5:]:
            new_line.append(x)
        new.append(new_line)
    fin['ATOM'] = new
    return fin

def impropers(fd, at_dict):
    imps, iss = [], []
    try:
        for i in fd['IMPHI']:
            for j in i:
                iss.append(j)
                if len(iss) == 4:
                    imps.append(iss)
                    iss = []
    except KeyError:
        return False
    return [[at_dict[l] for l in k] for k in imps]

def remove_empties(fd):
    new_dict = {}
    for i, j in fd.items():
        if not empty_tree(j):
            new_dict[i] = j
    return new_dict

def exp_parser(exp):
    i = exp.split("E")
    if len(i) == 1:
        return float(i[0])
    return float(i[0]) * 10 ** float(i[1])

def empty_tree(input_list):
    """Recursively iterate through values in nested lists."""
    for item in input_list:
        if not isinstance(item, list) or not empty_tree(item):
             return False
    return True

def bond_fixer(bonds, atoms):
    bond_pairs, at_dict, new = [], {}, []
    for line in bonds:
        for x in range(0, len(line), 2):
            bond_pairs.append(line[x:x+2])
    for atom in atoms:
        at_dict[atom[0]] = atom[4]
    for pair in bond_pairs:
        new.append([at_dict[pair[0]], at_dict[pair[1]]])
    return [new, at_dict]

def write_out(fo, fd):
    count = 0
    with open(fo, "w+") as f:
        f.write("[ {} ]\n\n".format(fd['ATOM'][0][3]))
        f.write("  [ atoms ]\n")
        for atom in fd['ATOM']:
            f.write("\t{}{} {}".format(" "*(5-len(atom[4])), atom[4], atom[5]))
            exp = exp_parser(atom[6])
            f.write("{}{}".format(" "*(8-len(atom[5])), round(exp, 4)))
            f.write("{}{}\n".format(" "*(4-len(str(count))), count))
            count += 1
        f.write("  [ bonds ]\n")
        bonds, at_dict = bond_fixer(fd['BOND'], fd['ATOM'])
        for bond in bonds:
            f.write("\t{}{}".format(" "*(5-len(bond[0])), bond[0]))
            f.write("{}{}\n".format(" "*(6-len(bond[1])), bond[1]))
        imps = impropers(fd, at_dict)
        if imps:
            f.write("  [ impropers ]\n")
            for imp in imps:
                for x in range(4):
                    f.write("\t{}{}".format(" "*(4-len(imp[x])), imp[x]))
                f.write("\n")


def main():
    if len(sys.argv) < 3:
        print "USAGE | PSF_PARSE [path/to/psf] [path/to/pdb]"
        sys.exit()

    print "\n\nThis is a PDF_PARSER that will generate a correctly numbered and formatted .rtp file for use in GROMACS\n" \
          "The first file supplied must be the .psf file from **Charmm-GUI**\n" \
          "The second file supplied must be the correctly numbered and formatted .pdb for the atom in question\n\n"
    filein, pdb, fileout = sys.argv[1], sys.argv[2], os.path.dirname(sys.argv[1]) + "/hanks.rtp"
    file_dict = generate_psf_dict(filein)
    file_dict = atom_number_fixer(file_dict, pdb)
    file_dict = remove_empties(file_dict)
    write_out(fileout, file_dict)

if __name__ == '__main__':
    main()
