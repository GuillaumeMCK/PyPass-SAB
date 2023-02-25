from winreg import HKEYType, HKEY_CURRENT_USER
from winreg import OpenKey, QueryValueEx, SetValueEx, QueryInfoKey, EnumKey, DeleteKey


class Regedit(object):
    """
    Simple class to manage the registry
    """
    @staticmethod
    def get_value(key: str, sub_key: str) -> tuple[any, int]:
        """
        Get a value from the registry
        :param key: Key of the value
        :param sub_key: Name of the value
        :return: Tuple of the value and the type
        """
        return QueryValueEx(OpenKey(HKEY_CURRENT_USER, key), sub_key)

    @staticmethod
    def set_value(key: str, value: str, value_type: int, value_data: any) -> None:
        """
        Set a value in the registry
        :param key: Key of the value
        :param value: Name of the value
        :param value_type: Type of the value
        :param value_data: Data of the value
        :return: None
        """
        SetValueEx(OpenKey(HKEY_CURRENT_USER, key), value, 0, value_type, value_data)

    @staticmethod
    def delete_key(key: str) -> None:
        """
        Delete a key from the registry
        :param key: Key to delete
        :return: None
        """
        try:
            DeleteKey(HKEY_CURRENT_USER, key)
        except FileNotFoundError:
            pass

    @staticmethod
    def get_key(key: str) -> HKEYType:
        """
        Get a key from the registry
        :param key: Key to get
        :return: Key
        """
        return OpenKey(HKEY_CURRENT_USER, key)



    @staticmethod
    def get_sub_keys_in_key(key: HKEYType) -> list[str]:
        """
        Get all sub keys in a key
        :param key: Key to get the sub keys from
        :return: List of sub keys
        """
        return [EnumKey(key, i) for i in range(QueryInfoKey(key)[0])]
