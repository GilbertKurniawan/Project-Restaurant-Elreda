from elreda_v1.uis import ElredaUI

from kink import inject

@inject
class Container:
    def __init__(self, _elreda_ui:ElredaUI):
        self.__elreda_ui = _elreda_ui

    def init(self):
        self.__elreda_ui.init()

    def run(self):
        self.__elreda_ui.start()


