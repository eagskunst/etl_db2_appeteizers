from dataclasses import dataclass, field
import uuid
from appeteizer import ingredients_dict
from typing import Dict, List
import datetime

@dataclass
class SellData:
    month: str
    client_id: int
    week_day: str
    day: int
    client_first_name: str
    client_last_name: str
    agency: str
    appetizer_type: int
    quantity: int
    unitary_cost: float
    appeterize_price: float
    total_payment: float
    agency_ubication: str
    maintenance_price: int

    @property
    def sell_date(self):
        months_dict = {'enero': 1, 'febrero': 2, 'marzo': 3}
        return datetime.date(2022, months_dict[self.month], self.day)

    @property
    def margen(self):
        return self.total_payment - (self.unitary_cost * self.quantity)

@dataclass
class Cliente:
    nombre: str
    cedula: str
    key_cliente: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Agencia:
    nombre: str
    ubicacion: str
    maintenance_cost: int
    key_agencia: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Pasapalo:
    tipo_num: int
    costo_produccion: float
    precio_unitario: float
    key_pasapalo: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def ingrediente(self):
        return ingredients_dict[self.tipo_num][1]
    
    @property
    def tipo(self):
        return ingredients_dict[self.tipo_num][0]

@dataclass
class SellInfo:
    sell_data: SellData
    client: Cliente
    agency: Agencia
    appeteizer: Pasapalo

@dataclass
class EntitiesCollectionsWrapper:
    sell_info: List[SellInfo]
    clients: Dict[str, Cliente]
    agencies: Dict[str, Agencia]
    appeteizers: Dict[str, Pasapalo]