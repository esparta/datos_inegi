
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Entidad(Base):
    __tablename__ = 'entidades'

    cve_ent = Column(String(2), primary_key=True)
    nom_ent = Column(String(50))
    nom_abr = Column(String(5))
    cve_cap = Column(String(7))
    nom_cap = Column(String(100))
    ptot = Column(Integer)
    pmas = Column(Integer)
    pfem = Column(Integer)
    vtot = Column(Integer)

    def __repr__(self):
        return "<Entidad(cve_ent='{self.cve_ent}', nombre='{self.nom_ent}')>".format(self=self)

class Municipio(Base):
    __tablename__ = 'municipios'

    cve_ent = Column(String(2), ForeignKey("entidades.cve_ent"),
                     primary_key=True)
    nom_ent = Column(String(50))
    nom_abr = Column(String(5))
    cve_mun = Column(String(3), primary_key=True)
    nom_mun = Column(String(100))
    cve_cab = Column(String(4))
    nom_cab = Column(String(100))
    ptot = Column(Integer)
    pmas = Column(Integer)
    pfem = Column(Integer)
    vtot = Column(Integer)

    entidad = relationship("Entidad", backref=backref('municipios',
                                                   order_by=cve_mun))

    def __repr__(self):
        return "<Municipio(cve_mun='{self.cve_mun}', nombre='{self.nom_mun}'".format(self=self)


class Localidad(Base):
    __tablename__ = 'localidades'

    cve_ent  = Column(String(2), ForeignKey("municipios.cve_ent"),
                      primary_key=True )
    nom_ent  = Column(String(50))
    nom_abr  = Column(String(5))
    cve_mun  = Column(String(3), ForeignKey("municipios.cve_mun"),
                      primary_key=True)
    nom_mun  = Column(String(100))
    cve_loc  = Column(String(4), primary_key=True)
    nom_loc  = Column(String(100))
    latitud  = Column(String(12))
    longitud = Column(String(12))
    altitud  = Column(Integer)
    cve_cart = Column(String(6))
    ambito = Column(String(1))
    ptot = Column(Integer)
    pmas = Column(Integer)
    pfem = Column(Integer)
    vtot = Column(Integer)



    #municipio = relationship("Municipio",
    #                         foreign_keys=[cve_ent, cve_mun],
    #                         backref=backref('localidades',
    #                                         order_by=cve_loc))
    def __repr__(self):
        return "<Localidad(cve_mun='{self.cve_mun}', nombre='{self.nom_loc}'".format(self=self)
