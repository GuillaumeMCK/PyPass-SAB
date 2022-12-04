from src.models.base_model import BaseModel


class Patch(BaseModel):
    offset: int
    bytes: bytes
