class DuplicateProxyError(Exception):
    """Исключение, возбуждаемое при попытке добавить дубликат прокси."""
    def __init__(self, host: str, port: int, message: str | None = None):
        self.host = host
        self.port = port
        if message is None:
            message = f"Proxy with host='{self.host}' and port={self.port} already exists."
        super().__init__(message) 