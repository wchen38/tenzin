from abc import ABC, abstractmethod

class ApiInterface(ABC):
    @abstractmethod
    def getRealizedGain(self):
        pass

    @abstractmethod
    def getUnrealizedGain(self):
        pass

    @abstractmethod
    def getCryptoTax(self):
        pass
