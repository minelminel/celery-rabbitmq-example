from abc import ABC, abstractmethod

class BaseParser(ABC):

    def __init__(self, *args):
        raise NotImplementedError()

    @staticmethod
    def _strain_links():
        raise NotImplementedError()

    @abstractmethod
    def _extract_title():
        raise NotImplementedError()

    @abstractmethod
    def _extract_text():
        raise NotImplementedError()

    @abstractmethod
    def _extract_captions():
        raise NotImplementedError()

    @abstractmethod
    def _extract_links():
        raise NotImplementedError()

    @abstractmethod
    def extract_content():
        raise NotImplementedError()
