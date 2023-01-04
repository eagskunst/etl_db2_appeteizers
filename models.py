from sqlalchemy import Column, Integer, String, Float, Date
from dbconfig import Base

class Client(Base):
    __tablename__ = "DimCliente"
    key_cliente = Column(String, primary_key=True)
    nombre = Column(String)
    cedula = Column(String)

    def __init__(self, key_cliente, nombre, cedula):
        self.key_cliente = key_cliente
        self.nombre = nombre
        self.cedula = cedula

class Agency(Base):
    __tablename__ = "DimAgencia"
    key_agencia = Column(String, primary_key=True)
    nombre = Column(String)
    ubicacion = Column(String)
    costo_mantenimiento = Column(Float)

    def __init__(self, key_agencia, nombre, ubicacion, costo_mantenimiento):
        self.key_agencia = key_agencia
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.costo_mantenimiento = costo_mantenimiento

class Appeteizer(Base):
    __tablename__ = "DimPasapalo"
    key_pasapalo = Column(String, primary_key=True)
    tipo = Column(Integer)
    ingrediente = Column(String)
    costo_produccion = Column(Float)
    precio_unitario = Column(Float)

    def __init__(self, key_pasapalo, tipo, ingrediente, costo_produccion, precio_unitario):
        self.key_pasapalo = key_pasapalo
        self.tipo = tipo
        self.ingrediente = ingrediente
        self.costo_produccion = costo_produccion
        self.precio_unitario = precio_unitario

class Sale(Base):
    __tablename__ = "HechosVentas"
    key_venta = Column(String, primary_key=True)
    key_agencia = Column(String)
    key_pasapalo = Column(String)
    key_cliente = Column(String)
    total_pasapalos = Column(Integer)
    total_vendido = Column(Float)
    margen = Column(Float)
    nombre_dia = Column(String)
    fecha = Column(Date)

    def __init__(self, key_agencia, key_pasapalo, key_cliente, total_pasapalos, total_vendido, margen, nombre_dia, fecha):
        self.key_venta = f'{key_agencia},{key_pasapalo},{key_cliente},{total_pasapalos},{total_vendido},{fecha}'
        self.key_agencia = key_agencia
        self.key_pasapalo = key_pasapalo
        self.key_cliente = key_cliente
        self.total_pasapalos = total_pasapalos
        self.total_vendido = total_vendido
        self.margen = margen
        self.nombre_dia = nombre_dia
        self.fecha = fecha
