from src.models.base_model import BaseModel


class FileInfo(BaseModel):
    is_original: bool = False
    original_hash: str = ""
    is_patched: bool = False
    patched_hash: str = ""
    version: str = ""
