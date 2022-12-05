from datetime import datetime
from os import path
from hashlib import sha1
from os import system, remove
from time import sleep

from tkinter.filedialog import askopenfilename
from tkinter import messagebox

from src.widgets.event_viewer import EventViewer
from src.models import Patch


def _get_file_name(path: str) -> str:
    return path.split("/")[-1]


class Patcher(object):
    _file_path = "C:/Program Files/StartAllBack/StartAllBackX64.dll"
    _file_hash = "3f38db606009e1fc4ea82beb357f8351d438c0d0"
    _patched_file_hash = "b812d69da8e057463f33ad500dabb7d52be6b6a5"
    _patches = [
        Patch(offset=0x1369, bytes=b'\xc7\x01\x01\x00\x00\x00\xb8\x01\x00\x00\x00\xc3'),
        Patch(offset=0x1564, bytes=b'\xb8\x00\x00\x00\x00\xc3')
    ]
    _backup_path = ""

    def __init__(self, _do_backup_func: any, ev: EventViewer):
        self.ev = ev
        self.checkup_is_valid = False
        self._do_backup_func = _do_backup_func
        # self._gen_patches(self._readFile("C:/Program Files/StartAllBack/StartAllBackX64.dll"),
        #                   self._readFile("C:/Program Files/StartAllBack/StartAllBackX64_patched.dll"))

    def checkup(self):
        """
        Check if the file is patched
        :return None
        """
        self.ev.event(f"Searching for {_get_file_name(self._file_path)}... ")
        if path.isfile(self._file_path):
            self.ev.event_done("Found")
            self.ev.event("Checking hash... ")
            if self._check_hash(self._file_path, self._file_hash, print_hash=True):
                self.ev.event_warning("Not patched")
                self.checkup_is_valid = True
            elif self._check_hash(self._file_path, self._patched_file_hash):
                self.ev.event_done("Patched")
            else:
                self.ev.event_error("File not matching")
                if messagebox.askyesno(
                        "File not matching",
                        "The file is not matching the original file. Do you want to patch it anyway ?"):
                    self.checkup_is_valid = True
                else:
                    self.checkup_is_valid = False
                    self._file_path = ""
        else:
            self.ev.event_error("Not found")
            self.ev.event("Select the file... ")
            self._file_path = askopenfilename(filetypes=[("DLL", "*.dll")])
            if self._file_path != "":
                self.ev.event_done("Selected")
                self.checkup()
            else:
                self.ev.event_error("Cancelled")
                self.checkup_is_valid = False

    def _get_hash(self, file_path: str, print_hash: bool = False) -> str:
        """
        Get the hash of a file
        :param file_path: Path of the file
        :param print_hash: Print the hash of the file
        :return Hash of the file
        """
        if not path.isfile(file_path):
            return ""
        with open(file_path, 'rb') as f:
            file_hash = sha1(f.read()).hexdigest()
        if print_hash:
            self.ev.event(f"{file_hash} ", color="blue")
        return file_hash

    def _check_hash(self, file_path: str, hash: str, print_hash: bool = False) -> bool:
        """
        Check if the hash of a file is matching
        :param file_path: Path of the file
        :param hash: Hash to compare
        :param print_hash: Print the hash of the file
        :return True if the hash is matching, False otherwise
        """
        return self._get_hash(file_path, print_hash) == hash

    def _create_backup(self) -> None:
        """
        Create a backup of the file.
        :return: None
        """
        self.ev.event("Creating backup... ")
        self._backup_path = self._file_path + f".{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.bak"
        if self._writeFile(self._backup_path, self._readFile(self._file_path)):
            self.ev.event_done("OK")

    def patch(self) -> None:
        """
        Patch the file
        :return None
        """
        self.ev.add_banner("Start patch")
        if self.checkup_is_valid:
            if self._do_backup_func():
                self._create_backup()
            original_file = self._readFile(self._file_path)
            patched_file = original_file
            self.ev.event("Stop explorer.exe", end="\n")
            system("taskkill /f /im explorer.exe")
            self.ev.event("Patching... ")
            for patch in self._patches:
                patched_file = patched_file[:patch.offset] + patch.bytes + patched_file[patch.offset + len(patch.bytes):]
            sleep(1)  # Wait for explorer
            if self._writeFile(self._file_path, patched_file):
                self.ev.event_done("Done")
                self.ev.event("Checking hash... ")
                if self._check_hash(self._file_path, self._patched_file_hash, print_hash=True):
                    self.ev.event_done("Patched")
                else:
                    self.ev.event_error("Not matching")
                    self.ev.event("Restoring backup... ")
                    if self._writeFile(self._file_path, original_file):
                        self.ev.event_done("Done")
            else:
                self.ev.event_error("Failed")
            self.ev.event("Start explorer.exe", end="\n")
            system("start explorer.exe")
        else:
            self.ev.event_error("Checkup not valid")
        self.ev.add_banner("End of patch")

    def _writeFile(self, file_path: str, data: bytes) -> bool:
        """
        Write data to a file
        :param file_path: Path to the file
        :param data: Data to write
        :return True if the file was written, False otherwise
        """
        try:
            if path.isfile(file_path):
                remove(file_path)
            with open(file_path, 'wb') as f:
                f.write(data)
            return True
        except IOError as e:
            self.ev.event_error("Error while writing file : " + str(e))
            return False

    def _readFile(self, path: str) -> bytes:
        """
        :param path: Path of the file
        :return Data of the file
        """
        try:
            with open(path, 'rb') as f:
                return f.read()
        except IOError as e:
            self.ev.event_error("Error while reading file : " + str(e))
            raise e

    @staticmethod
    def _gen_patches(original_file: bytes, patched_file: bytes) -> list[Patch]:
        """
        Generate patches from two files
        :param original_file: The original file
        :param patched_file: The patched file created with ghidra
        :return: The list of patches
        """
        patches = []
        patch_size = 0
        for i in range(len(original_file)):
            if original_file[i] != patched_file[i]:
                patch_size += 1
            elif patch_size > 0:
                patches.append(Patch(offset=i - patch_size, bytes=patched_file[i - patch_size:i]))
                patch_size = 0
        for patch in patches:
            print(f'Patch(offset={hex(patch.offset)}, bytes={patch.bytes})')
        return patches
