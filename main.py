import logging
import petl as etl
from petl.io.csv_py3 import CSVView
from objects import SellData, Cliente, Agencia, Pasapalo, SellInfo, EntitiesCollectionsWrapper
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("etl_teque;os_ca")
from dbconfig import Base, engine, Session
from models import Client, Agency, Appeteizer, Sale


def main():
    logger.info("Start extract process")
    table = _extract()
    logger.info("End extract process")
    logger.info("Start transform process")
    entities_wrapper =_transform(table)
    logger.info("End transform process")
    logger.info("Start load process")
    _load(entities_wrapper)
    logger.info("End load process")

def _extract():
    return etl.fromcsv("datos.csv")

def _transform(table: CSVView):
    table = etl.convert(table, 'numero', int)
    table = etl.convert(table, 'dia_num', int)
    table = etl.convert(table, 'tipo_pasapalo', int)
    table = etl.convert(table, 'cantidad', int)
    table = etl.convert(table, 'costo_unitario', float)
    table = etl.convert(table, 'precio_por_pasapalo', float)
    table = etl.convert(table, 'total_a_pagar', float)
    table = etl.convert(table, 'mantenimiento_agencia', float)
    sell_info_list = []
    client_dict = dict()
    agency_dict = dict()
    appeteizers_dict = dict()

    for idx, row in enumerate(table):
        if (idx == 0):
            continue
        item = SellData(*row)
        if item.client_id not in client_dict:
            client_dict[item.client_id] = Cliente(f'{item.client_first_name} {item.client_last_name}', item.client_id)
        if item.agency not in agency_dict:
            agency_dict[item.agency] = Agencia(item.agency, item.agency_ubication, item.maintenance_price)
        if item.appetizer_type not in appeteizers_dict:
            appeteizers_dict[item.appetizer_type] = Pasapalo(item.appetizer_type, item.unitary_cost, item.appeterize_price)
        
        sell_info = SellInfo(item, client_dict[item.client_id], agency_dict[item.agency], appeteizers_dict[item.appetizer_type])
        sell_info_list.append(sell_info)
    
    return EntitiesCollectionsWrapper(sell_info_list, client_dict, agency_dict, appeteizers_dict)

def _load(entities_wrapper: EntitiesCollectionsWrapper):
    Base.metadata.create_all(engine)
    session = Session()
    for client in entities_wrapper.clients.values():
        db_client = Client(client.key_cliente, client.nombre, client.cedula)
        session.add(db_client)
    
    for agency in entities_wrapper.agencies.values():
        db_agency = Agency(agency.key_agencia, agency.nombre, agency.ubicacion, agency.maintenance_cost)
        session.add(db_agency)
    
    for appeteizer in entities_wrapper.appeteizers.values():
        db_appeteizer = Appeteizer(appeteizer.key_pasapalo, appeteizer.tipo, appeteizer.ingrediente, appeteizer.costo_produccion, appeteizer.precio_unitario)
        session.add(db_appeteizer)
    
    for sale in entities_wrapper.sell_info:
        sell_data = sale.sell_data
        db_sale = Sale(sale.agency.key_agencia, sale.appeteizer.key_pasapalo, sale.client.key_cliente, sell_data.quantity, sell_data.total_payment, sell_data.margen, sell_data.week_day, sell_data.sell_date)
        session.add(db_sale)

    session.commit()
    session.close()

if __name__ == "__main__":
    main()