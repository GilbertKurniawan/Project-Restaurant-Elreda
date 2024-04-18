from elreda_v2.uis import ElredaUIV2

from kink import inject

@inject
class Container:
    def __init__(self, _elreda_ui:ElredaUIV2):
        self.__elreda_ui = _elreda_ui

    def init(self):
        self.__elreda_ui.init()

    def run(self):
        self.__elreda_ui.start()


