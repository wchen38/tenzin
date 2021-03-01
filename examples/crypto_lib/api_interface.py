from abc import ABC, abstractmethod

class ApiInterface(ABC):
    @abstractmethod
    def get_realized_gain(self):
        pass

    @abstractmethod
    def get_unrealized_gain(self):
        pass

    @abstractmethod
    def get_crypto_tax(self):
        pass
