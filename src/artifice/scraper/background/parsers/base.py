from abc import ABC, abstractmethod

class BaseParser(ABC):

    def __init__(self):
        pass

    @staticmethod
    def _strain_links():
        pass

    @abstractmethod
    def _extract_title(self):
        pass

    @abstractmethod
    def _extract_text(self):
        pass

    @abstractmethod
    def _extract_captions(self):
        pass

    @abstractmethod
    def _extract_links(self):
        pass

    @abstractmethod
    def extract_content(self):
        pass
