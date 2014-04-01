# coding=utf-8
"""
   tocsv.py
   Convert the DBF file provided by the "Instituto Nacional de Geografía
   Estadística e Informática" (INEGI) to comma separated value file,
   preservers the enconding (from DBF's codepage 1252 to UFT-8)
   The DBFs can be obtained here:
   --- Catálogo Único de Claves de Áreas Geoestadísticas Estatales,
       Municipales y Localidades ---
   http://www.inegi.org.mx/geo/contenidos/geoestadistica/catalogoclaves.aspx
"""
from __future__ import unicode_literals, print_function
import dbf
from utils import UnicodeWriter
from csv import QUOTE_ALL
import time
import sys
import optparse
import os

def main(args=None):
    """Process whe DBF file"""
    parser = optparse.OptionParser(usage="python tocsv.py [options] file")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="Verbose logging", default=False)
    options, args = parser.parse_args(args)
    if not args:
        sys.stderr.write("Need at least a file to process\n")
        sys.stderr.write("Use --help to show usage\n")
        return 2

    ## Trick: http://stackoverflow.com/a/9462099
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    for filename in args:
        if options.verbose:
            print("Processing {0}".format(filename))
            print('.', end="")
            init_time = time.time()
        table = dbf.Table(filename, codepage="cp1252")
        table.open()
        with open("{f}.csv".format(f=filename), "w") as csvfile:
            # Include the first line as a comma-separated line, no-quoting
            csvfile.write(",".join(table.field_names)+"\n")
            csvwriter = UnicodeWriter(csvfile, quoting=QUOTE_ALL )
            records = 0
            for records, row in enumerate(table, start=1):
                csvwriter.writerow([field.strip() for field in row])
                if options.verbose:
                    # print a dot every 1000 records
                    if records % 1000 == 0:
                        print('.', end="")
            if options.verbose:
                print("\nTotal records: {records} on {s:.2f} seconds"\
                      .format(records=records, s = time.time() - init_time))

if __name__ == "__main__":
    main()

