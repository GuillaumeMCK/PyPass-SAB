FUNCS_FOOTPRINTS: dict[str, bytes] = {
    "CheckLicense": b'\x48\x89\x5c\x24\x08\x55\x56\x57\x48\x8d\xac\x24\x70\xff\xff\xff\x48\x81\xec\x90\x01\x00\x00\x48'
                    b'\x8b\xf1\x48\x8d\x4d\x20',
    "CompareFileTime": b'\x48\x89\x5c\x24\x18\x57\x48\x83\xec\x30\x48\x8d\x4c\x24\x48'
}

PATCHED_FUNCS_FOOTPRINTS: dict[str, bytes] = {
    "CheckLicense": b'\x48\xc7\x01\x01\x00\x00\x00\xb8\x01\x00\x00\x00\xc3',
    "CompareFileTime": b'\x48\x89\x5c\x24\x18\xb8\x00\x00\x00\x00\xc3'
}


def get_funcs_names() -> list[str]:
    """
    Get the names of the functions to search
    :return: List of the names of the functions
    """
    return list(FUNCS_FOOTPRINTS.keys())


def get_patch_funcs_names() -> list[str]:
    """
    Get the names of the functions to search in the patched file
    :return: List of the names of the functions
    """
    return list(PATCHED_FUNCS_FOOTPRINTS.keys())


def get_offset_from_footprint(file_path: str, footprint: bytes) -> int:
    """
    Find the offset of the footprint in the file.
    :param file_path: Path to the file to search in
    :param footprint: Footprint to search
    :return: Offset of the footprint in the file, or -1 if not found or file cannot be opened
    """
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            try:
                offset = file_content.index(footprint)
                return offset
            except ValueError:
                return -1
    except IOError:
        return -1
