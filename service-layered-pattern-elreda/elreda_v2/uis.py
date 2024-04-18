from elreda_v1.uis import ElredaUI
from elreda_v2.services import ElredaServiceV2
from kink import inject

@inject
class ElredaUIV2(ElredaUI):
    def __init__(self, _elreda_service: ElredaServiceV2):
        super().__init__(_elreda_service)