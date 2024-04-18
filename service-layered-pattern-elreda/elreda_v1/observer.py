'''
Observer Pattern
'''

from abc import ABCMeta, abstractmethod
from typing import List
from kink import inject
from tkinter import *


class ElredaNotification(metaclass=ABCMeta):
    @abstractmethod
    def notified(self, _type, _data):
        pass


@inject
class Publisher:
    def __init__(self, _all_publisher: List[ElredaNotification]):
        self.subscriber =_all_publisher
        self.topic = "Order"

    def add_subscriber(self, _subscriber: ElredaNotification):
        self.subscriber.append(_subscriber)

    def unsubscribe(self, _subscriber: ElredaNotification):
        self.subscriber.remove(_subscriber)

    def notify(self, _type, _data):
        for s in self.subscriber:
            s.notified(_type, _data)


@inject(alias=ElredaNotification)
class FoodSupplier(ElredaNotification):
    # Jadi Publisher akan memberitahu Suppliers
    # Jika satu bahan sudah pakai sampai 20 kali, maka Suppiers akan diberitahu bahwa bahan itu sudah habis.
    # Jadi Supplier dapat mengirimkan barangnya lagi.
    def __init__(self):
        self.ingredient = {"beef": 0, "eggs":0, "rice":0, "tomatoes":0, "chicken":0, "fish":0, "vegetables":0}

    def notified(self, _type, _data):
        if _type == "DONE":
            amount = int(_data.amount_of_food)
            if _data.food == "Kubideh Rice":
                self.ingredient["beef"] += amount
                self.ingredient["eggs"] += amount
                self.ingredient["rice"] += amount
            elif _data.food == "Fischteller":
                self.ingredient["fish"] += amount
                self.ingredient["tomatoes"] += amount
                self.ingredient["rice"] += amount
            elif _data.food == "Chicken Rice":
                self.ingredient["chicken"] += amount
                self.ingredient["tomatoes"] += amount
                self.ingredient["rice"] += amount
            elif _data.food == "Gemischter Salad":
                self.ingredient["vegetables"] += amount
                self.ingredient["tomatoes"] += amount
                self.ingredient["eggs"] += amount
            elif _data.food == "Djujeh":
                self.ingredient["vegetables"] += amount
                self.ingredient["rice"] += amount
                self.ingredient["eggs"] += amount
                self.ingredient["vegetables"] += amount
                self.ingredient["beef"] += amount
            for key in self.ingredient:
                if self.ingredient[key] >= 20:
                    print(f"{key.title()} have run out. You can supply again")
                    self.ingredient[key] = 0


@inject(alias=ElredaNotification)
class Kitchen(ElredaNotification):
    def notified(self, _type, _data):
        if _type == "ORDER":
            print()
            print("+-------------------------+")
            print("| {}  {}   ".format(_data.food, _data.amount_of_food))
            print("+-------------------------+")
            print("+-------------------------+")
            print("| {}  {}   ".format(_data.drink, _data.amount_of_drink))
            print("+-------------------------+")
            print()


@inject(alias=ElredaNotification)
class Customer(ElredaNotification):
    def notified(self, _type, _data):
        if _type == "ORDER":
            # Masalah untuk pop up email: hanya cuma boleh satu siklus
            # Jika IMPORT dari UI -> Service, maka "ERROR" tidak boleh IMPORT dari Service -> UI
            # Supaya mencegah siklus melingkar [circular (cyclic) import]
            # Jadi  pop up dari customernya langsung
            self.pop_up_email_on_the_screen(_data)

    def pop_up_email_on_the_screen(self, dto):
        root = Tk()
        root.title("Email")
        root.geometry('450x273')
        email_frame = Frame(root, pady=20, padx=20)
        label_email = Label(email_frame, text=f"Dear Mr/Ms  {dto.name}, \n" \
                                              f"Thank you for ordering at El Reda restaurant. You are on table number {dto.table_number}.\n Your order:\n" \
                                              f"  - {dto.food}   {dto.amount_of_food} \n" \
                                              f"  - {dto.drink}   {dto.amount_of_drink}\n" \
                                              f"Your order will be processed, please wait.\n\n" \
                                              f"Regards, \n El Reda Restaurant", justify=LEFT,
                            font=("Roboto Reguler", 9))
        label_email.pack()
        email_frame.pack()

        def close_pop_up():
            root.destroy()

        button_close = Button(root, text="OK", font=("Roboto Medium", 8), width=5, height=2,
                              command=close_pop_up)
        button_close.pack(pady=30, padx=30, side=RIGHT)
        root.mainloop()

