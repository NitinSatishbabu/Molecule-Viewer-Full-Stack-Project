import molecule

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500

radGrad = """<radialGradient id="norm" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                <stop offset="0%" stop-color="#ff0000"/>
                <stop offset="50%" stop-color="#ff0000"/>
                <stop offset="100%" stop-color="#ff0000"/>
             </radialGradient>"""

class Atom:
    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = c_atom.z


    def __str__(self):
        return "Element = {}, x: {}, y: {}, z: {}".format(self.atom.element, self.atom.x, self.atom.y, self.z)

    def svg(self):
        cx = self.atom.x * 100 + offsetx
        cy = self.atom.y * 100 + offsety
        # r = radius[self.atom.element]
        # fill = element_name[self.atom.element]

        if self.atom.element in element_name:
            r = radius[self.atom.element]
            fill = element_name[self.atom.element]
        else:
            r = 25
            fill = "norm"
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, fill)

class Bond:
    def __init__(self, c_bond):
        self.bond = c_bond
        self.z = c_bond.z

    def __str__(self):
        return "Bond = x1: {}, x2: {}, y1: {}, y2: {}, z: {}, len: {}, dx: {}, dy: {}".format(self.bond.x1, self.bond.x2, self.bond.y1, self.bond.y2, self.z, self.bond.len, self.bond.dx, self.bond.dy)

    def svg(self):
        x1_up = (self.bond.x1 * 100 + offsetx) + (self.bond.dy * 10)
        x1_down = (self.bond.x1 * 100 + offsetx) - (self.bond.dy * 10)

        y1_up = (self.bond.y1 * 100 + offsety) - (self.bond.dx * 10)
        y1_down = (self.bond.y1 * 100 + offsety) + (self.bond.dx * 10)

        x2_up = (self.bond.x2 * 100 + offsetx) + (self.bond.dy * 10)
        x2_down = (self.bond.x2 * 100 + offsetx) - (self.bond.dy * 10)

        y2_up = (self.bond.y2 * 100 + offsety) - (self.bond.dx * 10)
        y2_down = (self.bond.y2 * 100 + offsety) + (self.bond.dx * 10)

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1_up, y1_up, x1_down, y1_down, x2_down, y2_down, x2_up, y2_up)

class Molecule(molecule.molecule):
    def __str__(self):
        # return " Atom_max = {}, Atom_no = {}, Bond_max = {}, Bond_no = {}" % (molecule.atom_max, molecule.atom_no, molecule.bond_max, molecule.bond_no)
        for x in self.atom_max:
            print("atom {} = {}") % (x, self.atom[x])

        for y in self.bond_max:
            print("bond {} = {}") % (y, self.bond[y])

    def svg(self):
        # atoms_asc = sorted(self.molecule.atom, key=lambda x: x.z)
        # bonds_asc = sorted(self.molecule.bond, key=lambda x: x.z)

        # for x in range(self.molecule.atom_no):
        #     atom_l += self.molecule.get_atom(x)

        # for y in range(self.molecule.bond_no):
        #     bond_l += self.molecule.get_bond(y)

        svg_fstr = ""
        s_1 = self.atom_no
        s_2 = self.bond_no
        i, j = 0, 0

        while i < s_1 and j < s_2:
            atom_l = Atom(self.get_atom(i))
            bond_l = Bond(self.get_bond(j))
            if atom_l.z < bond_l.z:
                svg_fstr += atom_l.svg()
                i = i + 1

            else:
                svg_fstr += bond_l.svg()
                j = j + 1

        while i < s_1:
            atom_l = Atom(self.get_atom(i))
            svg_fstr += atom_l.svg()
            i = i + 1

        while j < s_2:
            bond_l = Bond(self.get_bond(j))
            svg_fstr += bond_l.svg()
            j = j + 1

        return header + radGrad +svg_fstr + footer

    def parse(self, file):

            file.readline()
            file.readline()
            file.readline()

            i_line = file.readline()
            aandb = i_line.split()
            total_atoms = int(aandb[0])
            total_bonds = int(aandb[1])

            for i in range(total_atoms):
                line = file.readline()
                split_l = line.split()

                x = float(split_l[0])
                y = float(split_l[1])
                z = float(split_l[2])
                element = split_l[3]

                self.append_atom(element, x, y, z)

            for j in range(total_bonds):
                line = file.readline()
                split_l = line.split()
                a_1 = int(split_l[0]) - 1
                a_2 = int(split_l[1]) - 1
                bond_type = int(split_l[2])

                self.append_bond(a_1, a_2, bond_type)
