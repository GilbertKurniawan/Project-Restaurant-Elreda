from kink import inject


@inject
class OrderDTO:
    def __init__(self, _food, _drink, _table_number, _amount_of_food, _amount_of_drink, _name=None, _date=None):
        self.food = _food
        self.drink = _drink
        self.table_number = _table_number
        self.amount_of_food = _amount_of_food
        self.amount_of_drink = _amount_of_drink
        self.name = _name
        self.date = _date