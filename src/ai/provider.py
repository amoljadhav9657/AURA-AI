from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def answer(self, text: str) -> str:
        pass
