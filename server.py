import sys
import MolDisplay
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import urllib
import molsql
import molecule

home_files = ['/home_page.html', '/home_page.css', '/element_page.html', '/element_page.css', '/element_page.js', '/remove_page.js', '/sdf_page.html', '/sdf_page.css', '/sdf_page.js','/sdfname.html', '/sdfname.js', '/display.js', '/display.css', 'sdfname.css','/remove_page.css']

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if self.path in home_files:   # make sure it's a valid file
              self.send_response( 200 );  # OK
              self.send_header( "Content-type", "text/html" );
              fp = open( self.path[1:] );
              page = fp.read();
              fp.close();
              self.send_header( "Content-length", len(page) );
              self.end_headers();

              self.wfile.write( bytes( page, "utf-8" ) );



        elif self.path == "/remove_page.html":
             self.send_response( 200 );  # OK
             self.send_header( "Content-type", "text/html" );
             fp = open( self.path[1:] );
             page = fp.read();


             db = molsql.Database(reset = False);
             db.create_tables();
             ele = db.conn.execute("SELECT ELEMENT_CODE FROM Elements")

             # elements = [row[0] for row in c.fetchall()]
             #
             options = '<select id="element_select" name="element_select">'
             for element in ele:
                 options += '  <option value="' + element[0] + '">' + element[0] + '</option>'

             print(options)
             page = page.replace('<select id="element_select" name="element_select">', options)
             # print(page)
             fp.close();

             self.send_header( "Content-length", len(page) );
             self.end_headers();

             self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/display.html":
                self.send_response( 200 );  # OK
                self.send_header( "Content-type", "text/html" );
                fp = open( self.path[1:] );
                page = fp.read();


                db = molsql.Database(reset = False);
                db.create_tables();
                mol = db.conn.execute("SELECT * FROM Molecules")
                molfet = mol.fetchall()
                # options = '<select id="mol_select" name="mol_select">'

                valuesstr = ""
                if len(molfet) != 0:
                    for i in molfet:

                        # mol_id = db.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?", (i,))
                        atomcount = db.conn.execute("SELECT ATOM_ID FROM MoleculeAtom WHERE MOLECULE_ID = ?", (i[0],))
                        fatmc = atomcount.fetchall()

                        bondcount = db.conn.execute("SELECT BOND_ID FROM MoleculeBond WHERE MOLECULE_ID = ?", (i[0],))
                        fbndc = bondcount.fetchall()

                        valuesstr += '  <option value="' + i[1] + '">' + i[1] + " Atoms = "+ str(len(fatmc)) +" Bonds = "+ str(len(fbndc)) +"</option>"

                    selectstr = '<select id="mol_select" name="mol_select">{}</select>'.format(valuesstr)
                    page = page.replace('<select id="mol_select" name="mol_select"></select>', selectstr)

                # for mols in molfet:
                #
                #     options += '  <option value="' + mols[0] + '">' + mols[0] + "Atoms = "+ len_acount + "Bonds" + len_bcount +"</option>"
                #
                # page = page.replace('<select id="mol_select" name="mol_select">', options)
                # print(page)
                fp.close();

                self.send_header( "Content-length", len(page) );
                self.end_headers();

                self.wfile.write( bytes( page, "utf-8" ) );

        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

    def do_POST(self):

        if self.path == "/sdf_upload.html":
            # code to handle sdf_upload
            db = molsql.Database(reset = False)
            content_length = int(self.headers['Content-Length'])

            fobj = io.TextIOWrapper(io.BytesIO(self.rfile.read(content_length)))
            fobj.readline()
            fobj.readline()
            fobj.readline()
            fobj.readline()

            db.add_molecule('Some', fobj)
            db.conn.close()

            self.send_response(302)
            self.send_header('Location', '/sdfname.html')
            self.end_headers();


            # molecule = MolDisplay.Molecule();
            # for i in range(0,4):    # skip 4 lines
            #     string = next(self.rfile);
            #
            #
            #
            # content_length = int(self.headers['Content-Length'])
            # post_data = self.rfile.read(content_length).decode('utf-8')
            # print(post_data)
            # name = post_data.split("=")[-1]
            # # print(name)
            #
            # # molsql.add_molecule( self.rfile, name);
            #
            # message = "sdf file uploaded to database with name: " + name;
            #
            # self.send_response( 200 ); # OK
            # self.send_header( "Content-type", "text/plain" );
            # self.send_header( "Content-length", len(message) );
            # self.end_headers();

            # self.wfile.write( bytes( message, "utf-8" ) );

        elif self.path == "/form_handler.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            new_dict = {}
            for key, value in postvars.items():
               if key in ['colour_1', 'colour_2', 'colour_3']:
                   new_dict[key] = [v.replace('#', '') for v in value]
               else:
                   new_dict[key] = value

            # print( new_dict );


            # postvars
            vals = ()
            for key in new_dict:
                vals += tuple(new_dict[key])

            # print(vals)

            db = molsql.Database(reset = False);
            db.create_tables();
            db.__setitem__('Elements', vals)

            message = "data received";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );


        elif self.path == "/form_hand.html":
            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            # print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            # print(postvars)
            code = postvars['elementsel'][0]
            print(code)

            db = molsql.Database(reset = False);
            db.create_tables();
            db.conn.execute('DELETE FROM Elements WHERE ELEMENT_CODE = ?', (code,))
            db.conn.commit()


            message = "deleted";
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

        elif self.path == "/Loc":
            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers.get('Content-Length', 0));
            body = self.rfile.read(content_length);
            # print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            print(postvars)
            # sdfname = postvars.get('sdfname', [''])[0]
            sdfname = postvars.get(' name', [''])[0].split('\r\n\r\n')[1].split('\r\n')[0]
            print(sdfname)
            db = molsql.Database(reset = False);
            db.conn.execute("UPDATE Molecules SET NAME= ? WHERE NAME = 'Some'", (sdfname,))
            db.conn.commit()
            db.conn.close()


            self.send_response( 302 ); # OK
            self.send_header( "Location", "/sdf_page.html" )
            self.end_headers();

        elif self.path == "/display.html":
            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers.get('Content-Length', 0));
            body = self.rfile.read(content_length);
            # print( repr( body.decode('utf-8') ) );
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            # print(postvars)
            molna = postvars.get('molsel', [''])[0]
            axis = postvars.get('axis', [''])[0]
            deg = postvars.get('degreesc', [''])[0]
            # print(molna)
            print(axis)
            # print(deg)

            mol = MolDisplay.Molecule();
            db = molsql.Database(reset = False);
            molfile = db.load_mol(molna)

            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()

            if axis == 'X':
                mx = molecule.mx_wrapper(int(deg),0,0)
                molfile.xform( mx.xform_matrix );

            elif axis == 'Y':
                mx = molecule.mx_wrapper(0,int(deg),0)
                molfile.xform( mx.xform_matrix );

            elif axis == 'Z':
                mx = molecule.mx_wrapper(0,0,int(deg))
                molfile.xform( mx.xform_matrix );

            molfile.sort();
            svg_data = molfile.svg()
            print(svg_data)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(svg_data))
            self.end_headers()
            self.wfile.write(bytes(svg_data, "utf-8"))


        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );


httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
db = molsql.Database(reset = False);
db.create_tables();
httpd.serve_forever();
