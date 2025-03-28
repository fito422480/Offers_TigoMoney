from enum import Enum


class OfferLoadTypes(Enum):
    BATCH = "1"
    DIRECT = "2"
    PAYMENT = "3"
    REFINANCE = "4"
    MICRO_LOANS_OFFERS = "5"
    DA_COLLECTION = "6"


class OfferHeadersMandatory(Enum):
    DIRECT = ['FirstName', 'LastName']
    BATCH = ['FirstName', 'LastName']
    PREOFFER = []
    PAYMENT = []
    REFINANCE = []
    MICRO_LOAN_OFFERS = ['FirstName', 'LastName']
    DA_COLLECTION = []


class OffersFormatHeadersFileException(Exception):
    def __init__(self) -> None:
        self.message = 'El archivo de entrada no tiene formato correcto en las columnas'
        super().__init__(self.message)
