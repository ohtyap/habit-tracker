class ConsoleDefinition:
    # Description of the command. Used for the help overview
    _description: str

    # Usage line for help
    _usage: str

    # In case of parameters, a meaningful title for the help command
    _parameter_title: str

    # Available parameters as dictionary
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