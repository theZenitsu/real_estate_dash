from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Define the association table
annonce_equipement = Table(
    'annonce_equipement',
    Base.metadata,
    Column('annonce_id', Integer, ForeignKey('annonce.id'), primary_key=True),
    Column('equipement_id', Integer, ForeignKey('equipement.id'), primary_key=True)
)

class Ville(Base):
    __tablename__ = 'ville'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Equipement(Base):
    __tablename__ = 'equipement'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Annonce(Base):
    __tablename__ = 'annonce'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    datetime = Column(String, nullable=False)
    nb_rooms = Column(Integer, nullable=False)
    nb_baths = Column(Integer, nullable=False)
    surface_area = Column(Float, nullable=False)
    link = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('ville.id'), nullable=False)

    # Relationships
    city = relationship("Ville", back_populates="annonces")
    equipments = relationship("Equipement", secondary=annonce_equipement, back_populates="annonces")

Equipement.annonces = relationship("Annonce", secondary=annonce_equipement, back_populates="equipments")
Ville.annonces = relationship("Annonce", back_populates="city")
