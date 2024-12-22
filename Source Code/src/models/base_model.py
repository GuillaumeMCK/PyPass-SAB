class BaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dict(self) -> dict:
        return self.__dict__

    def to_str(self) -> str:
        return str(self.__dict__)
