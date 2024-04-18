from elreda_v1.observer import Publisher
from elreda_v1.persistances import ElredaDB
from elreda_v1.dtos import OrderDTO

from abc import ABCMeta, abstractmethod
from kink import inject


@inject
class IElredaService(metaclass=ABCMeta):
    @abstractmethod
    def get_queue_from_service_for_ui(self):
        pass

    @abstractmethod
    def get_report_data(self):
        pass

    @abstractmethod
    def check_valid_to_append_queue(self, _food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date):
        pass

    @abstractmethod
    def add_order_queue(self, _food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date):
        pass

    @abstractmethod
    def get_queue_from_service_for_ui(self):
        pass

    @abstractmethod
    def send_notice_at_order_page(self):
        pass

    @abstractmethod
    def insert_to_database_queue_idx_0(self):
        pass


@inject
class ElredaService(IElredaService):
    def __init__(self, _elreda_db:ElredaDB, _publisher:Publisher):
        self.queue = []
        self.__publisher = _publisher
        self.__elreda_db = _elreda_db

    def init(self):
        self.__elreda_db.init()

    def get_report_data(self):
        order_dtos = self.__elreda_db.get_all_data_to_report_tab()
        return order_dtos

    def check_valid_to_append_queue(self,  _food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date):
        if not _amount_of_drink.isnumeric() or not _amount_of_food.isnumeric():
            return False
        else:
            if int(_amount_of_food) < 0 or int(_amount_of_drink) < 0:
                return False

        if _amount_of_drink == '' or _amount_of_food == '' or _name == '':
            return False
        return True

    def add_order_queue(self, _food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date):
        dto = OrderDTO(_food, _drink, _table_num, _amount_of_food, _amount_of_drink, _name, _date)
        self.queue.append(dto)
        self.__publisher.notify("ORDER", dto)

    def get_queue_from_service_for_ui(self):
        return self.queue

    def send_notice_at_order_page(self):
        if len(self.queue) > 5:
            return True, "Kitchen is Busy (remind guest!!)"
        else:
            return False, ""

    def insert_to_database_queue_idx_0(self):
        # setelah button done diclick
        # queue terdepan akan dihapus
        # lalu dimasukan ke dalam queue
        # jika tanggal pemesanannya belum pernah ada didatabase, buat baru dan default 0
        # jika tanggal pemesanannya sudah ada didatabase, tambahkan saja, berdasarkan menu makanan dan minuman
        if len(self.queue) > 0:
            dto = self.queue[0]
            self.queue.pop(0)
            if not self.__elreda_db.find_data_by_date(dto.date): # Ketika tanggal tersebut tidak terdapat terdapat dalam database
                self.__elreda_db.insert_all_menu_new_date_default_nul(dto.date)

            id_date = self.__elreda_db.get_id_date_by_date(dto.date)
            self.__elreda_db.insert__into_the_total_food_menu_that_date(id_date, dto.food, dto.amount_of_food, dto.drink, dto.amount_of_drink)
            self.__publisher.notify("DONE", dto)


