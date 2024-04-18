from elreda_v1.services import ElredaService

from kink import inject
from tkinter import *
from tkinter import ttk, messagebox
import time


@inject
class ElredaUI:
    def __init__(self, _elreda_service: ElredaService):
        # connect service
        self.__elreda_service = _elreda_service

        self.root = Tk()
        self.frame = None

        # date
        time_object = time.localtime()
        self.local_time = time.strftime("%d-%m-%Y", time_object)  # local_time = "08-12-2022"
        # self.local_time = "08-12-2022"

        # dropdown/entry frame for input
        self.drop_down_food = None
        self.drop_down_drink = None
        self.drop_down_table_number = None
        self.entry_amount_of_food = None
        self.entry_amount_of_drink = None
        self.entry_name = None

    def init(self):
        self.__elreda_service.init()

    def order_done(self):
        # Input to database
        self.__elreda_service.insert_to_database_queue_idx_0()
        self.kitchen_tab()

    def order_submit(self):
        food = self.drop_down_food.get().strip()
        drink = self.drop_down_drink.get().strip()
        table_num = self.drop_down_table_number.get().strip()
        amt_food = self.entry_amount_of_food.get().strip()
        amt_drink = self.entry_amount_of_drink.get().strip()
        name = self.entry_name.get().strip()

        self.order_tab()
        if self.__elreda_service.check_valid_to_append_queue(food, drink, table_num, amt_food, amt_drink, name, self.local_time):
            self.__elreda_service.add_order_queue(food, drink, table_num, amt_food, amt_drink, name, self.local_time)
        else:
            messagebox.showinfo("Info", "The order was not successful, because something has not been filled")

    def kitchen_tab(self):
        self.frame.pack_forget()

        # *** SCROLL BAR
        frame3 = Frame(self.root)
        frame3.pack(fill=BOTH, expand=1)
        self.frame = frame3


        # create a canvas
        my_canvas = Canvas(frame3)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar to the canvas
        my_scrollbar = ttk.Scrollbar(frame3, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        # ***

        label1_frame3 = Label(second_frame, text=" Queue Number", font=("Roboto Reguler", 10), width=14, height=2)
        label1_frame3.grid(row=0, column=0)

        label2_frame3 = Label(second_frame, text=" Name", font=("Roboto Reguler", 10), width=12, height=2)
        label2_frame3.grid(row=0, column=1)

        label3_frame3 = Label(second_frame, text=" Table", font=("Roboto Reguler", 10), width=10, height=2)
        label3_frame3.grid(row=0, column=2)

        label4_frame3 = Label(second_frame, text="Food ", font=("Roboto Reguler", 10), width=19, height=2)
        label4_frame3.grid(row=0, column=3)

        label5_frame3 = Label(second_frame, text="Drink ", font=("Roboto Reguler", 10), width=19, height=2)
        label5_frame3.grid(row=0, column=4)

        count = 1
        queue = self.__elreda_service.get_queue_from_service_for_ui()
        for dto in queue:
            label_queue_no = Label(second_frame, text=count, font=("Roboto Reguler", 10), width=14, height=2)
            label_queue_no.grid(row=count, column=0)

            label_name = Label(second_frame, text=dto.name, font=("Roboto Reguler", 10), width=12, height=2)
            label_name.grid(row=count, column=1)

            label_table_no = Label(second_frame, text=dto.table_number, font=("Roboto Reguler", 10), width=10, height=2)
            label_table_no.grid(row=count, column=2)

            label_food = Label(second_frame, text=f"{dto.food}     {dto.amount_of_food}", font=("Roboto Reguler", 10), width=19, height=2)
            label_food.grid(row=count, column=3)

            label_drink = Label(second_frame, text=f"{dto.drink}     {dto.amount_of_drink}", font=("Roboto Reguler", 10), width=19, height=2)
            label_drink.grid(row=count, column=4)

            count += 1

        button_done_order = Button(second_frame, text="DONE", font=("Roboto Medium", 10), width=10, height=2, command=self.order_done)
        button_done_order.grid(row=count, column=4, pady=20, padx=10)

    def report_tab(self):
        self.frame.pack_forget()

        # *** SCROLL BAR
        frame4 = Frame(self.root)
        frame4.pack(fill=BOTH, expand=1)
        self.frame = frame4

        # create a canvas
        my_canvas = Canvas(frame4)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar to the canvas
        my_scrollbar = ttk.Scrollbar(frame4, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        # ***

        label1_frame4 = Label(second_frame, text="Date", font=("Roboto Reguler", 10), width=15, height=2)
        label1_frame4.grid(row=0, column=0)

        label2_frame4 = Label(second_frame, text="Food", font=("Roboto Reguler", 10), width=20, height=2)
        label2_frame4.grid(row=0, column=1)

        label3_frame4 = Label(second_frame, text="Total Food ", font=("Roboto Reguler", 10), width=11, height=2)
        label3_frame4.grid(row=0, column=2)

        label4_frame4 = Label(second_frame, text="Drink ", font=("Roboto Reguler", 10), width=15, height=2)
        label4_frame4.grid(row=0, column=3)

        label5_frame4 = Label(second_frame, text="Total Drink ", font=("Roboto Reguler", 10), width=11, height=2)
        label5_frame4.grid(row=0, column=4)

        order_dtos = self.__elreda_service.get_report_data()
        count = 1
        for dto in order_dtos:
            if count % 6 == 0:
                label_date = Label(second_frame, text=" ", font=("Roboto Reguler", 10), width=10, height=2)
                label_date.grid(row=count, column=0)
                count += 1

            label_date = Label(second_frame, text=dto.date, font=("Roboto Reguler", 10), width=15, height=2)
            label_date.grid(row=count, column=0)

            label_food = Label(second_frame, text=dto.food, font=("Roboto Reguler", 10),width=20, height=2)
            label_food.grid(row=count, column=1)

            label_amt_food = Label(second_frame, text=dto.amount_of_food, font=("Roboto Reguler", 10),width=1, height=2)
            label_amt_food.grid(row=count, column=2)

            label_drink = Label(second_frame, text=dto.drink, font=("Roboto Reguler", 10), width=15, height=2)
            label_drink.grid(row=count, column=3)

            label_amt_drink = Label(second_frame, text=dto.amount_of_drink, font=("Roboto Reguler", 10), width=1, height=2)
            label_amt_drink.grid(row=count, column=4)
            count += 1

        frame4.pack()

    def order_tab(self):
        if self.frame != None:
            self.frame.pack_forget()

        # frame2 untuk input order tab. Jika mau pindah ke tab lain, maka ganti frame dengan "frame2.forget"
        frame2 = Frame(self.root)
        self.frame = frame2
        label0_frame2 = Label(frame2, text="Order Quantity", font=("Roboto Reguler", 10), width=30, height=2)
        label0_frame2.grid(row=0, column=2, sticky=E)

        # ada 4 label : "Food", "Drink", "Table Number", "Name".
        label1_frame2 = Label(frame2, text=" Food                :", font=("Roboto Reguler", 10), width=30, height=2)
        label1_frame2.grid(row=1, column=0)

        label2_frame2 = Label(frame2, text="Drink               :", font=("Roboto Reguler", 10), width=30, height=2)
        label2_frame2.grid(row=2, column=0)

        label3_frame2 = Label(frame2, text="Table Number   :", font=("Roboto Reguler", 10), width=30, height=2)
        label3_frame2.grid(row=3, column=0)

        label4_frame2 = Label(frame2, text="Name              :", font=("Roboto Reguler", 10), width=30, height=2)
        label4_frame2.grid(row=4, column=0)

        # ada 3 dropdown dan 1 entry utk name

        # 1. Dropdown food menu options
        food_options = [
            "Kubideh Rice     ",
            "Fischteller      ",
            "Chicken Rice     ",
            "Gemischter Salad ",
            "Djujeh           "
        ]
        # datatype of menu text
        clicked_f = StringVar()

        # initial menu text
        clicked_f.set("Kubideh Rice     ")
        food_drop = OptionMenu(frame2, clicked_f, *food_options)
        food_drop.grid(row=1, column=1, sticky=W)
        self.drop_down_food = clicked_f  # Supaya bisa ambil value (.get) dengan memanggil self

        # 2. Dropdown drink menu options
        drink_options = [
            "Ayran                  ",
            "Coca cola              ",
            "Mineral Water          ",
            "Tea                    ",
            "Coffee                 "
        ]
        # datatype of menu text
        clicked_d = StringVar()

        # initial menu text
        clicked_d.set("Ayran                  ")
        drink_drop = OptionMenu(frame2, clicked_d, *drink_options)
        drink_drop.grid(row=2, column=1, sticky=W)
        self.drop_down_drink = clicked_d  # Supaya bisa ambil value (.get) dengan memanggil self

        # 3. Dropdown Table number options
        table_options = [
            "1                   ",
            "2                   ",
            "3                   ",
            "4                   ",
            "5                   ",
            "6                   ",
            "7                   ",
            "8                   ",
            "9                   ",
            "10                  ",
        ]
        # datatype of menu text
        clicked_t = StringVar()
        # initial menu text
        clicked_t.set("1              ")
        table_num_drop = OptionMenu(frame2, clicked_t, *table_options)
        table_num_drop.grid(row=3, column=1, sticky=W)
        self.drop_down_table_number = clicked_t

        # 4. Entry name
        entry_name = Entry(frame2, width=20, borderwidth=2)
        entry_name.grid(row=4, column=1, pady=3)
        self.entry_name = entry_name  # Supaya bisa ambil value (.get) dengan memanggil self

        entry_amount_of_food = Entry(frame2, width=5, borderwidth=2)
        entry_amount_of_food.grid(row=1, column=2, pady=3)
        self.entry_amount_of_food = entry_amount_of_food

        entry_amount_of_drink = Entry(frame2, width=5, borderwidth=2)
        entry_amount_of_drink.grid(row=2, column=2, pady=3)
        self.entry_amount_of_drink = entry_amount_of_drink

        busy, notice_text = self.__elreda_service.send_notice_at_order_page()
        if busy:
            label_warning = Label(frame2, text=notice_text, font=("Roboto Medium", 10))
            label_warning.grid(row=5, columnspan=2, sticky=W, padx=72, pady=10)

        button_submit_order = Button(frame2, text="ORDER", font=("Roboto Medium", 10), width=10, height=2,
                                     command=self.order_submit)
        button_submit_order.grid(row=6, column=2, pady=20, padx=10)

        frame2.pack()

    def start(self):
        self.root.title('El-Reda Restaurant')
        self.root.geometry('662x562')
        self.root.config(bg='#3C6135')

        # frame1 untuk tampilan (Nama dan Alamat Restaurant) dan Bar Tab (order | dapur | report)
        frame1 = Frame(self.root)

        # Label atas (Nama dan Alamat Restaurant)
        label1_frame1 = Label(frame1, text="El Reda \n Huttenstraße 69 - 70,\n 10553 Berlin, Germany",
                              font=("Roboto Bold", 14), fg="#FB031E", bg="#ECEFF2", width=18, height=3)
        label1_frame1.grid(column=1, row=1, pady=3)

        # Date
        label1_frame1 = Label(frame1, text=str(self.local_time), font=("Roboto Medium", 12), width=10, height=1)
        label1_frame1.grid(column=2, row=2, pady=2)

        # Button Bar
        button_order = Button(frame1, text="Order Tab", font=("Roboto Medium", 10), bg="#E3D663", width=30, height=2,
                              command=self.order_tab)
        button_dapur = Button(frame1, text="Kitchen Tab", font=("Roboto Medium", 10), bg="#E3D663", width=30, height=2,
                              command=self.kitchen_tab)
        button_report = Button(frame1, text="Report Tab", font=("Roboto Medium", 10), bg="#E3D663", width=30, height=2,
                               command=self.report_tab)
        button_order.grid(row=3, column=0, padx=0)
        button_dapur.grid(row=3, column=1, padx=0)
        button_report.grid(row=3, column=2, padx=0)

        frame1.pack()
        # frame1 done
        self.order_tab()

        self.root.mainloop()

