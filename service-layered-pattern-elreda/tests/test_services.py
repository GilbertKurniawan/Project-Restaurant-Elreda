from elreda_v1 import ElredaService

from elreda_v1 import IElredaDB
from elreda_v1 import OrderDTO
from elreda_v1 import Publisher, FoodSupplier, Kitchen, Customer


class MockDB(IElredaDB):
    def __init__(self):
        self.pesanan = [
            {"ID_tanggal": "P001", "Tanggal": "07-12-2022"},
            {"ID_tanggal": "P002", "Tanggal": "08-12-2022"}
        ]
        self.detail_pesanan = [
            {"ID_tanggal": "P001", "Menu_makanan": "Kubideh Rice",     "Jumlah_makanan": 1, "Menu_minuman": "Ayran",         "Jumlah_minuman": 1},
            {"ID_tanggal": "P001", "Menu_makanan": "Fischteller",      "Jumlah_makanan": 2, "Menu_minuman": "Coca cola",     "Jumlah_minuman": 2},
            {"ID_tanggal": "P001", "Menu_makanan": "Chicken Rice",     "Jumlah_makanan": 0, "Menu_minuman": "Mineral water", "Jumlah_minuman": 3},
            {"ID_tanggal": "P001", "Menu_makanan": "Gemischter Salad", "Jumlah_makanan": 21, "Menu_minuman": "Tea",          "Jumlah_minuman": 4},
            {"ID_tanggal": "P001", "Menu_makanan": "Djujeh",           "Jumlah_makanan": 5, "Menu_minuman": "Coffee",        "Jumlah_minuman": 5},

            {"ID_tanggal": "P002", "Menu_makanan": "Kubideh Rice",     "Jumlah_makanan": 5, "Menu_minuman": "Ayran",         "Jumlah_minuman": 3},
            {"ID_tanggal": "P002", "Menu_makanan": "Fischteller",      "Jumlah_makanan": 5, "Menu_minuman": "Coca cola",     "Jumlah_minuman": 3},
            {"ID_tanggal": "P002", "Menu_makanan": "Chicken Rice",     "Jumlah_makanan": 5, "Menu_minuman": "Mineral water", "Jumlah_minuman": 3},
            {"ID_tanggal": "P002", "Menu_makanan": "Gemischter Salad", "Jumlah_makanan": 5, "Menu_minuman": "Tea",           "Jumlah_minuman": 3},
            {"ID_tanggal": "P002", "Menu_makanan": "Djujeh",           "Jumlah_makanan": 5, "Menu_minuman": "Coffee",        "Jumlah_minuman": 3}
        ]

    def find_data_by_date(self, _date):
        id_date = None
        for dict in self.pesanan:
            if dict["Tanggal"] == _date:
                id_date = dict["ID_tanggal"]
        if id_date != None:
            return True
        else: return False

    def insert_all_menu_to_database_with_new_date_default_nul(self, _date):
        # make unique_id
        unique_id = "P00" + str(len(self.pesanan))
        self.detail_pesanan.append({"ID_tanggal": unique_id, "Menu_makanan": "Kubideh Rice", "Jumlah_makanan": 0, "Menu_minuman": "Ayran", "Jumlah_minuman": 0})
        self.detail_pesanan.append({"ID_tanggal": unique_id, "Menu_makanan": "Fischteller", "Jumlah_makanan": 0, "Menu_minuman": "Coca cola", "Jumlah_minuman": 0})
        self.detail_pesanan.append({"ID_tanggal": unique_id, "Menu_makanan": "Chicken Rice", "Jumlah_makanan": 0, "Menu_minuman": "Mineral water", "Jumlah_minuman": 0})
        self.detail_pesanan.append({"ID_tanggal": unique_id, "Menu_makanan": "Gemischter Salad", "Jumlah_makanan": 0, "Menu_minuman": "Tea", "Jumlah_minuman": 0})
        self.detail_pesanan.append({"ID_tanggal": unique_id, "Menu_makanan": "Djujeh", "Jumlah_makanan": 0, "Menu_minuman": "Coffee", "Jumlah_minuman": 0})

    def insert__into_the_total_food_menu_that_date(self, id_date, food, amt_food, drink, amt_drink):
        for dict in self.detail_pesanan:
            if dict["ID_tanggal"] == id_date and dict["Menu_makanan"] == food:
                dict["Jumlah_makanan"] += amt_food
            if dict["ID_tanggal"] == id_date and dict["Menu_minuman"] == drink:
                dict["Jumlah_minuman"] += amt_drink

    def get_id_date_by_date(self, _date):
        for dict in self.pesanan:
            if dict["Tanggal"] == _date:
                id_date = dict["ID_tanggal"]
                return id_date

    def get_all_data_to_report_tab(self):
        order_dtos = []
        for dict in self.pesanan:
            for dict2 in self.detail_pesanan:
                if dict["ID_tanggal"] == dict2["ID_tanggal"]:
                    order_dtos.append(OrderDTO(dict2["Menu_makanan"], dict2["Menu_minuman"], None, dict2["Jumlah_makanan"], dict2["Jumlah_minuman"], None, dict["Tanggal"]))

        return order_dtos


