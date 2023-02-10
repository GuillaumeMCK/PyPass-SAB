from src.models import Patch

PATCHES_REPOSITORY = [
    {
        "version": "3.5.5",
        "original_hash": "3f38db606009e1fc4ea82beb357f8351d438c0d0",
        "patched_hash": "b812d69da8e057463f33ad500dabb7d52be6b6a5",
        "patches": [
            {"offset": 0x1369, "bytes": b"\xc7\x01\x01\x00\x00\x00\xb8\x01\x00\x00\x00\xc3"},
            {"offset": 0x1564, "bytes": b"\xb8\x00\x00\x00\x00\xc3"},
        ]
    },
    {
        "version": "3.5.6",
        "original_hash": "00d51d42b6715fbc7a822e0ec443b6c74eacd7a7",
        "patched_hash": "264649730808f5ec7259f2a54feda2651f04705c",
        "patches": [
            {"offset": 0x1369, "bytes": b"\xc7\x01\x01\x00\x00\x00\xb8\x01\x00\x00\x00\xc3"},
            {"offset": 0x1564, "bytes": b"\xb8\x00\x00\x00\x00\xc3"},
        ]
    },
    {
        "version": "3.5.7",
        "original_hash": "5e4009d5400360af836045eaf76cd6dcb15c688b",
        "patched_hash": "26b168a2db8a7ed62ba4222bef1bfd2db064dc8e",
        "patches": [
            {"offset": 0x1369, "bytes": b"\xc7\x01\x01\x00\x00\x00\xb8\x01\x00\x00\x00\xc3"},
            {"offset": 0x1564, "bytes": b"\xb8\x00\x00\x00\x00\xc3"},
        ]
    },
    {
        "version": "v3.6.0", "original_hash": "c517f366c06400fbf89b142090d6842c224afc8a",
        "patched_hash": "bc759d64b3d7af277814e2ceae3dbf9577f3a24e",
        "patches": [
            {"offset": 4972, "bytes": b"gH\xc7\x01\x01\x00\x00\x00"},
            {"offset": 4981, "bytes": b"\xc7\xc0\x01\x00\x00\x00\xc3"},
            {"offset": 5480, "bytes": b"\xb8\x00\x00\x00\x00\xc3"}
        ]
    },
]


def create_patch_repo(version: str, original_hash: str, patched_hash: str, patches: list[Patch]) -> dict[str, any]:
    return {
        "version": version,
        "original_hash": original_hash,
        "patched_hash": patched_hash,
        "patches": [patch.dict() for patch in patches]
    }
