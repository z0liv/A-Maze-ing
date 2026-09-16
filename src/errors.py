class InvalidConfigError(Exception):
    """
    Exception raised when the configuration is invalid.
    """
    def __init__(self, messages: list[str]) -> None:
        """
            Initialize the exception with a list of error messages.

            Args:
                messages: List of one or more error messages.
        """
        prefix: str = "Invalid configuration: "
        super().__init__(prefix + "\n" + "\n".join(messages))
        self.messages = messages


class ParamsError(Exception):
    """
    Exception raised when the parameters are invalid.
    """
    def __init__(self, message: str) -> None:
        """
            Initialize the exception with an error message.

            Args:
                message: Error message to raise.
        """
        super().__init__(message)
        self.message = message
