class ConsoleDefinition:
    _description: str
    _usage: str
    _parameter_title: str
    _parameters: dict

    def __init__(self, description: str, usage: str, parameter_title: str, parameters: dict):
        self._description = description
        self._usage = usage
        self._parameter_title = parameter_title
        self._parameters = parameters

    @property
    def description(self) -> str:
        return self._description

    @property
    def usage(self) -> str:
        return self._usage

    @property
    def parameter_title(self) -> str:
        return self._parameter_title

    @property
    def parameters(self) -> dict:
        return self._parameters