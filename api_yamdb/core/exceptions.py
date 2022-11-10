class SecretKeyError(Exception):
    """Вызывается, когда отсутствует SECRET_KEY."""

    def __init__(self):
        super().__init__('Отсутствует SECRET_KEY')