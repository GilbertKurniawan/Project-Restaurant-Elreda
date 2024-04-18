from elreda_v1.services import ElredaService
from elreda_v1.persistances import ElredaDB
from elreda_v1.observer import Publisher

from kink import inject


@inject
class ElredaServiceV2(ElredaService):
    def __init__(self, _elreda_db:ElredaDB, _publisher:Publisher):
        super().__init__(_elreda_db, _publisher)

    def add_order_queue(self, _food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date):
        print("\nTinggTongg... Ada pesanan masuk!")
        super().add_order_queue(_food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date)


