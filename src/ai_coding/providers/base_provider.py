from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate_code(
        self,
        task,
        requirements,
        architecture
    ):
        pass

    @abstractmethod
    def fix_code(
        self,
        task,
        requirements,
        architecture,
        files,
        errors
    ):
        pass