class MockPublisher(Publisher):
    def __init__(self):
        # _all_publisher dibuat [] kosong
        # supaya MockKitchen dan MockCustomer bisa terpisah dari Publisher jadi bisa di check counternya
        super(MockPublisher, self).__init__([])


class MockKitchen(Kitchen):
    def __init__(self):
        self.counter_print = 0

    def notified(self, _type, _data):
        if _type == "ORDER":
            self.counter_print += 1


class MockCustomer(Customer):
    def __init__(self):
        self.counter_email = 0

    def pop_up_email_on_the_screen(self, dto):
        self.counter_email += 1


def test_should_show_a_new_add_order_in_kitchen_tab():
    # before test
    food = "Kubideh Rice"
    drink = "Ayran"
    table_num = "4"
    amt_food = "1"
    amt_drink = "2"
    name = "John"
    date = "21-12-2022"

    mock_publisher = MockPublisher()
    mock_customer = MockCustomer()
    mock_kitchen = MockKitchen()

    mock_publisher.add_subscriber(mock_customer)
    mock_publisher.add_subscriber(mock_kitchen)

    # pytest tidak dapat dijalankan dengan DI
    # di["_elreda_db"] = MockDB()
    # di["_publisher"] = mock_publisher

    elreda_service = ElredaService(MockDB(), mock_publisher)

    # expected result before test
    expected_len_queue = 0
    current_len_queue = len(elreda_service.queue)

    assert expected_len_queue == current_len_queue, \
        f"Expected {expected_len_queue} but get {current_len_queue}"

    # System Under Test / SUT
    elreda_service.add_order_queue(food, drink, table_num, amt_food, amt_drink, name, date)
    dto = elreda_service.queue[0]

    # expected result before test
    expected_len_queue = 1
    current_len_queue = len(elreda_service.queue)

    assert expected_len_queue == current_len_queue, \
        f"Expected {expected_len_queue} but get {current_len_queue}"

    assert food == dto.food, \
        f"Expected {food} but get {dto.food}"

    assert drink == dto.drink, \
        f"Expected {drink} but get {dto.drink}"

    assert table_num == dto.table_number, \
        f"Expected {table_num} but get {dto.table_number}"

    assert amt_food == dto.amount_of_food, \
        f"Expected {amt_food} but get {dto.amount_of_food}"

    assert amt_drink == dto.amount_of_drink, \
        f"Expected {amt_drink} but get {dto.amount_of_drink}"

    assert name == dto.name, \
        f"Expected {name} but get {dto.name}"

    assert date == dto.date, \
        f"Expected {date} but get {dto.date}"


