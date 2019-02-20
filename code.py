import os
import sys
from sqlalchemy import Table,Column,ForeignKey,Integer,Float,String
from sqlalchemy import and_ , or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.schema import Sequence
from sqlalchemy.inspection import inspect

Base = declarative_base()

class Association(Base):
    __tablename__="Association"
    nom = Column("nom",String,primary_key=True)
    tel = Column("tel",String(8)) 
    add =Column("addresse",String)

class Creneau(Base):
    __tablename__="Créneau"
    id = Column("id_Creneau",Integer,
                Sequence("Creneau_id_seq",start=1,increment=1),primary_key=True)
    j= Column("date_j",Integer)
    m = Column("date_m",Integer)
    a = Column("date_a",Integer)
    h_debut = Column("h_debut",String)
    dur = Column("durée",Integer) #en mn
    
class Gardien(Base):
    __tablename__="Gardien"
    id = Column("id_Gardien",Integer,
                Sequence("Creneau_id_seq",start=1,increment=1),primary_key=True)
    nom = Column("nom",String)
    prenom = Column("prénom",String)
    tel = Column("tel",String(8))

class Aire(Base):
    __tablename__="Aire"
    id = Column("id_Aire",Integer,
                Sequence("Creneau_id_seq",start=1,increment=1),primary_key=True)
    nom = Column("nom",String)
    id_Equipement = Column("id Equipement",
                           String,ForeignKey("Equipement.id_Equipement"))
    Equipements = relationship("Equipement",backref="Aire" ,uselist=True)

class Equipement(Base):
    __tablename__="Equipement"
    id = Column("id_Equipement",Integer,
                Sequence("Creneau_id_seq",start=1,increment=1),primary_key=True)
    nom = Column("nom",String)
    secteur = Column("secteur",String)

occupe_table= Table("Occupe",Base.metadata,
                    Column("sportifs_prevu",Integer),
                    Column("sportifs_present",Integer),
                    Column("id_Creneau",String,ForeignKey("Créneau.id_Creneau")),
                    Column("id_Association",String,ForeignKey("Association.nom")),
                    Column("id_Aire",String,ForeignKey("Aire.id_Aire")),
                    Column("id_Gardien",String,ForeignKey("Gardien.id_Gardien"))
                    )

subit_talbe= Table("Subit",Base.metadata,
                   Column("id_Creneau",String,ForeignKey("Créneau.id_Creneau")),
                   Column("id_Aire",String,ForeignKey("Aire.id_Aire")),
                   Column("Probleme",String)
                   )
    
# engine = storage for the data
engine = create_engine('sqlite:///PM.db')
#create all table in the engine
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
subit = [Base.metadata.tables["Subit"]][0]
occupe=[Base.metadata.tables["Occupe"]][0]
s= Session()

def create_all():
    c1 = Creneau()
    c2 = Creneau(j=9,m=12,a=2018)

    a1 = Aire(nom="piscine")
    a2 = Aire(nom="terrain foot")
    a3 = Aire(nom="A3")
    e1 = Equipement(nom="E1")
    e2 = Equipement(nom="E2")
    e3 = Equipement(nom="E3")

    g = Gardien(nom="Mohamed",prenom="Mohamed",tel="88888888")

    ass = Association(nom="A",tel="99999999")
    
    a1.Equipements.append(e1)
    a1.Equipements.append(e2)
    a2.Equipements.append(e3)

    s.add(c1)
    s.add(c2)
    s.add(a1)
    s.add(a2)
    s.add(a3)
    s.add(e1)
    s.add(e2)
    s.add(e3)
    s.add(g)
    s.add(ass)
##create_all()
for i in s.query(Aire).all():
    print(i.nom)
for i in s.query(Aire).filter(Aire.id_Equipement==1).all():
    print(i.nom)
#Q1
##print("Q1")
##q = s.query(Equipement,Aire).filter(Aire.nom=="terrain foot").all()
##for i in q :
##    print(i[0].nom)
###Q2
##print("Q2")
##q = s.query(Creneau).filter(and_(Creneau.j==9,Creneau.m==12,Creneau.a==2018))
##for i in q:
##    print(i.h_debut)
###Q3
##print("Q3")
##for i in s.query(Aire).filter(Aire.Equipements==None):
##    print(i.nom)
###Q4
##print("Q4")
##s.execute(occupe.insert().values(id_Aire=3))
##for i in s.execute(occupe.select().where(Aire.nom=="piscine")):
##    print(s.query(Association).filter(Association.nom==i.id_Association).all())
###Q5
##print("Q5")
##for i in s.execute(occupe.select().where(and_(Gardien.nom=="Mohamed"
##                                         ,Gardien.prenom=="Mohamed"))):
##    for k in s.query(Creneau).filter(Creneau.id==i.id_Creneau):
##        print("{0}/{1}/[2}".format(k.j,k.m,k.a))
###Q6
##print("Q6")
##for i in s.execute(subit.select().where(Aire.nom=="piscine")):
##    print(i.Probleme)
###Q7
##print("Q7")
##for i in s.execute(occupe.select().where(and_(Aire.nom=="terrain foot"
##                                              ,Creneau.j==18
##                                              ,Creneau.m==11
##                                              ,Creneau.a==2017))):
##    for j in s.query(Associaiton).filter(Association.nom==i.id_Associaiton):
##        print(j.nom)
###Q8
##print("Q8")
##for i in s.execute(occupe.select().where(Aire.nom=="piscine")):
##    print(i.sportifs_present)
###Q9
##print("Q9")
##sum_q9=0
##for i in s.execute(occupe.select().where(and_(Creneau.j==20
##                                              ,Creneau.m==1
##                                              ,Creneau.a==2019))):
##    sum_q9=sum_q9+int(i.sportifs_prevu)
##print(sum_q9)
###Q10
##print("Q10")
##for i in s.execute(subit.select().where(and_(Creneau.j==31,Creneau.m==12
##                                             ,Creneau.a==2018
##                                             ,Aire.nom=="piscine"))):
##    for j in s.execute(occupe.select().where(Aire.nom==i.id_Aire)):
##        for k in s.query(Gardien).filter(Gardien.id==j.id_Gardien):
##            print(k)
##
##t = inspect(Creneau)
##for col in t.c:
##    print(col.name)
s.commit()
