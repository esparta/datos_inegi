"""tosqlite3.py
   Script to convert the csv file to SQLite3 database
"""
from __future__ import unicode_literals
import csv
import sqlite3 as s



MUNICIPIOS = """
      CREATE TABLE municipios(cve_ent text, nom_ent text, nom_abr text,
                              cve_mun text, nom_mun text, cve_cab text,
                              nom_cab text,
                              ptot int, pmas int, pfem int, vtot int);
   """

ENTIDADES = """
     CREATE TABLE entidades (cve_ent text, nom_ent text, nom_abr text,
                             cve_cap text, nom_cap text,
                             ptot int, pmas int, pfem int, vtot int);
   """

LOCALIDADES = """
      CREATE TABLE localidades (cve_ent text, nom_ent text, nom_abr text,
                                cve_mun text, nom_mun text,
                                cve_loc text, nom_loc text,
                                latitud numeric, longitud numeric,
                                altitud int,
                                cve_carta text, ambito text,
                                ptot int, pmas int, pfem int, vtot int);
   """

WORKERS = {"entidades": {"query": ENTIDADES,
                         "fields": 9},
           "municipios": {"query": MUNICIPIOS,
                          "fields": 11},
           "localidades": {"query": LOCALIDADES,
                           "fields": 16}
          }

def create(work, cur):
    """Create the entity """
    entity, values = (work)
    print("Creating entity ({e})".format(e=entity))
    query = "DROP TABLE IF EXISTS {entity};".format(entity=entity)
    query += values["query"]
    cur.executescript(query)

def insert(work, cur):
    """Inserting the rows of the current entity into database """
    entity, values = (work)
    print("Inserting records on ({e})".format(e=entity))
    with open("{e}.csv".format(e=entity)) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(4086))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        query = """
             INSERT INTO {entity} VALUES ({qm});
        """.format(entity=entity, qm = ("?," * values["fields"])[:-1])
        cur.executemany(query, reader)


def main():
    """ Main loop, cicle the entidades, municipios y localidades"""
    conn = s.connect("datos_inegi.db")
    cur = conn.cursor()
    for entity, values in WORKERS.items():
        print("Working with {e}".format(e=entity))
        create((entity, values), cur)
        insert((entity, values), cur)
    conn.commit()

if __name__ == "__main__":
    main()