def test_should_show_warning_msg_if_more_than_5_in_queue():
    # before test
    food_1 = "Kubideh Rice"
    drink_1 = "Ayran"
    table_num_1 = "1"
    amt_food_1 = "1"
    amt_drink_1 = "1"
    name_1 = "Lucas"
    date_1 = "21-12-2022"

    food_2 = "Fischteller"
    drink_2 = "Coca cola"
    table_num_2 = "2"
    amt_food_2 = "2"
    amt_drink_2 = "2"
    name_2 = "Paulus"
    date_2 = "22-12-2022"

    food_3 = "Chicken Rice"
    drink_3 = "Mineral water"
    table_num_3 = "3"
    amt_food_3 = "3"
    amt_drink_3 = "3"
    name_3 = "Matthew"
    date_3 = "22-12-2022"

    food_4 = "Gemischter Salad"
    drink_4 = "Tea"
    table_num_4 = "4"
    amt_food_4 = "2"
    amt_drink_4 = "1"
    name_4 = "David"
    date_4 = "21-12-2022"

    food_5 = "Djujeh"
    drink_5 = "Coffee"
    table_num_5 = "5"
    amt_food_5 = "3"
    amt_drink_5 = "1"
    name_5 = "Maria"
    date_5 = "22-12-2022"

    food_6 = "Chicken Rice"
    drink_6 = "Coffee"
    table_num_6 = "6"
    amt_food_6 = "5"
    amt_drink_6 = "5"
    name_6 = "Yusuf"
    date_6 = "23-12-2022"

    mock_publisher = MockPublisher()
    mock_customer = MockCustomer()
    mock_kitchen = MockKitchen()

    mock_publisher.add_subscriber(mock_customer)
    mock_publisher.add_subscriber(mock_kitchen)

    # pytest tidak dapat dijalankan dengan DI
    # di["_elreda_db"] = MockDB()
    # di["_publisher"] = mock_publisher
    elreda_service = ElredaService(MockDB(), mock_publisher)

    # System Under Test / SUT
    elreda_service.add_order_queue(food_1, drink_1, table_num_1, amt_food_1, amt_drink_1, name_1, date_1)

    # expected result
    cur_value, cur_str = elreda_service.send_notice_at_order_page()
    expected_value = False
    expected_str = ""
    assert expected_value == cur_value, \
        f"Expected {expected_value} but get {cur_value}"

    assert expected_str == cur_str, \
        f"Expected {expected_str} but get {cur_str}"

    # System Under Test / SUT
    elreda_service.add_order_queue(food_2, drink_2, table_num_2, amt_food_2, amt_drink_2, name_2, date_2)
    elreda_service.add_order_queue(food_3, drink_3, table_num_3, amt_food_3, amt_drink_3, name_3, date_3)
    elreda_service.add_order_queue(food_4, drink_4, table_num_4, amt_food_4, amt_drink_4, name_4, date_4)
    elreda_service.add_order_queue(food_5, drink_5, table_num_5, amt_food_5, amt_drink_5, name_5, date_5)

    # expected result
    cur_value, cur_str = elreda_service.send_notice_at_order_page()
    expected_value = False
    expected_str = ""
    assert expected_value == cur_value, \
        f"Expected {expected_value} but get {cur_value}"

    assert expected_str == cur_str, \
        f"Expected {expected_str} but get {cur_str}"

    # System Under Test / SUT
    elreda_service.add_order_queue(food_6, drink_6, table_num_6, amt_food_6, amt_drink_6, name_6, date_6)

    # expected result
    cur_value, cur_str = elreda_service.send_notice_at_order_page()
    expected_value = True
    expected_str = "Kitchen is Busy (remind guest!!)"
    assert expected_value == cur_value, \
        f"Expected {expected_value} but get {cur_value}"

    assert expected_str == cur_str, \
        f"Expected {expected_str} but get {cur_str}"


