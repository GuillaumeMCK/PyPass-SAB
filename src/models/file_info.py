from src.models.base_model import BaseModel
from src.datas import get_funcs_names


class FileInfo(BaseModel):
    is_original: bool = False
    original_hash: str = ""
    is_patched: bool = False
    patched_hash: str = ""
    version: str = ""
    funcs_offset: dict[str, int | None] = dict.fromkeys(get_funcs_names(), None)

    def isValid(self) -> bool:
        """
        Check if the file info is valid
        note: the file info is valid if it's original and patched and the original hash and patched hash and version are
        not empty or if all the functions offset are not empty
        :return:
        """
        return (self.is_original and self.is_patched and self.original_hash and self.patched_hash and self.version) or \
            self.haveFuncsOffset()

    def haveFuncsOffset(self) -> bool:
        """
        Check if the file info have the functions offset set (false if eq -1)
        :return:
        """
        return all([offset != -1 for offset in self.funcs_offset.values()])
