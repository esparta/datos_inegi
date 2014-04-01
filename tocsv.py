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
from __future__ import unicode_literals
import dbf
from utils import UnicodeWriter
from csv import QUOTE_ALL


def main():
    """Process whe DBF file"""
    table = dbf.Table("cat_localidad_FEB2014.dbf", codepage="cp1252")
    table.open()
    with open("localidades.csv", "w") as csvfile:
        # Include the first line as a comma-separated line, with no-quoting
        csvfile.write(",".join(table.field_names)+"\n")
        csvwriter = UnicodeWriter(csvfile, quoting=QUOTE_ALL )
        for row in table:
            csvwriter.writerow([field.strip() for field in row])

if __name__ == "__main__":
    main()