def test_email_sent_if_order_placed():
    # before test
    food_1 = "Kubideh Rice"
    drink_1 = "Ayran"
    table_num_1 = "1"
    amt_food_1 = "1"
    amt_drink_1 = "1"
    name_1 = "Lucas"
    date_1 = "21-12-2022"

    food_2 = "Fischteller"
    drink_2 = "Coca cola"
    table_num_2 = "2"
    amt_food_2 = "2"
    amt_drink_2 = "2"
    name_2 = "Paulus"
    date_2 = "22-12-2022"

    food_3 = "Chicken Rice"
    drink_3 = "Mineral water"
    table_num_3 = "3"
    amt_food_3 = "3"
    amt_drink_3 = "3"
    name_3 = "Matthew"
    date_3 = "22-12-2022"

    mock_publisher = MockPublisher()
    mock_customer = MockCustomer()
    mock_kitchen = MockKitchen()

    mock_publisher.add_subscriber(mock_customer)
    mock_publisher.add_subscriber(mock_kitchen)

    # pytest tidak dapat dijalankan dengan DI
    # di["_elreda_db"] = MockDB()
    # di["_publisher"] = mock_publisher

    elreda_service = ElredaService(MockDB(), mock_publisher)

    # expected result before test
    expected_counter_email = 0
    current_counter_customer = mock_customer.counter_email

    assert expected_counter_email == current_counter_customer, \
        f"Expected {expected_counter_email} but get {current_counter_customer}"

    # System Under Test / SUT
    elreda_service.add_order_queue(food_1, drink_1, table_num_1, amt_food_1, amt_drink_1, name_1, date_1)
    elreda_service.add_order_queue(food_2, drink_2, table_num_2, amt_food_2, amt_drink_2, name_2, date_2)
    elreda_service.add_order_queue(food_3, drink_3, table_num_3, amt_food_3, amt_drink_3, name_3, date_3)

    # expected
    expected_counter_email = 3
    current_counter_customer = mock_customer.counter_email

    assert expected_counter_email == current_counter_customer, \
        f"Expected {expected_counter_email} but get {current_counter_customer}"


def test_text_print_if_order_placed():
    # before test
    food_1 = "Kubideh Rice"
    drink_1 = "Ayran"
    table_num_1 = "1"
    amt_food_1 = "1"
    amt_drink_1 = "1"
    name_1 = "Lucas"
    date_1 = "21-12-2022"

    food_2 = "Fischteller"
    drink_2 = "Coca cola"
    table_num_2 = "2"
    amt_food_2 = "2"
    amt_drink_2 = "2"
    name_2 = "Paulus"
    date_2 = "22-12-2022"

    food_3 = "Chicken Rice"
    drink_3 = "Mineral water"
    table_num_3 = "3"
    amt_food_3 = "3"
    amt_drink_3 = "3"
    name_3 = "Matthew"
    date_3 = "22-12-2022"

    mock_publisher = MockPublisher()
    mock_customer = MockCustomer()
    mock_kitchen = MockKitchen()

    mock_publisher.add_subscriber(mock_customer)
    mock_publisher.add_subscriber(mock_kitchen)

    # pytest tidak dapat dijalankan dengan DI
    # di["_elreda_db"] = MockDB()
    # di["_publisher"] = mock_publisher

    elreda_service = ElredaService(MockDB(), mock_publisher)

    # expected result before test
    expected_counter_print = 0
    current_counter_kitchen = mock_kitchen.counter_print

    assert expected_counter_print == current_counter_kitchen, \
        f"Expected {expected_counter_print} but get {current_counter_kitchen}"

    # System Under Test / SUT
    elreda_service.add_order_queue(food_1, drink_1, table_num_1, amt_food_1, amt_drink_1, name_1, date_1)
    elreda_service.add_order_queue(food_2, drink_2, table_num_2, amt_food_2, amt_drink_2, name_2, date_2)
    elreda_service.add_order_queue(food_3, drink_3, table_num_3, amt_food_3, amt_drink_3, name_3, date_3)

    # expected
    expected_counter_print = 3
    current_counter_kitchen = mock_kitchen.counter_print

    assert expected_counter_print == current_counter_kitchen, \
        f"Expected {expected_counter_print} but get {current_counter_kitchen}"




















