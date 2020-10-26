from abc import ABC, abstractmethod

class Interface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def recive(self):
        pass