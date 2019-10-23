import abc

__all__ = ["Operation"]


class Operation(abc.ABC):
    """An operation within an qwikstart `Task`"""

    name: str

    @abc.abstractmethod
    def run(self, context):
        """Override with action"""
