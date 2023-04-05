import MolDisplay
import os
import sqlite3

class Database:
    def __init__(self, reset = False):
        if reset:
            os.remove('molecules.db')

        self.conn = sqlite3.connect('molecules.db')

    def create_tables(self): #Creating specified tables

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements (
                    ELEMENT_NO      INTEGER NOT NULL,
                    ELEMENT_CODE    VARCHAR(3) NOT NULL,
                    ELEMENT_NAME    VARCHAR(32) NOT NULL,
                    COLOUR1         CHAR(6) NOT NULL,
                    COLOUR2         CHAR(6) NOT NULL,
                    COLOUR3         CHAR(6) NOT NULL,
                    RADIUS          DECIMAL(3) NOT NULL,
             		PRIMARY KEY (ELEMENT_CODE) );""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Atoms (
                    ATOM_ID         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    ELEMENT_CODE    VARCHAR(3) NOT NULL,
                    X               DECIMAL(7,4) NOT NULL,
                    Y               DECIMAL(7,4) NOT NULL,
                    Z               DECIMAL(7,4) NOT NULL,
                    FOREIGN KEY(ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE));""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Bonds (
                    BOND_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    A1               INTEGER NOT NULL,
                    A2               INTEGER NOT NULL,
                    EPAIRS           INTEGER NOT NULL);""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Molecules (
                    MOLECULE_ID         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    NAME                TEXT UNIQUE NOT NULL);""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom (
                    MOLECULE_ID          INTEGER NOT NULL,
                    ATOM_ID              INTEGER NOT NULL,
                    PRIMARY KEY          (MOLECULE_ID, ATOM_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                    FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID));""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond (
                    MOLECULE_ID          INTEGER NOT NULL,
                    BOND_ID              INTEGER NOT NULL,
                    PRIMARY KEY          (MOLECULE_ID, BOND_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                    FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID));""" )


    def __setitem__( self, table, values ): # setting the elements table
        self.conn.execute("INSERT INTO %s VALUES %s;" % (table, str(values)))

        self.conn.commit()



    def add_atom( self, molname, atom ): # inserting into Atoms table
        atomEle = atom.atom.element
        atomX = atom.atom.x
        atomY = atom.atom.y
        atomZ = atom.atom.z

        self.conn.execute( """INSERT
                              INTO   Atoms ( ATOM_ID, ELEMENT_CODE, X, Y, Z )
                              VALUES    ( NULL, '%s', %.4f, %.4f, %.4f);""" % (atomEle, atomX, atomY, atomZ));

        self.conn.commit()

        val = self.conn.execute(""" SELECT ATOM_ID
                                    FROM   Atoms
                                    WHERE  ATOM_ID = last_insert_rowid(); """);

        id_atom = val.fetchone()[0];

        val2 = self.conn.execute(""" SELECT MOLECULE_ID
                                    FROM   Molecules
                                    WHERE  NAME = ?; """, (molname, ));

        id_mol = val2.fetchone()[0];

        self.conn.execute("""INSERT
                              INTO   MoleculeAtom (MOLECULE_ID, ATOM_ID)
                              VALUES    (%d, %d);""" % (id_mol, id_atom));

        self.conn.commit()



    def add_bond( self, molname, bond ): #inserting into Bonds table
        bond_A1 = bond.bond.a1
        bond_A2 = bond.bond.a2
        bond_Epairs = bond.bond.epairs


        self.conn.execute( """INSERT
                              INTO   Bonds (BOND_ID, A1, A2, EPAIRS)
                              VALUES    ( NULL, %d, %d, %d);""" % (bond_A1, bond_A2, bond_Epairs));
        self.conn.commit()

        val = self.conn.execute(""" SELECT BOND_ID
                                    FROM   Bonds
                                    WHERE  BOND_ID = last_insert_rowid(); """);

        id_bond = val.fetchone()[0];

        val2 = self.conn.execute(""" SELECT MOLECULE_ID
                                    FROM   Molecules
                                    WHERE  NAME = '%s'; """ % (molname));

        id_mol = val2.fetchone()[0];


        self.conn.execute("""INSERT
                              INTO   MoleculeBond (MOLECULE_ID, BOND_ID)
                              VALUES    (%d, %d);""" % (id_mol, id_bond));
        self.conn.commit()


    def add_molecule( self, name, fp ): # inserting molecules in Molecules table
        MolObj = MolDisplay.Molecule()
        MolObj.parse(fp)
        self.conn.execute("""INSERT
                             INTO   Molecules (MOLECULE_ID, NAME)
                             VALUES    (NULL, '%s');""" % (name));
        self.conn.commit()

        for i in range (MolObj.atom_no):
            self.add_atom(name, MolDisplay.Atom(MolObj.get_atom(i)))

        for j in range (MolObj.bond_no):
            self.add_bond(name, MolDisplay.Bond(MolObj.get_bond(j)))

# Test
# if __name__ == "__main__":
#     db = Database(reset=True);
#     db.create_tables();
#     db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
#     db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
#     db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
#     db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
#     fp = open( 'water.sdf' );
#     db.add_molecule( 'Water', fp );
#     fp = open( 'caffeine.sdf' );
#     db.add_molecule( 'Caffeine', fp );
#     fp = open( 'CID.sdf' );
#     db.add_molecule( 'Isopentanol', fp );
# # display tables
#     print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
#     print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
#     print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
#     print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
#     print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
#     print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );



    def load_mol( self, name ): # returning an object containg atoms and bonds
        MolObj = MolDisplay.Molecule()

        val = self.conn.execute(""" SELECT Atoms.ELEMENT_CODE, Atoms.X, Atoms.Y, Atoms.Z
                                    FROM   Atoms
                                    INNER JOIN MoleculeAtom
                                    ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                                    INNER JOIN Molecules
                                    ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
                                    WHERE Molecules.NAME = '%s'
                                    ORDER BY Atoms.ATOM_ID ASC;""" % (name));

        req = val.fetchall()

        length = len(req)
        for i in range(length):
            MolObj.append_atom(req[i][0], req[i][1], req[i][2], req[i][3])


        val2 = self.conn.execute(""" SELECT Bonds.A1, Bonds.A2, Bonds.EPAIRS
                                    FROM   Bonds
                                    INNER JOIN MoleculeBond
                                    ON Bonds.BOND_ID = MoleculeBond.BOND_ID
                                    INNER JOIN Molecules
                                    ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
                                    WHERE Molecules.NAME = '%s'
                                    ORDER BY Bonds.BOND_ID ASC;""" % (name));

        req2 = val2.fetchall()

        length2 = len(req2)
        for j in range(length2):
            MolObj.append_bond(req2[j][0], req2[j][1], req2[j][2])

        return MolObj

    def radius( self ): # returning a radius dictionary

        val = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements;")
        req3 = val.fetchall()
        length = len(req3)

        dictionary = {}
        for i in range(length):
            dictionary.update({req3[i][0]:req3[i][1]})

        return dictionary


    def element_name( self ): # returning an element name dictionary
        val = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements;")
        req4 = val.fetchall()
        length = len(req4)

        dictionary = {}
        for i in range(length):
            dictionary.update({req4[i][0]:req4[i][1]})

        return dictionary


    def radial_gradients( self ): # returning string with values from Elements table
        val = self.conn.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements;")
        req5 = val.fetchall()
        length = len(req5)
        retstr = ""

        for i in range(length):
            retstr += """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                            <stop offset="0%%" stop-color="#%s"/>
                            <stop offset="50%%" stop-color="#%s"/>
                            <stop offset="100%%" stop-color="#%s"/>
                         </radialGradient>""" % (req5[i][0], req5[i][1], req5[i][2], req5[i][3]);

        return retstr
#
# if __name__ == "__main__":
#     db = Database(reset=True); # or use default
#     db.create_tables();
#     MolDisplay.radius = db.radius();
#     MolDisplay.element_name = db.element_name();
#     MolDisplay.header += db.radial_gradients();
#     for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
#         mol = db.load_mol( molecule );
#         mol.sort();
#         fp = open( molecule + ".svg", "w" );
#         fp.write( mol.svg() );
#         fp.close();
