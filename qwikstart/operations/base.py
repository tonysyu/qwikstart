import abc

__all__ = ["Operation"]


class Operation(abc.ABC):
    """An operation within an qwikstart `Task`"""

    name: str

    @abc.abstractmethod
    def run(self, context):
        """Override with action"""

    def pre_run(self, context):
        return context

    def post_run(self, context):
        return context

    def execute(self, context):
        context = self.pre_run(context)
        context = self.run(context)
        return self.post_run(context)
